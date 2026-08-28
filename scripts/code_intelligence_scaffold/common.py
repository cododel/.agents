"""Manifest validation, component probes, and shared process helpers."""

import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


SCRIPT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SCRIPT_ROOT.parent
MANIFEST_PATH = REPO_ROOT / "capabilities" / "code-intelligence" / "manifest.json"
VERSION_RE = re.compile(r"(?<!\d)(\d+)\.(\d+)\.(\d+)(?!\d)")
LEGACY_CLIENT_IDS = (
    "codex", "antigravity", "grok", "claude-code", "kimi-code", "opencode",
)


class ScaffoldError(Exception):
    """An actionable validation, compatibility, or configuration error."""


def fail(message):
    raise ScaffoldError(message)


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
    replacements = {
        "{home}": str(home),
        "{kimi_code_home}": os.environ.get("KIMI_CODE_HOME", str(home / ".kimi-code")),
        "{xdg_config_home}": os.environ.get("XDG_CONFIG_HOME", str(home / ".config")),
    }
    for marker, replacement in replacements.items():
        value = value.replace(marker, replacement)
    return Path(value).expanduser()


def parse_version(output):
    match = VERSION_RE.search(output)
    return tuple(int(part) for part in match.groups()) if match else None


def component_status(component):
    path = shutil.which(component["binary"])
    if not path:
        return {"state": "missing", "path": None, "version": None}
    completed = run([path, "--version"], check=False)
    version = parse_version((completed.stdout or "") + "\n" + (completed.stderr or ""))
    if completed.returncode != 0 or version is None:
        return {"state": "broken", "path": str(Path(path).resolve()), "version": None}
    required = parse_version(component["version"]["value"])
    compatible = version == required if component["version"]["policy"] == "exact" else version >= required
    return {
        "state": "ready" if compatible else "incompatible",
        "path": str(Path(path).resolve()),
        "version": ".".join(str(part) for part in version),
    }


def language_server_status(server):
    command = shutil.which(server["command"])
    probe = list(server["probe_argv"])
    probe_path = shutil.which(probe[0])
    if not command:
        state = "missing"
    elif not probe_path:
        state = "broken"
    else:
        probe[0] = probe_path
        state = "ready" if run(probe, check=False).returncode == 0 else "broken"
    return {
        "id": server["id"],
        "state": state,
        "command": server["command"],
        "repair_argv": server["repair_argv"],
    }


def _string_list(value, label, allow_empty=False):
    if not isinstance(value, list) or (not allow_empty and not value):
        fail("{} must be an array{}".format(label, "" if allow_empty else " with values"))
    if any(not isinstance(item, str) or not item for item in value):
        fail("{} must contain non-empty strings".format(label))


def read_manifest():
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        fail("cannot read manifest: {}".format(exc))
    expected_keys = {
        "schema_version", "id", "platforms", "components", "language_servers",
        "project_harnesses", "legacy_global_registries", "expected_mcp_tools",
    }
    if set(manifest) != expected_keys:
        fail("manifest keys differ from schema v3")
    if manifest["schema_version"] != 3 or manifest["id"] != "code-intelligence":
        fail("manifest schema_version/id must be 3/code-intelligence")
    if manifest["platforms"] != ["darwin"]:
        fail("platforms must be exactly ['darwin']")
    if set(manifest["components"]) != {"mcpls", "ast-grep"}:
        fail("components must contain mcpls and ast-grep")
    mcpls = manifest["components"]["mcpls"]
    if mcpls["binary"] != "mcpls" or mcpls["version"] != {"policy": "exact", "value": "0.3.9"}:
        fail("mcpls must remain pinned to 0.3.9")
    expected_languages = {"python", "typescript", "php", "rust", "cpp", "swift"}
    seen = set()
    for index, server in enumerate(manifest["language_servers"]):
        required = {
            "id", "language_id", "command", "args", "file_patterns", "project_markers",
            "probe_argv", "repair_argv", "semantic_smoke",
        }
        if set(server) != required:
            fail("language_servers[{}] keys differ from schema v3".format(index))
        if server["id"] in seen:
            fail("duplicate language server {}".format(server["id"]))
        seen.add(server["id"])
        for key in ("file_patterns", "project_markers", "probe_argv", "repair_argv"):
            _string_list(server[key], "language_servers[{}].{}".format(index, key))
        _string_list(server["args"], "language_servers[{}].args".format(index), allow_empty=True)
    if seen != expected_languages:
        fail("language server set must be python/typescript/php/rust/cpp/swift")
    if [item["id"] for item in manifest["language_servers"] if item["semantic_smoke"]] != ["python"]:
        fail("Python must remain the semantic smoke owner")
    if set(manifest["project_harnesses"]) != {"root-mcp-json", "codex"}:
        fail("project harnesses must be root mcp.json and Codex")
    if set(manifest["legacy_global_registries"]) != set(LEGACY_CLIENT_IDS):
        fail("legacy registry set changed")
    return manifest


def ensure_platform(manifest):
    if sys.platform not in manifest["platforms"]:
        fail("unsupported platform {!r}; no changes made".format(sys.platform))
