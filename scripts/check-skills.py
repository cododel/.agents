#!/usr/bin/env python3
"""Validate the portable skill corpus with Python standard library only."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


PORTABLE_KEYS = {"name", "description", "allowed-tools", "metadata"}
CLIENT_KEYS = {"claude": {"name", "description", "allowed-tools", "disable-model-invocation"}}
VENDOR_LARGE_SKILLS = {"graphify"}
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
    if len(names) != len(set(names)):
        errors.append(f"{path}: duplicate skill rows")
    return names, errors


def local_targets(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    targets = set(LINK_RE.findall(text))
    if path.name == "SKILL.md":
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
    parser.add_argument("--skip-claude", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    errors: list[str] = []

    matrix_names, matrix_errors = scenario_names(root / "evals/skill-scenarios.tsv")
    errors.extend(matrix_errors)
    skill_files = sorted((root / "skills").glob("*/SKILL.md"))
    actual_names = [path.parent.name for path in skill_files]
    if actual_names != sorted(matrix_names):
        errors.append(f"entrypoint mismatch: actual={actual_names!r} matrix={sorted(matrix_names)!r}")

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
        unexpected = keys - CLIENT_KEYS.get(client, PORTABLE_KEYS)
        if unexpected:
            errors.append(f"{path.relative_to(root)}: unsupported {client} keys {sorted(unexpected)}")

    markdown = [
        path for path in (root / "skills").rglob("*.md")
        if ".git" not in path.parts and "assets" not in path.parts
    ]
    errors.extend(validate_links(root, markdown))

    legacy = (root / "skills/graphify/.graphify_version")
    if not legacy.is_file() or not legacy.read_text().strip():
        errors.append("skills/graphify/.graphify_version: missing vendor version")
    lock = json.loads((root / ".skill-lock.json").read_text(encoding="utf-8"))
    if "find-skills" not in lock.get("skills", {}):
        errors.append(".skill-lock.json: find-skills is not externally managed")

    claude_root = Path.home() / ".claude/skills"
    if not args.skip_claude and claude_root.is_dir():
        for name in matrix_names:
            link = claude_root / name
            expected = (root / "skills" / name).resolve()
            if not link.exists() or link.resolve() != expected:
                errors.append(f"Claude discovery: {name!r} does not resolve to {expected}")
                continue
            for raw in local_targets(expected / "SKILL.md"):
                target = raw.split("#", 1)[0].strip()
                if not target or target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                if any(marker in target for marker in ("<", ">", "{", "}", "*", "|")):
                    continue
                if not (link / target).resolve().exists():
                    errors.append(f"Claude link {name!r}: broken local reference {raw!r}")

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
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("skill_structure=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
