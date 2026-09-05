"""Keep derived reading material separate from stable Graphify source identity."""
from __future__ import annotations

import hashlib
from pathlib import Path
import unicodedata


def source_reads(files: dict[str, list[str]], originals: list[Path], root: Path,
                 converted: Path) -> tuple[dict[str, list[str]], dict[str, str]]:
    """Resolve the pinned converter's path-derived names; fail closed on ambiguity."""
    candidates: dict[str, list[str]] = {}
    for original in originals:
        key = unicodedata.normalize('NFC', original.resolve().relative_to(root.resolve()).as_posix())
        suffix = hashlib.sha256(key.encode()).hexdigest()[:8]
        name = f'{original.stem}_{suffix}.md'
        candidates.setdefault(name, []).append(str(original.resolve()))
    normalized: dict[str, list[str]] = {}
    reads: dict[str, str] = {}
    for kind, paths in files.items():
        normalized[kind] = []
        for raw in paths:
            path = Path(raw).resolve()
            if path.parent == converted.resolve():
                matches = candidates.get(path.name, [])
                if len(matches) != 1:
                    raise ValueError(f'cannot identify original for converted input: {path}')
                original = matches[0]
                normalized[kind].append(original)
                reads[original] = str(path)
            else:
                normalized[kind].append(str(path))
    return normalized, reads


def incremental_files(files: dict[str, list[str]], manifest: dict, root: Path) -> dict:
    new: dict[str, list[str]] = {kind: [] for kind in files}
    unchanged: dict[str, list[str]] = {kind: [] for kind in files}
    for kind, paths in files.items():
        for raw in paths:
            entry = manifest.get(unicodedata.normalize('NFC', raw))
            # Legacy or unstamped semantic input is deliberately re-extracted.
            stored_hash = entry.get('semantic_hash') if isinstance(entry, dict) else None
            current_hash = hashlib.md5(Path(raw).read_bytes()).hexdigest()
            (unchanged if stored_hash == current_hash else new)[kind].append(raw)
    current = {unicodedata.normalize('NFC', p) for paths in files.values() for p in paths}
    missing = [p for p in manifest if unicodedata.normalize('NFC', p) not in current]
    return {'new_files': new, 'unchanged_files': unchanged,
            'new_total': sum(len(paths) for paths in new.values()),
            'deleted_files': [p for p in missing if not Path(p).exists()],
            'excluded_files': [p for p in missing if Path(p).exists()], 'incremental': True}


def detect_sources(root: Path, *, published_output: Path, incremental: bool = False) -> dict:
    # Imported only for actual builds; helper validation and regression fixtures need no package.
    from graphify.detect import detect, load_manifest, OFFICE_EXTENSIONS
    from graphify.paths import out_path

    root = root.resolve()
    published_output = published_output.resolve()
    if published_output == root:
        raise ValueError('published output must not equal the corpus root')
    # Upstream excludes are gitignore patterns relative to root, not absolute filesystem paths.
    excludes = (["/" + published_output.relative_to(root).as_posix() + "/"]
                if published_output.is_relative_to(root) else [])
    full = detect(root, cache_root=Path.cwd(), google_workspace=False, extra_excludes=excludes)
    converted = out_path('converted').resolve()
    originals = [p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in OFFICE_EXTENSIONS
                 and 'graphify-out' not in p.relative_to(root).parts
                 and not p.resolve().is_relative_to(published_output)]
    full['files'], full['read_paths'] = source_reads(full['files'], originals, root, converted)
    if incremental:
        full.update(incremental_files(full['files'], load_manifest(root=root), root))
    return full
