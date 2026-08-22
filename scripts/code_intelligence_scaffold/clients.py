"""Client detection, registry inspection, and scoped MCP configuration."""

import json
from pathlib import Path
import plistlib
import shutil

from .common import (
    CLIENT_IDS,
    ScaffoldError,
    desired_command,
    expand_path,
    fail,
    parse_version,
    run,
)
from .jsonc import (
    atomic_write,
    delete_path,
    get_path,
    nested_delete,
    nested_get,
    nested_set,
    parse,
    read_plain_json,
    set_path,
)


MCP_CLIENTS = tuple(client_id for client_id in CLIENT_IDS if client_id != "pi")
RESTART_CLIENTS = {"antigravity", "kimi-code", "opencode"}


def selected_client_ids(client_id):
    return CLIENT_IDS if client_id == "all" else (client_id,)


def detect_client(delta):
    detection = delta["detection"]
    if detection["kind"] == "binary":
        path = shutil.which(detection["value"])
        return (path is not None), path
    expected_id = detection["bundle_id"]
    for raw_path in detection["paths"]:
        application = expand_path(raw_path)
        info_path = application / "Contents" / "Info.plist"
        if not info_path.is_file():
            continue
        try:
            with info_path.open("rb") as stream:
                info = plistlib.load(stream)
        except (OSError, plistlib.InvalidFileException):
            continue
        if info.get("CFBundleIdentifier") == expected_id:
            return True, str(application)
    return False, None


def _command_matches(command, mcpls_path):
    if not isinstance(command, str) or not Path(command).is_absolute():
        return False
    if mcpls_path is None:
        return Path(command).name == "mcpls"
    return command == str(Path(mcpls_path).resolve())


def desired_entry(manifest, client_id, mcpls_path, major=None):
    command, args = desired_command(manifest, client_id, mcpls_path)
    if client_id == "codex":
        return {
            "name": "mcpls",
            "enabled": True,
            "transport": {
                "type": "stdio", "command": command, "args": args,
                "env": None, "env_vars": [], "cwd": None,
            },
            "enabled_tools": None,
            "disabled_tools": None,
            "startup_timeout_sec": None,
            "tool_timeout_sec": None,
        }
    if client_id == "grok":
        return {
            "command": command, "args": args, "enabled": True,
            "name": "mcpls", "scope": "user",
        }
    if client_id == "claude-code":
        return {"type": "stdio", "command": command, "args": args, "env": {}}
    if client_id in ("antigravity", "kimi-code"):
        return {"command": command, "args": args}
    if client_id == "opencode":
        entry = {"type": "local", "command": [command] + args}
        if major == 1:
            entry["enabled"] = True
        return entry
    fail("{} has no MCP entry shape".format(client_id))


def entry_matches(manifest, client_id, entry, mcpls_path, major=None):
    if not isinstance(entry, dict):
        return False
    if client_id == "codex":
        transport = entry.get("transport")
        if not isinstance(transport, dict) or not _command_matches(transport.get("command"), mcpls_path):
            return False
        normalized = {
            "name": entry.get("name"),
            "enabled": entry.get("enabled"),
            "transport": {
                "type": transport.get("type"),
                "command": transport.get("command"),
                "args": transport.get("args", []),
                "env": transport.get("env"),
                "env_vars": transport.get("env_vars", []),
                "cwd": transport.get("cwd"),
            },
            "enabled_tools": entry.get("enabled_tools"),
            "disabled_tools": entry.get("disabled_tools"),
            "startup_timeout_sec": entry.get("startup_timeout_sec"),
            "tool_timeout_sec": entry.get("tool_timeout_sec"),
        }
        expected = desired_entry(manifest, client_id, transport["command"])
        return normalized == expected
    command = entry.get("command")
    if client_id == "opencode":
        command_argv = entry.get("command")
        if not isinstance(command_argv, list) or not command_argv:
            return False
        command = command_argv[0]
    if not _command_matches(command, mcpls_path):
        return False
    expected = desired_entry(manifest, client_id, command, major)
    return entry == expected


def _codex_entry(name):
    codex = shutil.which("codex")
    completed = run([codex, "mcp", "get", name, "--json"], check=False)
    if completed.returncode == 0:
        try:
            return json.loads(completed.stdout), "present", None
        except ValueError as exc:
            return None, "unreadable", "invalid Codex JSON: {}".format(exc)
    listed = run([codex, "mcp", "list", "--json"], check=False)
    if listed.returncode != 0:
        return None, "unreadable", "Codex MCP registry cannot be listed"
    try:
        entries = json.loads(listed.stdout)
    except ValueError as exc:
        return None, "unreadable", "invalid Codex list JSON: {}".format(exc)
    if isinstance(entries, list) and not any(
        isinstance(item, dict) and item.get("name") == name for item in entries
    ):
        return None, "missing", None
    return None, "unreadable", "Codex MCP entry cannot be inspected"


def _grok_entry(name):
    grok = shutil.which("grok")
    completed = run([grok, "mcp", "list", "--json"], check=False)
    if completed.returncode != 0:
        return None, "unreadable", "Grok MCP registry cannot be listed"
    try:
        entries = json.loads(completed.stdout)
    except ValueError as exc:
        return None, "unreadable", "invalid Grok list JSON: {}".format(exc)
    if not isinstance(entries, list):
        return None, "unreadable", "Grok MCP list is not an array"
    matches = [
        item for item in entries
        if isinstance(item, dict) and item.get("name") == name and item.get("scope") == "user"
    ]
    if not matches:
        return None, "missing", None
    if len(matches) != 1:
        return None, "unreadable", "Grok has duplicate user-scoped mcpls entries"
    return matches[0], "present", None


def _claude_entry(delta, name):
    path = expand_path(delta["inspect_path"])
    if not path.exists():
        return None, "missing", None, {"path": path}
    try:
        raw = path.read_text(encoding="utf-8")
        value = json.loads(raw)
    except (OSError, ValueError) as exc:
        return None, "unreadable", "cannot read Claude user config: {}".format(exc), {"path": path}
    if not isinstance(value, dict):
        return None, "unreadable", "Claude user config is not an object", {"path": path}
    servers = value.get("mcpServers", {})
    if not isinstance(servers, dict):
        return None, "unreadable", "Claude mcpServers is not an object", {"path": path}
    if name not in servers:
        return None, "missing", None, {"path": path}
    return servers[name], "present", None, {"path": path}


def _plain_json_entry(delta):
    path = expand_path(delta["config"]["path"])
    value, _ = read_plain_json(path)
    found, entry = nested_get(value, delta["config"]["entry_path"])
    state = "present" if found else "missing"
    return entry, state, None, {"path": path}


def _opencode_major(binary):
    completed = run([binary, "--version"], check=False)
    version = parse_version((completed.stdout or "") + "\n" + (completed.stderr or ""))
    if completed.returncode != 0 or version is None or version[0] not in (1, 2):
        fail("OpenCode version must resolve to supported major 1 or 2")
    return version[0]


def _opencode_path(delta):
    directory = expand_path(delta["config"]["directory"])
    candidates = [directory / name for name in delta["config"]["candidates"]]
    return next((path for path in candidates if path.exists()), candidates[0])


def _opencode_entry(delta, binary):
    major = _opencode_major(binary)
    path = _opencode_path(delta)
    if not path.exists():
        return None, "missing", None, {"path": path, "major": major, "source": "{}\n"}
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, "unreadable", "cannot read OpenCode config: {}".format(exc), {"path": path, "major": major}
    if not source.strip():
        source = "{}\n"
    try:
        parse(source)
        desired_path = delta["config"]["entry_paths"][str(major)]
        other_path = delta["config"]["entry_paths"]["2" if major == 1 else "1"]
        other_found, _ = get_path(source, other_path)
        found, entry = get_path(source, desired_path)
    except ScaffoldError as exc:
        return None, "unreadable", str(exc), {"path": path, "major": major, "source": source}
    if other_found:
        return entry, "unreadable", "OpenCode config mixes v1/v2 mcpls paths", {
            "path": path, "major": major, "source": source,
        }
    return entry, "present" if found else "missing", None, {
        "path": path, "major": major, "source": source,
    }


def inspect_client(manifest, client_id, mcpls_path=None):
    delta = manifest["client_deltas"][client_id]
    detected, location = detect_client(delta)
    mode = delta["type"]
    if not detected:
        return {
            "id": client_id, "detected": False, "mode": mode, "state": "skipped",
            "location": None, "detail": None, "entry": None, "metadata": {},
        }
    if mode == "rules_ast_only":
        return {
            "id": client_id, "detected": True, "mode": mode, "state": "lsp_unsupported",
            "location": location, "detail": delta["reason"], "entry": None, "metadata": {},
        }
    try:
        adapter = delta["adapter"]
        if adapter == "codex_cli":
            entry, state, detail = _codex_entry("mcpls")
            metadata = {}
        elif adapter == "grok_cli":
            entry, state, detail = _grok_entry("mcpls")
            metadata = {}
        elif adapter == "claude_cli":
            entry, state, detail, metadata = _claude_entry(delta, "mcpls")
        elif adapter == "json_file":
            entry, state, detail, metadata = _plain_json_entry(delta)
        elif adapter == "opencode_jsonc":
            entry, state, detail, metadata = _opencode_entry(delta, location)
        else:
            fail("unknown client adapter {}".format(adapter))
        major = metadata.get("major")
        if state == "present":
            state = "ready" if entry_matches(
                manifest, client_id, entry, mcpls_path, major
            ) else "conflict"
        return {
            "id": client_id, "detected": True, "mode": mode, "state": state,
            "location": location, "detail": detail, "entry": entry, "metadata": metadata,
        }
    except ScaffoldError as exc:
        return {
            "id": client_id, "detected": True, "mode": mode, "state": "unreadable",
            "location": location, "detail": str(exc), "entry": None, "metadata": {},
        }


def inspect_clients(manifest, client_id, mcpls_path=None):
    return [
        inspect_client(manifest, selected, mcpls_path)
        for selected in selected_client_ids(client_id)
    ]


def required_components(manifest, states):
    required = []
    for state in states:
        if not state["detected"]:
            continue
        for component in manifest["client_deltas"][state["id"]]["required_components"]:
            if component not in required:
                required.append(component)
    return required


def _remove_native(client_id):
    binary = shutil.which({"codex": "codex", "grok": "grok", "claude-code": "claude"}[client_id])
    if client_id == "codex":
        argv = [binary, "mcp", "remove", "mcpls"]
    else:
        argv = [binary, "mcp", "remove", "--scope", "user", "mcpls"]
    run(argv, capture=False)


def _add_native(client_id, command, args):
    binary = shutil.which({"codex": "codex", "grok": "grok", "claude-code": "claude"}[client_id])
    if client_id == "codex":
        argv = [binary, "mcp", "add", "mcpls", "--", command] + args
    else:
        argv = [binary, "mcp", "add", "--scope", "user", "mcpls", "--", command] + args
    run(argv, capture=False)


def configure_client(manifest, state, mcpls_path, replace):
    client_id = state["id"]
    if state["mode"] == "rules_ast_only":
        print("Pi uses shared rules and AST tooling; no MCP entry was changed.")
        return
    if state["state"] == "ready":
        print("{} MCP mcpls is already configured; no changes made.".format(client_id))
        return
    if state["state"] == "conflict" and not replace:
        fail("{} MCP mcpls conflicts with the capability; rerun with --replace".format(client_id))
    if state["state"] not in ("missing", "conflict"):
        fail("cannot configure {} from state {}".format(client_id, state["state"]))
    command, args = desired_command(manifest, client_id, mcpls_path)
    if client_id in ("codex", "grok", "claude-code"):
        if state["state"] == "conflict":
            _remove_native(client_id)
        _add_native(client_id, command, args)
    elif client_id in ("antigravity", "kimi-code"):
        delta = manifest["client_deltas"][client_id]
        path = expand_path(delta["config"]["path"])
        value, _ = read_plain_json(path)
        nested_set(value, delta["config"]["entry_path"], desired_entry(manifest, client_id, mcpls_path))
        atomic_write(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    elif client_id == "opencode":
        metadata = state["metadata"]
        source = metadata.get("source", "{}\n")
        path = metadata["path"]
        major = metadata["major"]
        entry_path = manifest["client_deltas"][client_id]["config"]["entry_paths"][str(major)]
        updated = set_path(source, entry_path, desired_entry(manifest, client_id, mcpls_path, major))
        atomic_write(path, updated)
    print("Configured {} MCP mcpls.".format(client_id))


def unconfigure_client(manifest, state):
    client_id = state["id"]
    if state["mode"] == "rules_ast_only":
        print("Pi has no MCP entry; no changes made.")
        return
    if state["state"] == "missing":
        print("{} MCP mcpls is absent; no changes made.".format(client_id))
        return
    if client_id in ("codex", "grok", "claude-code"):
        _remove_native(client_id)
    elif client_id in ("antigravity", "kimi-code"):
        delta = manifest["client_deltas"][client_id]
        path = expand_path(delta["config"]["path"])
        value, _ = read_plain_json(path)
        if nested_delete(value, delta["config"]["entry_path"]):
            atomic_write(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    elif client_id == "opencode":
        metadata = state["metadata"]
        entry_path = manifest["client_deltas"][client_id]["config"]["entry_paths"][
            str(metadata["major"])
        ]
        updated, changed = delete_path(metadata["source"], entry_path)
        if changed:
            atomic_write(metadata["path"], updated)
    print("Removed only the {} MCP mcpls entry; binaries were not removed.".format(client_id))


def verify_grok_doctor():
    grok = shutil.which("grok")
    completed = run([grok, "mcp", "doctor", "mcpls", "--json"], check=False)
    if completed.returncode != 0:
        fail("Grok MCP doctor failed")
    try:
        result = json.loads(completed.stdout)
    except ValueError as exc:
        fail("Grok MCP doctor returned invalid JSON: {}".format(exc))
    servers = result.get("servers") if isinstance(result, dict) else None
    matching = [item for item in servers or [] if isinstance(item, dict) and item.get("name") == "mcpls"]
    if len(matching) != 1 or matching[0].get("healthy") is not True:
        fail("Grok MCP doctor does not report a healthy mcpls server")
