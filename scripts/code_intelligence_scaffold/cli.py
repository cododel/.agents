"""Command-line orchestration for project-scoped code intelligence."""

import argparse
import json
import sys

from .clients import unconfigure_globals
from .common import LEGACY_CLIENT_IDS, ScaffoldError, ensure_platform, read_manifest
from .project import inspect_project, setup_project, verify_project
from .runtime import mcp_probe


def _print_report(report, as_json):
    if as_json:
        print(json.dumps(report, indent=2, sort_keys=True))
        return
    print("project: {}".format(report["root"]))
    print("stacks: {}".format(", ".join(report["languages"]) or "none"))
    print("harnesses: {}".format(", ".join(report["harnesses"]) or "none"))
    print("mcpls: {}".format(report["mcpls"]["state"]))
    for state in report["language_servers"]:
        if state["state"] == "ready":
            continue
        print("warning: {} LSP is {}; repair: {}".format(
            state["id"], state["state"], " ".join(state["repair_argv"])
        ))
    for changed in report.get("changed", []):
        print("changed: {}".format(changed))
    if report.get("action"):
        print("action: {}".format(report["action"]))
    if report.get("verified"):
        print("verified: exact project config, MCP handshake/tools, semantic smoke when applicable")
    if "codex" in report["harnesses"]:
        print("note: Codex loads project config only for trusted projects; start a new task after changes.")


def parser():
    root = argparse.ArgumentParser(
        description="Validate and configure mcpls only for an explicit Git project."
    )
    subparsers = root.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="validate the project-scoped capability manifest")
    for name, help_text in (
        ("inspect-project", "inspect stack, harness, and binary readiness without writes"),
        ("setup-project", "configure existing supported harnesses for one Git checkout"),
        ("verify-project", "verify exact config and run an MCP semantic smoke"),
    ):
        subparser = subparsers.add_parser(name, help=help_text)
        subparser.add_argument("--root", required=True)
        subparser.add_argument("--json", action="store_true")
    remove = subparsers.add_parser(
        "unconfigure-global", help="remove only legacy user-scoped mcpls registrations"
    )
    remove.add_argument("--client", choices=list(LEGACY_CLIENT_IDS) + ["all"], required=True)
    remove.add_argument("--force", action="store_true")
    return root


def main(argv=None):
    args = parser().parse_args(argv)
    try:
        manifest = read_manifest()
        ensure_platform(manifest)
        if args.command == "validate":
            print("code-intelligence project-scoped manifest is valid.")
        elif args.command == "inspect-project":
            report, _ = inspect_project(manifest, args.root)
            _print_report(report, args.json)
        elif args.command == "setup-project":
            _print_report(setup_project(manifest, args.root), args.json)
        elif args.command == "verify-project":
            _print_report(verify_project(manifest, args.root, mcp_probe), args.json)
        elif args.command == "unconfigure-global":
            unconfigure_globals(manifest, args.client, args.force)
        return 0
    except ScaffoldError as exc:
        print("error: {}".format(exc), file=sys.stderr)
        return 2
