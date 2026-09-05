#!/usr/bin/env python3
"""Validate the portable skill corpus with Python standard library only."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


PORTABLE_KEYS = {"name", "description", "metadata"}
VENDOR_LARGE_SKILLS = {"graphify"}
CLIENT_LOCK_MARKERS = {
    "allowed-tools:",
    "agent tool",
    "claude code",
    "claude desktop",
    "codex app",
    "codex cli",
    "claude_config_dir",
    "explore type",
    "general-purpose agent",
    "native plan mode",
    "native plan surface",
    "native question/ask",
    "orca",
    "subagent_type",
    "task tool",
    "task(description=",
    "using the write tool",
    "~/.claude",
    "~/.codex",
}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
CODE_PATH_RE = re.compile(r"`([^`\n]+\.md(?:#[^`\n]+)?)`")


def frontmatter(path: Path) -> tuple[dict[str, str], set[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        raise ValueError("missing opening frontmatter delimiter")
    try:
        end = lines.index("---", 1)
    except ValueError as error:
        raise ValueError("missing closing frontmatter delimiter") from error
    values: dict[str, str] = {}
    keys: set[str] = set()
    for line in lines[1:end]:
        if not line or line[0].isspace() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if not match:
            raise ValueError(f"invalid top-level frontmatter line: {line!r}")
        key, value = match.groups()
        keys.add(key)
        values[key] = (value or "").strip().strip('"').strip("'")
    return values, keys


def scenario_names(path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    required = {"skill", "should_trigger", "near_miss", "required_outcome", "forbidden_outcome"}
    if not rows or set(rows[0]) != required:
        return [], [f"{path}: expected TSV columns {sorted(required)}"]
    names: list[str] = []
    for number, row in enumerate(rows, 2):
        if any(not row[field].strip() for field in required):
            errors.append(f"{path}:{number}: empty scenario field")
        names.append(row["skill"].strip())
    return names, errors


def behavior_scenarios(path: Path) -> tuple[int, list[str]]:
    errors: list[str] = []
    required = {"id", "context", "required_behavior", "forbidden_behavior"}
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows or set(rows[0]) != required:
        return 0, [f"{path}: expected TSV columns {sorted(required)}"]
    seen: set[str] = set()
    for number, row in enumerate(rows, 2):
        if any(not row[field].strip() for field in required):
            errors.append(f"{path}:{number}: empty behavior field")
        scenario_id = row["id"].strip()
        if scenario_id in seen:
            errors.append(f"{path}:{number}: duplicate behavior id {scenario_id!r}")
        seen.add(scenario_id)
    return len(rows), errors


def local_targets(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    targets = set(LINK_RE.findall(text))
    targets.update(
        target for target in CODE_PATH_RE.findall(text)
        if target.startswith(("references/", "assets/", "../", "./"))
    )
    return targets


def validate_links(root: Path, markdown: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in markdown:
        for raw in local_targets(path):
            target = raw.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if any(marker in target for marker in ("<", ">", "{", "}", "*", "|")):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"{path.relative_to(root)}: broken local reference {raw!r}")
    return errors


def validate_client_neutrality(root: Path, paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            lowered = line.casefold()
            for marker in CLIENT_LOCK_MARKERS:
                if marker in lowered:
                    errors.append(
                        f"{path.relative_to(root)}:{number}: client-specific marker {marker!r}"
                    )
    return errors


def count_text(paths: list[Path]) -> tuple[int, int, int]:
    lines = words = size = 0
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        lines += len(text.splitlines())
        words += len(text.split())
        size += len(text.encode())
    return lines, words, size


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    matrix_names, matrix_errors = scenario_names(root / "evals/skill-scenarios.tsv")
    errors.extend(matrix_errors)
    behavior_count, behavior_errors = behavior_scenarios(root / "evals/agent-behavior.tsv")
    errors.extend(behavior_errors)
    skill_files = sorted((root / "skills").glob("*/SKILL.md"))
    actual_names = [path.parent.name for path in skill_files]
    matrix_skill_names = sorted(set(matrix_names))
    if actual_names != matrix_skill_names:
        errors.append(f"entrypoint mismatch: actual={actual_names!r} matrix={matrix_skill_names!r}")

    metadata_text: list[str] = []
    for path in skill_files:
        try:
            values, keys = frontmatter(path)
        except ValueError as error:
            errors.append(f"{path.relative_to(root)}: {error}")
            continue
        name = values.get("name", "")
        if name != path.parent.name:
            errors.append(f"{path.relative_to(root)}: name {name!r} does not match directory")
        if not values.get("description"):
            errors.append(f"{path.relative_to(root)}: missing description")
        unexpected = keys - PORTABLE_KEYS
        if unexpected:
            errors.append(f"{path.relative_to(root)}: unsupported frontmatter keys {sorted(unexpected)}")
        metadata_text.extend((name, values.get("description", "")))
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count > 500 and name not in VENDOR_LARGE_SKILLS:
            errors.append(f"{path.relative_to(root)}: {line_count} lines exceeds 500 without vendor exception")

    client_root = root / "clients"
    for path in sorted(client_root.glob("*/skills/*/SKILL.md")):
        client = path.relative_to(client_root).parts[0]
        try:
            values, keys = frontmatter(path)
        except ValueError as error:
            errors.append(f"{path.relative_to(root)}: {error}")
            continue
        if values.get("name") != path.parent.name:
            errors.append(f"{path.relative_to(root)}: client skill name does not match directory")
        unexpected = keys - PORTABLE_KEYS
        if unexpected:
            errors.append(f"{path.relative_to(root)}: unsupported {client} keys {sorted(unexpected)}")

    markdown = [
        path
        for base in (root / "skills", root / "clients")
        for path in base.rglob("*.md")
        if ".git" not in path.parts
        and "evals" not in path.parts
        and not (
            path.is_relative_to(root / "skills/graphify")
            and path.name != "SKILL.md"
        )
    ]
    errors.extend(validate_links(root, markdown))
    portable_runtime_paths = [root / "AGENTS.md", *sorted((root / "evals").glob("*.tsv"))]
    portable_runtime_paths.extend(
        path
        for path in sorted((root / "skills").rglob("*"))
        if path.is_file() and path.suffix in {".md", ".py"}
    )
    errors.extend(validate_client_neutrality(root, portable_runtime_paths))

    legacy = (root / "skills/graphify/.graphify_version")
    if not legacy.is_file() or not legacy.read_text().strip():
        errors.append("skills/graphify/.graphify_version: missing vendor version")
    lock = json.loads((root / ".skill-lock.json").read_text(encoding="utf-8"))
    if "find-skills" in lock.get("skills", {}):
        errors.append(".skill-lock.json: locally maintained find-skills must not be installer-managed")

    corpus_paths = [
        path for path in root.rglob("*")
        if path.is_file() and path.suffix in {".md", ".yaml", ".yml"} and ".git" not in path.parts
    ]
    corpus = count_text(corpus_paths)
    agents = count_text([root / "AGENTS.md"])
    metadata_blob = "\n".join(metadata_text)
    print(f"portable_skills={len(actual_names)}")
    print(f"maintenance_corpus files={len(corpus_paths)} lines={corpus[0]} words={corpus[1]} bytes={corpus[2]}")
    print(f"runtime_agents lines={agents[0]} words={agents[1]} bytes={agents[2]}")
    print(f"runtime_skill_metadata words={len(metadata_blob.split())} bytes={len(metadata_blob.encode())}")
    print(f"trigger_scenarios={len(matrix_names)}")
    print(f"behavior_scenarios={behavior_count}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("skill_structure=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
