"""Command-line orchestration for the code-intelligence scaffold."""

import argparse
import json
import sys

from .clients import (
    MCP_CLIENTS,
    RESTART_CLIENTS,
    configure_client,
    inspect_clients,
    required_components,
    unconfigure_client,
    verify_grok_doctor,
)
from .common import (
    CLIENT_IDS,
    ScaffoldError,
    component_status,
    ensure_platform,
    fail,
    install_components,
    language_server_status,
    read_manifest,
)
from .runtime import mcp_probe


def format_language_server_warning(warning):
    suffix = ""
    if warning["repair_argv"]:
        suffix = "; fix: {}".format(" ".join(warning["repair_argv"]))
    return "warning: language server {} is {} (not auto-installed{})".format(
        warning["id"], warning["state"], suffix
    )


def _component_statuses(manifest, names):
    return {
        name: component_status(name, manifest["components"][name])
        for name in names
    }


def _language_warnings(manifest, states):
    if not any(state["detected"] and state["id"] in MCP_CLIENTS for state in states):
        return []
    return [
        status
        for status in (language_server_status(server) for server in manifest["language_servers"])
        if status["state"] != "ready"
    ]


def build_plan(manifest, client_id):
    ensure_platform(manifest)
    initial_components = {
        name: component_status(name, value) for name, value in manifest["components"].items()
    }
    states = inspect_clients(manifest, client_id, initial_components["mcpls"]["path"])
    required = required_components(manifest, states)
    components = {name: initial_components[name] for name in required}
    actions = [
        {"kind": "component", "name": name, "state": status["state"]}
        for name, status in components.items()
        if status["state"] != "ready"
    ]
    for state in states:
        if state["state"] in ("missing", "conflict", "unreadable"):
            action = {
                "kind": "client-delta", "client": state["id"],
                "name": "mcpls", "state": state["state"],
            }
            if state["state"] == "unreadable" and state["detail"]:
                action["detail"] = state["detail"]
            actions.append(action)
        elif state["state"] == "skipped" and client_id != "all":
            actions.append({"kind": "client", "client": state["id"], "state": "missing"})
    clients = [
        {
            "id": state["id"], "detected": state["detected"],
            "mode": state["mode"], "state": state["state"],
        }
        for state in states
    ]
    return {
        "platform": sys.platform,
        "actions": actions,
        "warnings": _language_warnings(manifest, states),
        "clients": clients,
    }


def print_plan(plan, as_json):
    if as_json:
        print(json.dumps(plan, indent=2, sort_keys=True))
        return
    if not plan["actions"]:
        print("No capability or selected client deltas are required.")
    for action in plan["actions"]:
        if action["kind"] == "component":
            print("component {}: {}".format(action["name"], action["state"]))
        elif action["kind"] == "client-delta":
            line = "client-delta {}/{}: {}".format(
                action["client"], action["name"], action["state"]
            )
            if action.get("detail"):
                line += " ({})".format(action["detail"])
            print(line)
        else:
            print("client {}: {}".format(action["client"], action["state"]))
    for client in plan["clients"]:
        print("client {}: {}".format(client["id"], client["state"]))
    for warning in plan["warnings"]:
        print(format_language_server_warning(warning))


def _preflight_states(states, client_id, allow_conflicts=False, conflict_flag="--replace"):
    if client_id != "all" and states[0]["state"] == "skipped":
        fail("client {} is not installed; no changes made".format(client_id))
    detected = [state for state in states if state["detected"]]
    if not detected:
        fail("no selected clients were detected; no changes made")
    unreadable = [state for state in detected if state["state"] == "unreadable"]
    if unreadable:
        descriptions = [
            "{} ({})".format(state["id"], state["detail"] or "unknown registry error")
            for state in unreadable
        ]
        fail("cannot inspect client deltas: {}".format(", ".join(descriptions)))
    conflicts = [state["id"] for state in detected if state["state"] == "conflict"]
    if conflicts and not allow_conflicts:
        fail("client MCP conflicts require {}: {}".format(
            conflict_flag, ", ".join(conflicts)
        ))
    return detected


def apply_capability(manifest, client_id, install, replace):
    ensure_platform(manifest)
    initial_components = {
        name: component_status(name, value) for name, value in manifest["components"].items()
    }
    states = inspect_clients(manifest, client_id, initial_components["mcpls"]["path"])
    detected = _preflight_states(states, client_id, allow_conflicts=replace)
    required = required_components(manifest, detected)
    statuses = {name: initial_components[name] for name in required}
    unavailable = [name for name, status in statuses.items() if status["state"] != "ready"]
    if unavailable and not install:
        fail("components require installation or update: {}; rerun with --install".format(
            ", ".join(unavailable)
        ))
    if unavailable:
        install_components(manifest, statuses)
        statuses = _component_statuses(manifest, required)
        unavailable = [name for name, status in statuses.items() if status["state"] != "ready"]
        if unavailable:
            fail("components are still unavailable after installation: {}".format(
                ", ".join(unavailable)
            ))
    mcpls_path = statuses.get("mcpls", {}).get("path")
    states = inspect_clients(manifest, client_id, mcpls_path)
    detected = _preflight_states(states, client_id, allow_conflicts=replace)
    for state in detected:
        configure_client(manifest, state, mcpls_path, replace)


def unconfigure(manifest, client_id, force):
    ensure_platform(manifest)
    states = inspect_clients(manifest, client_id, None)
    detected = _preflight_states(
        states, client_id, allow_conflicts=force, conflict_flag="--force"
    )
    for state in detected:
        unconfigure_client(manifest, state)


def verify(manifest, client_id):
    ensure_platform(manifest)
    initial_states = inspect_clients(manifest, client_id, None)
    detected = _preflight_states(initial_states, client_id)
    required = required_components(manifest, detected)
    statuses = _component_statuses(manifest, required)
    bad = [name for name, status in statuses.items() if status["state"] != "ready"]
    if bad:
        fail("component verification failed: {}".format(", ".join(bad)))
    mcpls_path = statuses.get("mcpls", {}).get("path")
    states = inspect_clients(manifest, client_id, mcpls_path)
    detected = _preflight_states(states, client_id)
    mismatched = [state["id"] for state in detected if state["state"] not in (
        "ready", "lsp_unsupported",
    )]
    if mismatched:
        fail("client MCP verification failed: {}".format(", ".join(mismatched)))
    mcp_states = [state for state in detected if state["id"] in MCP_CLIENTS]
    warnings = []
    if mcp_states:
        for server in manifest["language_servers"]:
            status = language_server_status(server)
            if status["state"] == "ready":
                continue
            if server["semantic_smoke"]:
                fail("required semantic smoke server {} is {}".format(
                    server["id"], status["state"]
                ))
            warnings.append(status)
        if any(state["id"] == "grok" for state in mcp_states):
            verify_grok_doctor()
        mcp_probe(manifest, mcpls_path)
        print("Verified components, exact client registries, MCP handshake/tools, and Python semantic smoke.")
    else:
        print("Verified Pi shared rules/AST mode; LSP remains unsupported by policy.")
    for state in mcp_states:
        if state["id"] in RESTART_CLIENTS:
            print("note: restart {} or start a new session to load the MCP delta.".format(state["id"]))
    for warning in warnings:
        print(format_language_server_warning(warning))


def parser():
    root = argparse.ArgumentParser(
        description="Validate and scaffold the code-intelligence capability for supported clients."
    )
    subparsers = root.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="validate manifest and tracked configuration")
    choices = list(CLIENT_IDS) + ["all"]
    plan_parser = subparsers.add_parser("plan", help="show missing or conflicting deltas")
    plan_parser.add_argument("--client", choices=choices, required=True)
    plan_parser.add_argument("--json", action="store_true")
    apply_parser = subparsers.add_parser("apply", help="install explicitly and configure clients")
    apply_parser.add_argument("--client", choices=choices, required=True)
    apply_parser.add_argument("--install", action="store_true")
    apply_parser.add_argument("--replace", action="store_true")
    verify_parser = subparsers.add_parser("verify", help="verify tools, client deltas, and MCP semantics")
    verify_parser.add_argument("--client", choices=choices, required=True)
    remove_parser = subparsers.add_parser("unconfigure", help="remove only client MCP entries")
    remove_parser.add_argument("--client", choices=choices, required=True)
    remove_parser.add_argument("--force", action="store_true")
    return root


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        manifest = read_manifest()
        if args.command == "validate":
            print("code-intelligence manifest and tracked configuration are valid.")
        elif args.command == "plan":
            print_plan(build_plan(manifest, args.client), args.json)
        elif args.command == "apply":
            apply_capability(manifest, args.client, args.install, args.replace)
        elif args.command == "verify":
            verify(manifest, args.client)
        elif args.command == "unconfigure":
            unconfigure(manifest, args.client, args.force)
        return 0
    except ScaffoldError as exc:
        print("error: {}".format(exc), file=sys.stderr)
        return 2
