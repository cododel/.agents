"""Capability contract, component probes, and shared process helpers."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SCRIPT_ROOT.parent
CAPABILITY_ROOT = REPO_ROOT / "capabilities" / "code-intelligence"
MANIFEST_PATH = CAPABILITY_ROOT / "manifest.json"
MCPLS_CONFIG_PATH = CAPABILITY_ROOT / "mcpls.toml"
VERSION_RE = re.compile(r"(?<!\d)(\d+)\.(\d+)\.(\d+)(?!\d)")
CLIENT_IDS = (
    "codex", "antigravity", "grok", "claude-code", "kimi-code", "opencode", "pi",
)


class ScaffoldError(Exception):
    """An actionable validation, compatibility, or configuration error."""


def fail(message):
    raise ScaffoldError(message)


def exact_keys(value, expected, label):
    if not isinstance(value, dict):
        fail("{} must be an object".format(label))
    actual = set(value)
    wanted = set(expected)
    if actual != wanted:
        fail("{} keys differ: missing={}, unexpected={}".format(
            label, sorted(wanted - actual), sorted(actual - wanted)
        ))


def string_list(value, label, nonempty=True):
    if not isinstance(value, list) or (nonempty and not value):
        fail("{} must be {}array".format(label, "a non-empty " if nonempty else "an "))
    if any(not isinstance(item, str) or not item for item in value):
        fail("{} must contain non-empty strings".format(label))


def parse_version(output):
    match = VERSION_RE.search(output)
    return tuple(int(part) for part in match.groups()) if match else None


def run(argv, check=True, capture=True, cwd=None):
    try:
        completed = subprocess.run(
            argv,
            cwd=str(cwd) if cwd else None,
            text=True,
            stdout=subprocess.PIPE if capture else None,
            stderr=subprocess.PIPE if capture else None,
        )
    except OSError as exc:
        fail("cannot run {}: {}".format(argv[0], exc))
    if check and completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "").strip()
        fail("command failed ({}): {}".format(" ".join(argv), detail or completed.returncode))
    return completed


def expand_path(value):
    home = Path(os.environ.get("HOME", str(Path.home()))).expanduser()
    kimi_home = Path(os.environ.get("KIMI_CODE_HOME", str(home / ".kimi-code"))).expanduser()
    xdg_home = Path(os.environ.get("XDG_CONFIG_HOME", str(home / ".config"))).expanduser()
    replacements = {
        "{repo_root}": str(REPO_ROOT),
        "{home}": str(home),
        "{kimi_code_home}": str(kimi_home),
        "{xdg_config_home}": str(xdg_home),
    }
    expanded = value
    for marker, replacement in replacements.items():
        expanded = expanded.replace(marker, replacement)
    return Path(expanded)


def desired_command(manifest, client_id, mcpls_path):
    delta = manifest["client_deltas"][client_id]
    args = [item.replace("{repo_root}", str(REPO_ROOT)) for item in delta.get("args", [])]
    return str(Path(mcpls_path).resolve()), args


def read_manifest():
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        fail("cannot read manifest: {}".format(exc))
    exact_keys(
        manifest,
        ["schema_version", "id", "platforms", "components", "language_servers",
         "client_deltas", "expected_mcp_tools"],
        "manifest",
    )
    if manifest["schema_version"] != 2 or manifest["id"] != "code-intelligence":
        fail("manifest schema_version/id must be 2/code-intelligence")
    if manifest["platforms"] != ["darwin"]:
        fail("v2 platforms must be exactly ['darwin']")
    validate_components(manifest["components"])
    validate_language_servers(manifest["language_servers"])
    validate_client_deltas(manifest["client_deltas"])
    expected_tools = [
        "get_hover", "get_definition", "get_references", "get_diagnostics",
        "get_code_actions", "get_document_symbols", "workspace_symbol_search", "rename_symbol",
        "prepare_call_hierarchy", "get_incoming_calls", "get_outgoing_calls",
    ]
    if manifest["expected_mcp_tools"] != expected_tools:
        fail("expected_mcp_tools must preserve the v2 semantic contract")
    validate_mcpls_config(manifest)
    return manifest


def validate_components(components):
    exact_keys(components, ["mcpls", "ast-grep"], "components")
    contracts = {
        "mcpls": (
            "exact", "0.3.9", "cargo", ["manager", "argv"],
            ["cargo", "install", "mcpls", "--version", "0.3.9", "--locked"], None,
        ),
        "ast-grep": (
            "minimum", "0.45.0", "brew", ["manager", "argv", "upgrade_argv"],
            ["brew", "install", "ast-grep"], ["brew", "upgrade", "ast-grep"],
        ),
    }
    for name, contract in contracts.items():
        component = components[name]
        exact_keys(component, ["binary", "version", "install"], "components.{}".format(name))
        if component["binary"] != name:
            fail("components.{}.binary must be {}".format(name, name))
        exact_keys(component["version"], ["policy", "value"], "components.{}.version".format(name))
        if (component["version"]["policy"], component["version"]["value"]) != contract[:2]:
            fail("components.{} version contract changed".format(name))
        install = component["install"]
        exact_keys(install, contract[3], "components.{}.install".format(name))
        if install["manager"] != contract[2] or install["argv"] != contract[4]:
            fail("components.{} install contract changed".format(name))
        string_list(install["argv"], "components.{}.install.argv".format(name))
        if "upgrade_argv" in install and install["upgrade_argv"] != contract[5]:
            fail("components.{} upgrade command changed".format(name))


def validate_language_servers(servers):
    expected = {
        "python": ("basedpyright-langserver", ["basedpyright", "--version"], [], True),
        "typescript": (
            "typescript-language-server", ["typescript-language-server", "--version"], [], False,
        ),
        "php": (
            "intelephense",
            ["npm", "list", "--global", "--depth=0", "intelephense@1.18.5"],
            ["npm", "install", "--global", "intelephense@1.18.5"], False,
        ),
        "rust": (
            "rust-analyzer", ["rust-analyzer", "--version"],
            ["rustup", "component", "add", "rust-analyzer"], False,
        ),
        "cpp": ("clangd", ["clangd", "--version"], [], False),
        "swift": ("sourcekit-lsp", ["sourcekit-lsp", "--help"], [], False),
    }
    if not isinstance(servers, list) or len(servers) != len(expected):
        fail("language_servers must contain the exact v2 server set")
    seen = set()
    smoke = []
    for index, server in enumerate(servers):
        label = "language_servers[{}]".format(index)
        exact_keys(server, ["id", "command", "probe_argv", "repair_argv", "semantic_smoke"], label)
        server_id = server["id"]
        actual = (
            server["command"], server["probe_argv"], server["repair_argv"],
            server["semantic_smoke"],
        )
        if server_id in seen or expected.get(server_id) != actual:
            fail("{} has an unknown, mismatched, or duplicate server".format(label))
        seen.add(server_id)
        if server["semantic_smoke"]:
            smoke.append(server_id)
    if seen != set(expected) or smoke != ["python"]:
        fail("language server set or semantic smoke owner changed")


def validate_client_deltas(deltas):
    exact_keys(deltas, CLIENT_IDS, "client_deltas")
    common = {
        "type", "adapter", "detection", "required_components", "scope",
        "server_name", "command_component", "args",
    }
    adapter_contracts = {
        "codex": ("codex_cli", common),
        "antigravity": ("json_file", common | {"config"}),
        "grok": ("grok_cli", common),
        "claude-code": ("claude_cli", common | {"inspect_path"}),
        "kimi-code": ("json_file", common | {"config"}),
        "opencode": ("opencode_jsonc", common | {"config"}),
    }
    expected_args = ["--config", "{repo_root}/capabilities/code-intelligence/mcpls.toml"]
    for client_id, (adapter, keys) in adapter_contracts.items():
        delta = deltas[client_id]
        exact_keys(delta, keys, "client_deltas.{}".format(client_id))
        if (
            delta["type"] != "mcp_stdio" or delta["adapter"] != adapter
            or delta["scope"] != "user" or delta["server_name"] != "mcpls"
            or delta["command_component"] != "mcpls" or delta["args"] != expected_args
            or delta["required_components"] != ["mcpls", "ast-grep"]
        ):
            fail("client_deltas.{} MCP contract changed".format(client_id))
        validate_detection(client_id, delta["detection"])
    validate_json_client(deltas["antigravity"], "antigravity")
    validate_json_client(deltas["kimi-code"], "kimi-code")
    validate_opencode(deltas["opencode"])
    if deltas["claude-code"]["inspect_path"] != "{home}/.claude.json":
        fail("Claude Code inspection path changed")
    pi = deltas["pi"]
    exact_keys(
        pi, ["type", "adapter", "detection", "required_components", "lsp", "reason"],
        "client_deltas.pi",
    )
    validate_detection("pi", pi["detection"])
    if (
        pi["type"] != "rules_ast_only" or pi["adapter"] != "none"
        or pi["required_components"] != ["ast-grep"] or pi["lsp"] != "unsupported"
        or not isinstance(pi["reason"], str) or not pi["reason"]
    ):
        fail("Pi rules/AST-only contract changed")


def validate_detection(client_id, detection):
    if client_id == "antigravity":
        exact_keys(detection, ["kind", "bundle_id", "paths"], "antigravity.detection")
        if (
            detection["kind"] != "darwin_bundle"
            or detection["bundle_id"] != "com.google.antigravity"
            or detection["paths"] != [
                "/Applications/Antigravity.app", "{home}/Applications/Antigravity.app",
            ]
        ):
            fail("Antigravity bundle detection changed")
        return
    expected_binary = {
        "codex": "codex", "grok": "grok", "claude-code": "claude",
        "kimi-code": "kimi", "opencode": "opencode", "pi": "pi",
    }[client_id]
    exact_keys(detection, ["kind", "value"], "{}.detection".format(client_id))
    if detection != {"kind": "binary", "value": expected_binary}:
        fail("{} binary detection changed".format(client_id))


def validate_json_client(delta, client_id):
    config = delta["config"]
    exact_keys(config, ["format", "path", "entry_path", "entry_shape"], "{}.config".format(client_id))
    expected = {
        "antigravity": "{home}/.gemini/config/mcp_config.json",
        "kimi-code": "{kimi_code_home}/mcp.json",
    }[client_id]
    if (
        config["format"] != "json" or config["path"] != expected
        or config["entry_path"] != ["mcpServers", "mcpls"]
        or config["entry_shape"] != "command_args"
    ):
        fail("{}.config contract changed".format(client_id))


def validate_opencode(delta):
    config = delta["config"]
    exact_keys(
        config, ["format", "directory", "candidates", "entry_paths", "entry_shape"],
        "opencode.config",
    )
    exact_keys(config["entry_paths"], ["1", "2"], "opencode.config.entry_paths")
    if (
        config["format"] != "jsonc"
        or config["directory"] != "{xdg_config_home}/opencode"
        or config["candidates"] != ["opencode.jsonc", "opencode.json", "config.json"]
        or config["entry_paths"] != {
            "1": ["mcp", "mcpls"], "2": ["mcp", "servers", "mcpls"],
        }
        or config["entry_shape"] != "opencode"
    ):
        fail("OpenCode config contract changed")


def validate_mcpls_config(manifest):
    try:
        content = MCPLS_CONFIG_PATH.read_text(encoding="utf-8")
    except OSError as exc:
        fail("cannot read mcpls.toml: {}".format(exc))
    if "--trust-project-config" in content or "MCPLS_TRUST_PROJECT_CONFIG" in content:
        fail("mcpls.toml must not enable project configuration trust")
    required = [
        "[workspace]", "roots = []", "heuristics_max_depth = 10",
        "[[lsp_servers]]", "[lsp_servers.heuristics]",
        'file_patterns = ["**/*.py", "**/*.pyi"]',
        'project_markers = ["pyproject.toml", "setup.py", "requirements.txt", "pyrightconfig.json"]',
        'file_patterns = ["**/*.ts", "**/*.tsx", "**/*.js", "**/*.jsx", "**/*.mjs", "**/*.cjs", "**/*.mts", "**/*.cts"]',
        'project_markers = ["package.json", "tsconfig.json", "jsconfig.json"]',
        'file_patterns = ["**/*.php"]',
        'project_markers = ["composer.json", "composer.lock", "phpstan.neon", "phpstan.neon.dist", "psalm.xml", "phpunit.xml", "phpunit.xml.dist"]',
        'file_patterns = ["**/*.rs"]',
        'project_markers = ["Cargo.toml", "rust-toolchain.toml", "rust-project.json"]',
        'file_patterns = ["**/*.c", "**/*.cc", "**/*.cpp", "**/*.cxx", "**/*.h", "**/*.hh", "**/*.hpp", "**/*.hxx"]',
        'project_markers = ["compile_commands.json", "CMakeLists.txt", "Makefile", ".clangd"]',
        'file_patterns = ["**/*.swift"]',
        'project_markers = ["Package.swift", "project.pbxproj"]',
    ]
    for server in manifest["language_servers"]:
        required.append('command = "{}"'.format(server["command"]))
    missing = [item for item in required if item not in content]
    if missing:
        fail("mcpls.toml is missing required invariants: {}".format(sorted(set(missing))))
    if content.count("[[lsp_servers]]") != len(manifest["language_servers"]):
        fail("mcpls.toml language server count differs from manifest")
    if content.count("[lsp_servers.heuristics]") != len(manifest["language_servers"]):
        fail("each mcpls language server must have deferred-start heuristics")


def ensure_platform(manifest):
    if sys.platform not in manifest["platforms"]:
        fail("unsupported platform {!r}; v2 supports only darwin and made no changes".format(sys.platform))


def component_status(name, component):
    path = shutil.which(component["binary"])
    if not path:
        return {"name": name, "state": "missing", "path": None, "version": None}
    completed = run([path, "--version"], check=False)
    version = parse_version((completed.stdout or "") + "\n" + (completed.stderr or ""))
    if completed.returncode != 0 or version is None:
        return {"name": name, "state": "broken", "path": str(Path(path).resolve()), "version": None}
    required = parse_version(component["version"]["value"])
    policy = component["version"]["policy"]
    compatible = version == required if policy == "exact" else version >= required
    return {
        "name": name,
        "state": "ready" if compatible else "incompatible",
        "path": str(Path(path).resolve()),
        "version": ".".join(str(part) for part in version),
    }


def language_server_status(server):
    command_path = shutil.which(server["command"])
    probe = list(server["probe_argv"])
    probe_path = shutil.which(probe[0])
    if not command_path:
        state = "missing"
    elif not probe_path:
        state = "broken"
    else:
        probe[0] = probe_path
        state = "ready" if run(probe, check=False).returncode == 0 else "broken"
    return {
        "id": server["id"], "state": state, "command": server["command"],
        "repair_argv": server["repair_argv"],
    }


def install_components(manifest, statuses):
    for name, status in statuses.items():
        if status["state"] == "ready":
            continue
        install = manifest["components"][name]["install"]
        manager = shutil.which(install["manager"])
        if not manager:
            fail("{} is required to install {}".format(install["manager"], name))
        argv = list(install["argv"])
        if name == "ast-grep" and status["state"] != "missing":
            argv = list(install["upgrade_argv"])
        argv[0] = manager
        run(argv, capture=False)
