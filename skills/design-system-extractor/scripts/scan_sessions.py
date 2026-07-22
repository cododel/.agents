#!/usr/bin/env python3
"""Optionally mine design-relevant discussion from Claude Code session transcripts.

Discovers transcripts robustly (glob + match by cwd; sanitized-dir fallback), parses
JSONL defensively, and returns ONLY short, design-relevant, human-readable snippets.
Run only after user approval. Never dumps whole transcripts, drops tool output,
non-design chatter, and likely secret-bearing lines, and truncates every snippet.

Stdlib only.

Usage:
    python scan_sessions.py [PROJECT_ROOT] [--config-dir DIR] [--max-snippets N] [--json OUT.json]

If nothing is found, exits 0 with an explanatory note so the caller can proceed with
Layers 1-2.
"""
from __future__ import annotations
import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

SNIPPET_MAX_CHARS = 240
MAX_FILES = 600
MAX_BYTES_PER_FILE = 12_000_000
HEAD_LINES_FOR_CWD = 60

# Bilingual (EN/RU) design-relevance keywords. Substring match, case-insensitive.
KEYWORDS = [
    # EN
    "design", "ui", "ux", "interface", "aesthetic", "look and feel", "brand", "branding", "logo",
    "palette", "color", "colour", "theme", "dark mode", "light mode", "contrast",
    "font", "typeface", "typography", "serif", "monospace", "weight", "tracking",
    "leading", "spacing", "padding", "margin", "radius", "rounded", "border", "shadow",
    "grid", "layout", "hero", "component", "button", "card", "input", "navbar", "nav ",
    "header", "footer", "hover", "focus", "active", "animation", "transition", "motion",
    "glitch", "marquee", "cursor", "minimal", "brutal", "wireframe", "tailwind", "shadcn",
    "token", "uppercase", "tracking-tighter",
    # RU
    "дизайн", "интерфейс", "эстетик", "бренд", "логотип", "палитр", "цвет", "тема",
    "тёмн", "темн", "светл", "контраст", "шрифт", "типографик", "начертан", "моноширин",
    "насыщенн", "трекинг", "межстрочн", "отступ", "паддинг", "радиус", "скругл",
    "границ", "рамк", "тень", "сетк", "макет", "верстк", "герой", "компонент", "кнопк",
    "карточк", "инпут", "поле", "навигац", "хедер", "шапк", "футер", "ховер", "наведен",
    "фокус", "актив", "анимаци", "переход", "движен", "глитч", "бегущ", "курсор",
    "минимал", "бруталь", "вайрфрейм", "токен",
]
SENSITIVE_RE = re.compile(
    r"(?:authorization\s*:|bearer\s+[a-z0-9._-]+|api[_-]?key\s*[:=]|"
    r"password\s*[:=]|secret\s*[:=]|(?:access|refresh|auth|api)[_-]?token\s*[:=]|"
    r"-----BEGIN [A-Z ]+PRIVATE KEY-----)",
    re.IGNORECASE,
)


def project_root(arg: str) -> Path:
    p = Path(arg).resolve()
    try:
        top = subprocess.run(
            ["git", "-C", str(p), "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5,
        )
        if top.returncode == 0 and top.stdout.strip():
            return Path(top.stdout.strip()).resolve()
    except (OSError, subprocess.SubprocessError):
        pass
    return p


def config_root(arg: str | None) -> Path:
    if arg:
        return Path(arg).expanduser().resolve()
    env = os.environ.get("CLAUDE_CONFIG_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return (Path.home() / ".claude").resolve()


def sanitized(path: Path) -> str:
    return re.sub(r"[/.]", "-", str(path))


def candidate_files(cfg: Path) -> list[Path]:
    files: list[Path] = []
    projects = cfg / "projects"
    if projects.is_dir():
        files = list(projects.rglob("*.jsonl"))
    if not files and cfg.is_dir():
        # bounded fallback
        for i, f in enumerate(cfg.rglob("*.jsonl")):
            files.append(f)
            if i + 1 >= MAX_FILES:
                break
    files.sort(key=lambda f: f.stat().st_mtime if f.exists() else 0, reverse=True)
    return files[:MAX_FILES]


def file_cwd(path: Path) -> str | None:
    """Read the first lines and return the recorded cwd, if any."""
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as fh:
            for i, line in enumerate(fh):
                if i >= HEAD_LINES_FOR_CWD:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                cwd = obj.get("cwd")
                if cwd:
                    return str(cwd)
    except OSError:
        return None
    return None


def matches_project(path: Path, root: Path) -> bool:
    cwd = file_cwd(path)
    root_s = str(root)
    if cwd:
        cwd_r = str(Path(cwd).resolve()) if Path(cwd).is_absolute() else cwd
        return cwd_r == root_s or cwd_r.startswith(root_s + os.sep)
    # Conservative fallback: exact sanitized directory match only.
    san = sanitized(root)
    return path.parent.name == san


def text_blocks(obj: dict) -> list[tuple[str, str]]:
    """Return (role, text) pairs for human-readable text in a transcript entry."""
    role = obj.get("type") or obj.get("role")
    if role not in ("user", "assistant"):
        return []
    msg = obj.get("message")
    out: list[tuple[str, str]] = []
    if isinstance(msg, dict):
        content = msg.get("content")
    else:
        content = obj.get("content")
    if isinstance(content, str):
        out.append((role, content))
    elif isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                t = block.get("text")
                if isinstance(t, str):
                    out.append((role, t))
            elif isinstance(block, str):
                out.append((role, block))
    return out


def design_lines(text: str) -> list[str]:
    hits = []
    for raw in re.split(r"[\r\n]+", text):
        line = raw.strip()
        if len(line) < 4:
            continue
        low = line.lower()
        if SENSITIVE_RE.search(line):
            continue
        if any(kw in low for kw in KEYWORDS):
            hits.append(line[:SNIPPET_MAX_CHARS])
    return hits


def scan(root: Path, cfg: Path, max_snippets: int):
    files = candidate_files(cfg)
    matched = [f for f in files if matches_project(f, root)]
    # newest first
    matched.sort(key=lambda f: f.stat().st_mtime if f.exists() else 0, reverse=True)

    snippets = []
    seen = set()
    sessions_with_hits = 0

    for f in matched:
        try:
            if f.stat().st_size > MAX_BYTES_PER_FILE:
                continue
        except OSError:
            continue
        try:
            mtime = f.stat().st_mtime
        except OSError:
            mtime = 0
        import datetime
        date = datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d") if mtime else "?"
        file_had_hit = False
        try:
            with f.open("r", encoding="utf-8", errors="ignore") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if not isinstance(obj, dict):
                        continue
                    for role, text in text_blocks(obj):
                        for snip in design_lines(text):
                            key = (role, snip)
                            if key in seen:
                                continue
                            seen.add(key)
                            snippets.append(
                                {"date": date, "role": role, "text": snip}
                            )
                            file_had_hit = True
                            if len(snippets) >= max_snippets:
                                break
                        if len(snippets) >= max_snippets:
                            break
                    if len(snippets) >= max_snippets:
                        break
        except OSError:
            continue
        if file_had_hit:
            sessions_with_hits += 1
        if len(snippets) >= max_snippets:
            break

    note = None
    if not files:
        note = (
            f"No Claude Code transcripts found under {cfg}. "
            "Proceed with Layers 1-2 (code + docs) and note history was unavailable."
        )
    elif not matched:
        note = (
            f"Found {len(files)} transcript(s) but none matched project root {root}. "
            "Proceed with Layers 1-2."
        )
    elif not snippets:
        note = (
            f"Matched {len(matched)} session(s) for this project but found no design-relevant "
            "discussion. Treat Layer 3 as empty."
        )

    return {
        "project_root": str(root),
        "transcripts_found": len(files),
        "matched_sessions": len(matched),
        "sessions_with_design_hits": sessions_with_hits,
        "snippets": snippets,
        "note": note,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Mine design-relevant snippets from past sessions.")
    ap.add_argument("root", nargs="?", default=".", help="Project root (default: cwd)")
    ap.add_argument("--config-dir", default=None, help="Override Claude config dir")
    ap.add_argument("--max-snippets", type=int, default=80, help="Cap on snippets returned")
    ap.add_argument("--json", dest="out", default=None, help="Also write JSON to this path")
    args = ap.parse_args(argv)

    root = project_root(args.root)
    cfg = config_root(args.config_dir)
    result = scan(root, cfg, args.max_snippets)
    out_text = json.dumps(result, indent=2, ensure_ascii=False)
    try:
        print(out_text)
    except BrokenPipeError:
        try:
            sys.stdout.close()
        except OSError:
            pass
        return 0
    if args.out:
        Path(args.out).write_text(out_text, encoding="utf-8")
        print(f"\n[written] {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
