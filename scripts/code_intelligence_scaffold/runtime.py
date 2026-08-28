"""Direct MCP protocol and Python semantic verification."""

import json
import os
from pathlib import Path
import select
import signal
import subprocess
import time

from .common import fail


def send_message(process, payload):
    try:
        process.stdin.write(json.dumps(payload, separators=(",", ":")) + "\n")
        process.stdin.flush()
    except (BrokenPipeError, OSError) as exc:
        fail("MCP server closed stdin: {}".format(exc))


def receive_message(process, request_id, timeout=20.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        remaining = max(0.05, deadline - time.monotonic())
        readable, _, _ = select.select([process.stdout], [], [], remaining)
        if not readable:
            continue
        line = process.stdout.readline()
        if not line:
            break
        try:
            message = json.loads(line)
        except ValueError:
            continue
        if message.get("id") == request_id:
            return message
    fail("timed out waiting for MCP response {}".format(request_id))


def receive_response(process, request_id, timeout=20.0):
    message = receive_message(process, request_id, timeout)
    if "error" in message:
        fail("MCP request {} failed: {}".format(request_id, message["error"]))
    return message.get("result")


def call_tool_when_ready(process, name, arguments, request_id=3, timeout=30.0):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        send_message(process, {
            "jsonrpc": "2.0",
            "id": request_id,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        })
        remaining = max(0.05, deadline - time.monotonic())
        message = receive_message(process, request_id, min(20.0, remaining))
        if "error" not in message:
            return message.get("result")
        detail = message["error"]
        error_message = detail.get("message", "") if isinstance(detail, dict) else str(detail)
        if "still initializing" not in error_message.lower():
            fail("MCP request {} failed: {}".format(request_id, detail))
        request_id += 1
        time.sleep(min(0.5, max(0.0, deadline - time.monotonic())))
    fail("timed out waiting for {} after LSP initialization retries".format(name))


def signal_process(process, process_signal):
    try:
        os.killpg(process.pid, process_signal)
    except (PermissionError, ProcessLookupError):
        pass
    if process.poll() is None:
        try:
            process.send_signal(process_signal)
        except (PermissionError, ProcessLookupError):
            pass


def stop_process_group(process):
    process_group = process.pid
    signal_process(process, signal.SIGTERM)
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        signal_process(process, signal.SIGKILL)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            fail("mcpls verification process group did not terminate")
    deadline = time.monotonic() + 2
    while time.monotonic() < deadline:
        try:
            os.killpg(process_group, 0)
        except ProcessLookupError:
            return
        except PermissionError:
            fail("cannot confirm mcpls verification process-group cleanup")
        time.sleep(0.05)
    fail("mcpls child process survived verification cleanup")


def _python_source(project):
    ignored = {".git", ".venv", "venv", "node_modules", "target", "dist", "build"}
    for path in sorted(project.rglob("*.py")):
        if not any(part in ignored for part in path.relative_to(project).parts):
            return path
    fail("Python semantic smoke requested but no Python source exists")


def mcp_probe(manifest, mcpls_path, project, config_path, semantic_python=False):
    source = _python_source(project) if semantic_python else None
    with open(os.devnull, "w", encoding="utf-8") as stderr_file:
        try:
            process = subprocess.Popen(
                [mcpls_path, "--config", str(config_path.resolve())],
                cwd=str(project),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=stderr_file,
                text=True,
                bufsize=1,
                start_new_session=True,
            )
        except OSError as exc:
            fail("cannot start mcpls verification probe: {}".format(exc))
        try:
            send_message(process, {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "agents-code-intelligence-verify", "version": "3"},
                },
            })
            receive_response(process, 1)
            send_message(process, {
                "jsonrpc": "2.0", "method": "notifications/initialized", "params": {},
            })
            send_message(process, {
                "jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {},
            })
            tools_result = receive_response(process, 2)
            if not isinstance(tools_result, dict):
                fail("MCP tools/list returned a non-object result")
            tools = {
                tool.get("name")
                for tool in tools_result.get("tools", [])
                if isinstance(tool, dict)
            }
            missing = sorted(set(manifest["expected_mcp_tools"]) - tools)
            if missing:
                fail("MCP tools/list is missing expected tools: {}".format(", ".join(missing)))
            if source is not None:
                smoke = call_tool_when_ready(
                    process, "get_document_symbols", {"file_path": str(source.resolve())}
                )
                if not isinstance(smoke, dict) or smoke.get("isError") is True:
                    fail("Python get_document_symbols semantic smoke failed")
        finally:
            try:
                process.stdin.close()
            except (BrokenPipeError, OSError):
                pass
            stop_process_group(process)
