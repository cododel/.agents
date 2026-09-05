#!/usr/bin/env python3
"""Stage Graphify outputs and merge only manifest-bound results (standard library only)."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import uuid

from run_validation import validate_extraction, validate_graph

# These are the only artifacts this helper may replace. Exports outside this set are separate actions.
OUTPUTS = ("cache", "GRAPH_REPORT.md", "graph.html", "manifest.json", "cost.json",
           ".graphify_root", ".graphify_python", ".graphify_labels.json", "graph.json")


def read_json(path: Path) -> dict:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"expected regular JSON file: {path}")
    result = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(result, dict):
        raise ValueError(f"expected JSON object: {path}")
    return result


def digest(path: Path) -> str | None:
    if path.is_symlink():
        raise ValueError(f"symlink is not a run artifact: {path}")
    if not path.exists():
        return None
    if path.is_dir():
        return fingerprint({str(child.relative_to(path)): digest(child)
                            for child in sorted(path.rglob("*")) if not child.is_dir() or child.is_symlink()})
    if not path.is_file():
        raise ValueError(f"expected regular file: {path}")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fingerprint(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, allow_nan=False).encode()).hexdigest()


def write_json(path: Path, value: object) -> None:
    temporary = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex)
    try:
        temporary.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n", encoding="utf-8")
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def copy_artifact(source: Path, target: Path) -> None:
    if source.is_dir():
        shutil.copytree(source, target)
    else:
        shutil.copy2(source, target)


def begin(output: Path) -> Path:
    if output.is_symlink():
        raise ValueError("output must not be a symlink")
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    baseline = {name: digest(output / name) for name in OUTPUTS}
    runs = output / ".runs"
    if runs.is_symlink():
        raise ValueError("run directory must not be a symlink")
    run = runs / uuid.uuid4().hex
    staged = run / "work" / "graphify-out"
    staged.mkdir(parents=True)
    (run / "chunks").mkdir()
    (run / "backup").mkdir()
    for name, checksum in baseline.items():
        if checksum is not None:
            copy_artifact(output / name, run / "backup" / name)
    # Only seed state required by incremental detection and shrink protection, not old reports.
    for name in ("graph.json", "manifest.json", "cost.json", "cache"):
        if baseline[name] is not None:
            copy_artifact(run / "backup" / name, staged / name)
    write_json(run / "state.json", {"run_id": run.name, "output": str(output),
                                   "baseline": baseline, "status": "started"})
    return run


def state_for(run: Path) -> dict:
    if run.is_symlink():
        raise ValueError("run must not be a symlink")
    run = run.resolve()
    state = read_json(run / "state.json")
    if state.get("run_id") != run.name or Path(state.get("output", "")) / ".runs" != run.parent:
        raise ValueError("run identity/path mismatch")
    if state.get("baseline", {}).keys() != set(OUTPUTS):
        raise ValueError("invalid output baseline")
    return state


def prepare(run: Path, plan_path: Path) -> dict:
    state = state_for(run)
    if state["status"] != "started":
        raise ValueError("plan is immutable; begin a new run to change it")
    plan = read_json(plan_path)
    sources, chunks, parameters = plan.get("sources"), plan.get("chunks"), plan.get("parameters")
    if not isinstance(sources, list) or not isinstance(chunks, list) or not isinstance(parameters, dict):
        raise ValueError("plan requires sources[], chunks[][], parameters{}")
    if not all(isinstance(p, str) and Path(p).is_absolute() for p in sources):
        raise ValueError("sources must be absolute file paths")
    if len(set(sources)) != len(sources):
        raise ValueError("duplicate source path")
    hashes = {p: digest(Path(p)) for p in sources}
    if None in hashes.values():
        raise ValueError("source missing during preparation")
    assigned = []
    for chunk in chunks:
        if not isinstance(chunk, list) or not chunk or not all(isinstance(p, str) and p in hashes for p in chunk):
            raise ValueError("each chunk must contain known source paths")
        assigned.extend(chunk)
    if len(set(assigned)) != len(assigned):
        raise ValueError("source assigned to multiple chunks")
    reads = plan.get("read_paths", {})
    if not isinstance(reads, dict) or not all(isinstance(k, str) and isinstance(v, str)
                                              and k in hashes and v in hashes for k, v in reads.items()):
        raise ValueError("read_paths must map fingerprinted originals to fingerprinted derived files")
    if any(p in reads.values() for p in assigned):
        raise ValueError("chunks must use stable originals, not derived reading paths")
    if any(Path(p).is_relative_to(run.resolve()) for p in assigned):
        raise ValueError("chunk source identity must not reference a temporary run")
    manifest = {"sources": hashes, "parameters": parameters, "chunks": chunks, "read_paths": reads}
    state.update(status="prepared", manifest=manifest, fingerprint=fingerprint(manifest),
                 plan_path=str(plan_path.resolve()), plan_digest=digest(plan_path))
    write_json(run / "state.json", state)
    return state


def verify_inputs(state: dict) -> None:
    if digest(Path(state.get("plan_path", ""))) != state.get("plan_digest"):
        raise ValueError("plan parameters changed since preparation")
    manifest = state.get("manifest")
    if not isinstance(manifest, dict) or fingerprint(manifest) != state.get("fingerprint"):
        raise ValueError("manifest changed or run not prepared")
    for source, checksum in manifest["sources"].items():
        if digest(Path(source)) != checksum:
            raise ValueError(f"source changed since preparation: {source}")


def merge(run: Path) -> dict:
    state = state_for(run)
    if state["status"] not in ("prepared", "merged"):
        raise ValueError("run is not mergeable")
    verify_inputs(state)
    merged = {"nodes": [], "edges": [], "hyperedges": [], "input_tokens": 0, "output_tokens": 0}
    receipts = {}
    for index, sources in enumerate(state["manifest"]["chunks"]):
        name = f"chunk-{index:04d}.json"
        path = run / "chunks" / name
        envelope = read_json(path)
        if (envelope.get("run_id"), envelope.get("chunk_id"), envelope.get("fingerprint")) != (
                state["run_id"], index, state["fingerprint"]):
            raise ValueError(f"foreign or stale chunk: {name}")
        extraction = validate_extraction(envelope.get("extraction"), sources)
        for key in ("nodes", "edges", "hyperedges"):
            merged[key].extend(extraction.get(key, []))
        for key in ("input_tokens", "output_tokens"):
            merged[key] += extraction.get(key, 0)
        receipts[name] = digest(path)
    # Nothing is written until every expected chunk and current source has passed validation.
    verify_inputs(state)
    write_json(run / "work/graphify-out/.graphify_semantic_new.json", merged)
    state.update(status="merged", receipts=receipts)
    write_json(run / "state.json", state)
    return merged


def publish(run: Path) -> None:
    state = state_for(run)
    if state["status"] != "merged":
        raise ValueError("merge all expected chunks before publication")
    verify_inputs(state)
    for name, checksum in state["receipts"].items():
        if digest(run / "chunks" / name) != checksum:
            raise ValueError(f"chunk changed after merge: {name}")
    staged = run / "work/graphify-out"
    graph = read_json(staged / "graph.json")
    validate_graph(graph)
    validate_extraction(read_json(staged / ".graphify_extract.json"))
    report = staged / "GRAPH_REPORT.md"
    if digest(report) is None or not report.read_text(encoding="utf-8").strip():
        raise ValueError("missing graph report")
    names = [name for name in OUTPUTS if digest(staged / name) is not None]
    # Parse state files before replacing any published content.
    for name in names:
        if name.endswith(".json"):
            read_json(staged / name)
    output = Path(state["output"])
    lock = output / ".publish-lock"
    try:
        lock.mkdir()
    except FileExistsError as error:
        raise ValueError("publication locked; inspect interrupted run before retrying") from error
    try:
        for name, checksum in state["baseline"].items():
            if digest(output / name) != checksum:
                raise ValueError(f"published output changed during run: {name}")
        state.update(status="publishing", publishing=names)
        write_json(run / "state.json", state)
        touched = []
        try:
            for name in names:  # graph.json is last; replacements are on the same filesystem.
                temporary = run / "work" / (uuid.uuid4().hex + "-" + name)
                copy_artifact(staged / name, temporary)
                touched.append(name)
                if name == "cache" and (output / name).exists():
                    os.replace(output / name, run / "work" / (uuid.uuid4().hex + "-old-cache"))
                os.replace(temporary, output / name)
        except OSError:
            for name in reversed(touched):
                backup = run / "backup" / name
                if name == "cache" and (output / name).exists():
                    os.replace(output / name, run / "work" / (uuid.uuid4().hex + "-failed-cache"))
                if state["baseline"][name] is None:
                    (output / name).unlink(missing_ok=True)
                else:
                    temporary = run / "work" / (uuid.uuid4().hex + "-restore-" + name)
                    copy_artifact(backup, temporary)
                    os.replace(temporary, output / name)
            state["status"] = "merged"
            write_json(run / "state.json", state)
            raise
        state["status"] = "published"
        write_json(run / "state.json", state)
    finally:
        # An abrupt interruption leaves the lock and backups for explicit recovery, not blind replay.
        if state["status"] != "publishing":
            lock.rmdir()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("begin").add_argument("--output", type=Path, required=True)
    for name in ("prepare", "merge", "publish"):
        command = commands.add_parser(name)
        command.add_argument("--run", type=Path, required=True)
        if name == "prepare":
            command.add_argument("--plan", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "begin":
            print(begin(args.output))
        elif args.command == "prepare":
            print(json.dumps(prepare(args.run.resolve(), args.plan)))
        elif args.command == "merge":
            result = merge(args.run.resolve())
            print(json.dumps({"nodes": len(result["nodes"]), "edges": len(result["edges"])}))
        else:
            publish(args.run.resolve())
            print("published")
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Graphify run failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
