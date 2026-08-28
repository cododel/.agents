"""Project-scoped mcpls discovery and source-preserving harness configuration."""

from copy import deepcopy
import fnmatch
import json
import os
from pathlib import Path
import re

from .common import component_status, fail, language_server_status, run
from .jsonc import atomic_write, get_path, set_path


OWNER_MARKER = "# Managed by $setup-project-mcpls; re-run the skill to update."
IGNORED_DIRECTORIES = {
    ".git", ".hg", ".svn", ".cache", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    ".tox", ".venv", "venv", "node_modules", "vendor", "target", "dist", "build",
    "coverage", ".coverage", ".next", ".nuxt", ".output", "out", "__pycache__",
}
TABLE_RE = re.compile(r"^\s*\[([^\]]+)\]\s*(?:#.*)?$")
ASSIGNMENT_RE = re.compile(r"^(\s*)([A-Za-z0-9_-]+)(\s*=\s*)(.*?)(\r?\n)?$")


def resolve_git_root(candidate):
    path = Path(candidate).expanduser().resolve()
    completed = run(["git", "-C", str(path), "rev-parse", "--show-toplevel"], check=False)
    if completed.returncode != 0:
        fail("{} is not inside a Git checkout; no changes made".format(path))
    root = Path(completed.stdout.strip()).resolve()
    home = Path(os.environ.get("HOME", str(Path.home()))).expanduser().resolve()
    if root == Path("/") or root == home:
        fail("refusing unsafe Git root {}; no changes made".format(root))
    return root


def _matches(path, patterns):
    value = path.as_posix()
    return any(
        fnmatch.fnmatchcase(value, pattern)
        or (pattern.startswith("**/") and fnmatch.fnmatchcase(value, pattern[3:]))
        for pattern in patterns
    )


def detect_languages(root, manifest):
    files = []
    for directory, names, filenames in os.walk(root):
        names[:] = sorted(name for name in names if name not in IGNORED_DIRECTORIES)
        base = Path(directory)
        for filename in sorted(filenames):
            files.append((base / filename).relative_to(root))
    detected = []
    for server in manifest["language_servers"]:
        marker_names = set(server["project_markers"])
        has_marker = any(path.name in marker_names for path in files)
        has_source = any(_matches(path, server["file_patterns"]) for path in files)
        if has_marker and has_source:
            detected.append(server)
    return detected


def render_mcpls_config(root, servers):
    lines = [
        OWNER_MARKER,
        "",
        "[workspace]",
        "roots = [{}]".format(json.dumps(str(root))),
        "heuristics_max_depth = 10",
    ]
    for server in servers:
        lines.extend([
            "",
            "[[lsp_servers]]",
            "language_id = {}".format(json.dumps(server["language_id"])),
            "command = {}".format(json.dumps(server["command"])),
            "args = {}".format(json.dumps(server["args"])),
            "file_patterns = {}".format(json.dumps(server["file_patterns"])),
            "[lsp_servers.heuristics]",
            "project_markers = {}".format(json.dumps(server["project_markers"])),
        ])
    return "\n".join(lines) + "\n"


def _is_mcpls_command(command):
    return isinstance(command, str) and Path(command).name == "mcpls"


def _read_jsonc(path):
    try:
        source = path.read_text(encoding="utf-8")
        get_path(source, [])
    except OSError as exc:
        fail("cannot read {}: {}".format(path, exc))
    except Exception as exc:
        fail("cannot parse {}: {}".format(path, exc))
    return source


def _json_update(path, mcpls_path):
    source = _read_jsonc(path)
    found, existing = get_path(source, ["mcpServers", "mcpls"])
    if found and (not isinstance(existing, dict) or not _is_mcpls_command(existing.get("command"))):
        fail("{} has a foreign mcpServers.mcpls entry; no changes made".format(path))
    desired = deepcopy(existing) if found else {}
    desired["command"] = mcpls_path
    desired["args"] = ["--config", ".agents/mcpls.toml"]
    return set_path(source, ["mcpServers", "mcpls"], desired)


def _read_toml_source(path):
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as exc:
        fail("cannot read {}: {}".format(path, exc))
    return source


def _toml_literal(value):
    if isinstance(value, bool):
        return "true" if value else "false"
    return json.dumps(value)


def _toml_value_and_comment(value):
    quote = None
    escaped = False
    for index, character in enumerate(value):
        if escaped:
            escaped = False
        elif character == "\\" and quote == '"':
            escaped = True
        elif character in ('"', "'"):
            quote = None if quote == character else (character if quote is None else quote)
        elif character == "#" and quote is None:
            return value[:index].rstrip(), " " + value[index:].strip()
    return value.strip(), ""


def _toml_update(path, mcpls_path):
    source = _read_toml_source(path)
    desired = {
        "command": mcpls_path,
        "args": ["--config", ".agents/mcpls.toml"],
        "cwd": "..",
        "enabled": True,
    }
    lines = source.splitlines(keepends=True)
    starts = []
    end = len(lines)
    for index, line in enumerate(lines):
        match = TABLE_RE.match(line.rstrip("\r\n"))
        if match and match.group(1).strip() == "mcp_servers.mcpls":
            starts.append(index)
    if len(starts) > 1:
        fail("{} has duplicate [mcp_servers.mcpls] tables; no changes made".format(path))
    start = starts[0] if starts else None
    if start is None:
        if re.search(r"(?m)^\s*mcp_servers(?:\.mcpls)?\s*=", source):
            fail("{} uses an unsupported inline mcp_servers table; no changes made".format(path))
        separator = "" if not source or source.endswith("\n\n") else ("\n" if source.endswith("\n") else "\n\n")
        block = ["[mcp_servers.mcpls]\n"]
        block.extend("{} = {}\n".format(key, _toml_literal(item)) for key, item in desired.items())
        return source + separator + "".join(block)
    for index in range(start + 1, len(lines)):
        if TABLE_RE.match(lines[index].rstrip("\r\n")):
            end = index
            break
    commands = []
    managed_counts = {key: 0 for key in desired}
    for line in lines[start + 1:end]:
        match = ASSIGNMENT_RE.match(line)
        if not match:
            continue
        key = match.group(2)
        if key in managed_counts:
            managed_counts[key] += 1
        if key != "command":
            continue
        raw, _ = _toml_value_and_comment(match.group(4))
        try:
            commands.append(json.loads(raw))
        except (TypeError, ValueError):
            if len(raw) >= 2 and raw[0] == raw[-1] == "'":
                commands.append(raw[1:-1])
            else:
                fail("{} has an invalid mcpls command value; no changes made".format(path))
    duplicates = [key for key, count in managed_counts.items() if count > 1]
    if duplicates:
        fail("{} has duplicate mcpls keys {}; no changes made".format(path, ", ".join(duplicates)))
    if not commands:
        fail("{} mcpls table has no command; no changes made".format(path))
    if not _is_mcpls_command(commands[0]):
        fail("{} has a foreign mcp_servers.mcpls entry; no changes made".format(path))
    seen = set()
    updated = list(lines[: start + 1])
    for line in lines[start + 1:end]:
        match = ASSIGNMENT_RE.match(line)
        if match and match.group(2) in desired:
            key = match.group(2)
            ending = match.group(5) or ""
            _, comment = _toml_value_and_comment(match.group(4))
            updated.append(
                "{}{}{}{}{}{}".format(
                    match.group(1), key, match.group(3), _toml_literal(desired[key]),
                    comment, ending,
                )
            )
            seen.add(key)
        else:
            updated.append(line)
    for key, item in desired.items():
        if key not in seen:
            updated.append("{} = {}\n".format(key, _toml_literal(item)))
    updated.extend(lines[end:])
    return "".join(updated)


def inspect_project(manifest, candidate):
    root = resolve_git_root(candidate)
    detected = detect_languages(root, manifest)
    harnesses = [
        harness_id
        for harness_id, harness in manifest["project_harnesses"].items()
        if (root / harness["path"]).is_file()
    ]
    mcpls = component_status(manifest["components"]["mcpls"])
    language_states = [language_server_status(server) for server in detected]
    return {
        "root": str(root),
        "languages": [server["id"] for server in detected],
        "harnesses": harnesses,
        "mcpls": mcpls,
        "language_servers": language_states,
    }, detected


def _preflight(manifest, report, detected):
    root = Path(report["root"])
    if not detected or not report["harnesses"]:
        return {}
    if report["mcpls"]["state"] != "ready":
        repair = " ".join(manifest["components"]["mcpls"]["repair_argv"])
        fail("mcpls {}: run {}; no changes made".format(report["mcpls"]["state"], repair))
    generated = root / ".agents" / "mcpls.toml"
    if generated.exists():
        try:
            current = generated.read_text(encoding="utf-8")
        except OSError as exc:
            fail("cannot read {}: {}".format(generated, exc))
        if not current.startswith(OWNER_MARKER + "\n"):
            fail("{} is not owned by $setup-project-mcpls; no changes made".format(generated))
    writes = {generated: render_mcpls_config(root, detected)}
    for harness_id in report["harnesses"]:
        path = root / manifest["project_harnesses"][harness_id]["path"]
        if harness_id == "root-mcp-json":
            writes[path] = _json_update(path, report["mcpls"]["path"])
        else:
            writes[path] = _toml_update(path, report["mcpls"]["path"])
    return writes


def setup_project(manifest, candidate):
    report, detected = inspect_project(manifest, candidate)
    writes = _preflight(manifest, report, detected)
    changed = []
    for path, content in writes.items():
        current = path.read_text(encoding="utf-8") if path.exists() else None
        if current != content:
            atomic_write(path, content)
            changed.append(str(path))
    report["changed"] = changed
    if not detected:
        report["action"] = "no supported stack detected; no files changed"
    elif not report["harnesses"]:
        report["action"] = "create mcp.json and/or .codex/config.toml, then rerun; no files changed"
    else:
        report["action"] = "configured" if changed else "already configured"
    return report


def verify_project(manifest, candidate, probe):
    report, detected = inspect_project(manifest, candidate)
    writes = _preflight(manifest, report, detected)
    if not writes:
        fail(report.get("action", "project has no supported stack or harness"))
    mismatches = []
    for path, expected in writes.items():
        actual = path.read_text(encoding="utf-8") if path.exists() else None
        if actual != expected:
            mismatches.append(str(path))
    if mismatches:
        fail("project configuration differs; run setup-project: {}".format(", ".join(mismatches)))
    probe(
        manifest,
        report["mcpls"]["path"],
        Path(report["root"]),
        Path(report["root"]) / ".agents" / "mcpls.toml",
        semantic_python="python" in report["languages"],
    )
    report["verified"] = True
    return report
