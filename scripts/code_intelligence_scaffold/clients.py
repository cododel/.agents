"""Removal-only adapters for legacy user-scoped mcpls registries."""

import json
from pathlib import Path
import plistlib
import shutil

from .common import LEGACY_CLIENT_IDS, expand_path, fail, run
from .jsonc import atomic_write, delete_path, get_path, nested_delete, nested_get, read_plain_json


def selected_client_ids(client_id):
    return LEGACY_CLIENT_IDS if client_id == "all" else (client_id,)


def _detect(delta):
    detection = delta["detection"]
    if detection["kind"] == "binary":
        binary = shutil.which(detection["value"])
        if binary:
            return True, binary
        if delta.get("adapter") == "opencode_jsonc":
            directory = expand_path(delta["directory"])
            return any((directory / name).exists() for name in delta["candidates"]), None
        configured = expand_path(delta["path"]) if "path" in delta else None
        return bool(configured and configured.exists()), None
    for raw_path in detection["paths"]:
        application = expand_path(raw_path)
        info_path = application / "Contents" / "Info.plist"
        if info_path.is_file():
            try:
                with info_path.open("rb") as stream:
                    if plistlib.load(stream).get("CFBundleIdentifier") == detection["bundle_id"]:
                        return True, str(application)
            except (OSError, plistlib.InvalidFileException):
                pass
    configured = expand_path(delta["path"]) if "path" in delta else None
    return bool(configured and configured.exists()), None


def _is_mcpls_entry(client_id, entry):
    if not isinstance(entry, dict):
        return False
    command = entry.get("command")
    if client_id == "codex":
        transport = entry.get("transport")
        command = transport.get("command") if isinstance(transport, dict) else None
    elif client_id == "opencode":
        argv = entry.get("command")
        command = argv[0] if isinstance(argv, list) and argv else None
    return isinstance(command, str) and Path(command).name == "mcpls"


def _native_entry(client_id):
    binary_name = {"codex": "codex", "grok": "grok"}[client_id]
    binary = shutil.which(binary_name)
    if not binary:
        return None, "skipped", "{} is not installed".format(binary_name), {}
    if client_id == "codex":
        completed = run([binary, "mcp", "get", "mcpls", "--json"], check=False)
        if completed.returncode != 0:
            listed = run([binary, "mcp", "list", "--json"], check=False)
            if listed.returncode != 0:
                return None, "unreadable", "Codex MCP registry cannot be listed", {}
            return None, "missing", None, {"binary": binary}
    else:
        completed = run([binary, "mcp", "list", "--json"], check=False)
        if completed.returncode != 0:
            return None, "unreadable", "Grok MCP registry cannot be listed", {}
    try:
        value = json.loads(completed.stdout)
    except ValueError as exc:
        return None, "unreadable", "invalid registry JSON: {}".format(exc), {}
    if client_id == "codex":
        return value, "present", None, {"binary": binary}
    matches = [
        item for item in value if isinstance(item, dict)
        and item.get("name") == "mcpls" and item.get("scope") == "user"
    ] if isinstance(value, list) else []
    if len(matches) > 1:
        return None, "unreadable", "duplicate user-scoped mcpls entries", {}
    if matches:
        return matches[0], "present", None, {"binary": binary}
    return None, "missing", None, {"binary": binary}


def _json_entry(delta):
    path = expand_path(delta["path"])
    if not path.exists():
        return None, "missing", None, {"path": path}
    try:
        value, _ = read_plain_json(path)
        found, entry = nested_get(value, delta["entry_path"])
    except Exception as exc:
        return None, "unreadable", str(exc), {"path": path}
    return entry, "present" if found else "missing", None, {"path": path}


def _opencode_entry(delta, binary):
    directory = expand_path(delta["directory"])
    paths = [directory / name for name in delta["candidates"]]
    path = next((item for item in paths if item.exists()), paths[0])
    if not path.exists():
        return None, "missing", None, {"path": path}
    try:
        source = path.read_text(encoding="utf-8")
        found_entries = []
        for major in ("1", "2"):
            entry_path = delta["entry_paths"][major]
            found, entry = get_path(source, entry_path)
            if found:
                found_entries.append((entry_path, entry))
    except Exception as exc:
        return None, "unreadable", str(exc), {"path": path}
    if len(found_entries) > 1:
        return None, "unreadable", "OpenCode config mixes v1/v2 mcpls paths", {"path": path}
    if found_entries:
        entry_path, entry = found_entries[0]
        return entry, "present", None, {"path": path, "source": source, "entry_path": entry_path}
    return None, "missing", None, {"path": path, "source": source}


def inspect_global(manifest, client_id):
    delta = manifest["legacy_global_registries"][client_id]
    detected, binary = _detect(delta)
    if not detected:
        return {"id": client_id, "state": "skipped", "detail": None, "entry": None, "metadata": {}}
    adapter = delta["adapter"]
    if adapter in ("codex_cli", "grok_cli"):
        entry, state, detail, metadata = _native_entry(client_id)
    elif adapter in ("json_file", "claude_cli"):
        entry, state, detail, metadata = _json_entry(delta)
        metadata["binary"] = binary
    else:
        entry, state, detail, metadata = _opencode_entry(delta, binary)
    if state == "present":
        state = "legacy" if _is_mcpls_entry(client_id, entry) else "conflict"
    return {"id": client_id, "state": state, "detail": detail, "entry": entry, "metadata": metadata}


def inspect_globals(manifest, client_id):
    return [inspect_global(manifest, selected) for selected in selected_client_ids(client_id)]


def _remove_native(client_id, metadata):
    binary = metadata.get("binary") or shutil.which({"codex": "codex", "grok": "grok"}[client_id])
    if not binary:
        fail("{} is unavailable; cannot remove its native registry entry".format(client_id))
    argv = [binary, "mcp", "remove", "mcpls"]
    if client_id == "grok":
        argv = [binary, "mcp", "remove", "--scope", "user", "mcpls"]
    run(argv, capture=False)


def remove_global(manifest, state):
    client_id = state["id"]
    if state["state"] in ("missing", "skipped"):
        print("{} global MCP mcpls is absent; no changes made.".format(client_id))
        return
    delta = manifest["legacy_global_registries"][client_id]
    adapter = delta["adapter"]
    if adapter in ("codex_cli", "grok_cli"):
        _remove_native(client_id, state["metadata"])
    elif adapter == "claude_cli" and state["metadata"].get("binary"):
        run([state["metadata"]["binary"], "mcp", "remove", "--scope", "user", "mcpls"], capture=False)
    elif adapter in ("json_file", "claude_cli"):
        path = state["metadata"]["path"]
        value, _ = read_plain_json(path)
        if nested_delete(value, delta["entry_path"]):
            atomic_write(path, json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    else:
        updated, changed = delete_path(state["metadata"]["source"], state["metadata"]["entry_path"])
        if changed:
            atomic_write(state["metadata"]["path"], updated)
    print("Removed only the {} global MCP mcpls entry; binaries were not removed.".format(client_id))


def unconfigure_globals(manifest, client_id, force):
    states = inspect_globals(manifest, client_id)
    unreadable = [state for state in states if state["state"] == "unreadable"]
    if unreadable:
        fail("cannot inspect global registries: {}".format(", ".join(
            "{} ({})".format(state["id"], state["detail"]) for state in unreadable
        )))
    conflicts = [state["id"] for state in states if state["state"] == "conflict"]
    if conflicts and not force:
        fail("foreign global entries named mcpls require --force: {}".format(", ".join(conflicts)))
    for state in states:
        remove_global(manifest, state)
