#!/usr/bin/env python3
"""Deterministically harvest visual design-token candidates from a project.

Scans common web and native text formats for:
  - colors (hex + functional: rgb/hsl/oklch/...), with frequency counts
  - CSS custom properties (--name: value), color-valued ones flagged
  - font families (CSS font-family, next/font/google imports, Tailwind fontFamily)
  - border-radius values (CSS) and Tailwind `rounded-*` usage
  - dimension candidates (repeated px/rem/pt/dp/sp values)

Frequency is a prioritization signal, not semantic proof. Stdlib only.

Usage:
    python collect_tokens.py [PROJECT_ROOT] [--json OUT.json] [--top N]
"""
from __future__ import annotations
import argparse
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

IGNORE_DIRS = {
    ".git", "node_modules", ".next", "dist", "build", "out", ".turbo", "coverage",
    ".cache", "vendor", ".venv", "venv", "__pycache__", ".svelte-kit", ".vercel",
    ".output", "storybook-static", ".idea", ".vscode", "tmp",
}
SCAN_EXT = {
    ".css", ".scss", ".sass", ".less", ".pcss",
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".vue", ".svelte", ".astro", ".html",
    ".swift", ".kt", ".kts", ".dart", ".xml", ".storyboard", ".xib",
    ".json", ".yaml", ".yml", ".toml",
}
SKIP_FILES = {
    "package-lock.json", "npm-shrinkwrap.json", "yarn.lock", "pnpm-lock.yaml",
    "bun.lock", "bun.lockb", "Podfile.lock", "Package.resolved",
}
TAILWIND_CONFIG = re.compile(r"^tailwind\.config\.(?:js|cjs|mjs|ts)$")
MAX_BYTES = 1_500_000          # skip very large / likely-minified files
MIN_LINE_FOR_MINIFIED = 5000   # if a file has lines longer than this, treat as minified -> skip

HEX_RE = re.compile(r"#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{4}|[0-9a-fA-F]{3})\b")
FUNC_COLOR_RE = re.compile(
    r"\b(rgba?|hsla?|hwb|oklch|oklab|lab|lch)\(\s*([^)]{0,80})\)", re.IGNORECASE
)
CUSTOM_PROP_RE = re.compile(r"(--[A-Za-z0-9_-]+)\s*:\s*([^;{}]+);")
FONT_FAMILY_RE = re.compile(r"font-family\s*:\s*([^;{}]+);", re.IGNORECASE)
NEXT_FONT_RE = re.compile(
    r"import\s*\{?\s*([A-Za-z_][\w]*(?:\s*,\s*[A-Za-z_][\w]*)*)\s*\}?\s*from\s*"
    r"['\"]next/font/(?:google|local)['\"]"
)
TW_FONTFAMILY_RE = re.compile(r"fontFamily\s*:\s*\{([^}]*)\}", re.IGNORECASE | re.DOTALL)
RADIUS_RE = re.compile(r"border-radius\s*:\s*([^;{}]+);", re.IGNORECASE)
TW_ROUNDED_RE = re.compile(
    r"(?<![\w-])rounded(?:-(?:none|full|sm|md|lg|xl|2xl|3xl))?(?![\w-])"
)
DIMENSION_RE = re.compile(r"(?<![\w.])(\d+(?:\.\d+)?)(px|rem|pt|dp|sp)\b")
NATIVE_FONT_RE = re.compile(
    r"(?:fontFamily\s*[:=]\s*|font-family\s*=\s*|\.custom\(\s*)['\"]([^'\"]+)['\"]",
    re.IGNORECASE,
)
NATIVE_RADIUS_RE = re.compile(
    r"(?:cornerRadius\s*[:=(]\s*|BorderRadius\.circular\(\s*)(\d+(?:\.\d+)?)",
    re.IGNORECASE,
)
COLOR_HINT_RE = re.compile(
    r"(#[0-9a-fA-F]{3,8}\b|\b(?:rgba?|hsla?|oklch|oklab|lab|lch|hwb)\(|\bvar\(--)",
    re.IGNORECASE,
)


def is_probably_minified(text: str) -> bool:
    for line in text.splitlines():
        if len(line) > MIN_LINE_FOR_MINIFIED:
            return True
    return False


def norm_color_func(name: str, body: str) -> str:
    body = re.sub(r"\s+", " ", body.strip())
    return f"{name.lower()}({body})"


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            d for d in dirnames
            if (d not in IGNORE_DIRS and not d.startswith(".")) or d == ".storybook"
        )
        for fn in sorted(filenames):
            if fn in SKIP_FILES:
                continue
            p = Path(dirpath) / fn
            ext = p.suffix.lower()
            if ext in SCAN_EXT or TAILWIND_CONFIG.match(fn) or fn == "components.json":
                yield p


def read_text(p: Path):
    try:
        if p.stat().st_size > MAX_BYTES:
            return None
    except OSError:
        return None
    try:
        return p.read_text(encoding="utf-8", errors="strict")
    except (UnicodeDecodeError, OSError):
        try:
            return p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return None


def collect(root: Path, top: int):
    colors = Counter()
    color_sample = {}            # value -> first relative path
    custom_props = {}            # name -> values/count/color metadata
    font_families = Counter()
    next_fonts = set()
    tw_fontfamily_blocks = []
    radius_values = Counter()
    tw_rounded = Counter()
    dimensions = Counter()
    files_scanned = 0
    tailwind_config_present = False
    shadcn = None

    for p in iter_files(root):
        text = read_text(p)
        if text is None:
            continue
        if is_probably_minified(text):
            continue
        rel = str(p.relative_to(root))
        files_scanned += 1
        fn = p.name

        if TAILWIND_CONFIG.match(fn):
            tailwind_config_present = True
            for m in TW_FONTFAMILY_RE.finditer(text):
                tw_fontfamily_blocks.append(re.sub(r"\s+", " ", m.group(1)).strip()[:300])

        if fn == "components.json":
            try:
                data = json.loads(text)
                tw = data.get("tailwind", {}) if isinstance(data, dict) else {}
                shadcn = {
                    "style": data.get("style"),
                    "baseColor": tw.get("baseColor"),
                    "cssVariables": tw.get("cssVariables"),
                    "tsx": data.get("tsx"),
                }
            except (json.JSONDecodeError, AttributeError):
                pass

        # colors: hex
        for m in HEX_RE.finditer(text):
            val = m.group(0).lower()
            colors[val] += 1
            color_sample.setdefault(val, rel)
        # colors: functional
        for m in FUNC_COLOR_RE.finditer(text):
            val = norm_color_func(m.group(1), m.group(2))
            colors[val] += 1
            color_sample.setdefault(val, rel)

        # custom properties
        for m in CUSTOM_PROP_RE.finditer(text):
            name, raw = m.group(1), m.group(2).strip()
            entry = custom_props.setdefault(
                name, {"values": {}, "count": 0, "color": bool(COLOR_HINT_RE.search(raw))}
            )
            entry["count"] += 1
            value = raw[:120]
            value_entry = entry["values"].setdefault(value, {"count": 0, "sample": rel})
            value_entry["count"] += 1
            if COLOR_HINT_RE.search(raw):
                entry["color"] = True

        # fonts
        for m in FONT_FAMILY_RE.finditer(text):
            stack = re.sub(r"\s+", " ", m.group(1)).strip().strip(";")
            font_families[stack[:120]] += 1
        for m in NEXT_FONT_RE.finditer(text):
            for name in re.split(r"\s*,\s*", m.group(1)):
                name = name.strip()
                if name:
                    next_fonts.add(name)
        for m in NATIVE_FONT_RE.finditer(text):
            font_families[m.group(1).strip()[:120]] += 1

        # radius
        for m in RADIUS_RE.finditer(text):
            radius_values[re.sub(r"\s+", " ", m.group(1)).strip()] += 1
        for m in TW_ROUNDED_RE.finditer(text):
            tw_rounded[m.group(0)] += 1
        for m in NATIVE_RADIUS_RE.finditer(text):
            radius_values[m.group(1)] += 1

        # Dimension candidates; semantic role must be confirmed from source context.
        seen_in_file = Counter()
        for m in DIMENSION_RE.finditer(text):
            tok = f"{m.group(1)}{m.group(2)}"
            if seen_in_file[tok] < 50:
                dimensions[tok] += 1
                seen_in_file[tok] += 1

    color_top = [
        {"value": v, "count": c, "sample": color_sample.get(v)}
        for v, c in colors.most_common(top)
    ]
    color_props = {
        n: e for n, e in sorted(custom_props.items(), key=lambda kv: -kv[1]["count"])
        if e["color"]
    }

    return {
        "project_root": str(root),
        "files_scanned": files_scanned,
        "tailwind_config_present": tailwind_config_present,
        "shadcn_components_json": shadcn,
        "colors": {
            "distinct": len(colors),
            "top": color_top,
        },
        "custom_properties": {
            "total": len(custom_props),
            "color_valued": color_props,
            "all": dict(sorted(custom_props.items(), key=lambda kv: -kv[1]["count"])),
        },
        "fonts": {
            "css_families": [{"stack": s, "count": c} for s, c in font_families.most_common(20)],
            "next_font_imports": sorted(next_fonts),
            "tailwind_fontFamily": tw_fontfamily_blocks,
        },
        "radius": {
            "css_values": [{"value": v, "count": c} for v, c in radius_values.most_common(20)],
            "tailwind_rounded": [{"class": k, "count": c} for k, c in tw_rounded.most_common(20)],
        },
        "dimension_candidates": [
            {"value": v, "count": c} for v, c in dimensions.most_common(25)
        ],
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="Harvest visual design tokens from a project.")
    ap.add_argument("root", nargs="?", default=".", help="Project root (default: cwd)")
    ap.add_argument("--json", dest="out", default=None, help="Also write JSON to this path")
    ap.add_argument("--top", type=int, default=40, help="How many top colors to report")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: not a directory: {root}", file=sys.stderr)
        return 2

    result = collect(root, args.top)
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
