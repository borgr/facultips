#!/usr/bin/env python3
"""
Split a Markdown file into multiple Jekyll/ReadTheDocs pages.

Usage: run from the repository root or the `proof/facultips` directory.
It reads `index.md` and writes numbered files `01-title-slug.md`, etc.
Each file will have a YAML front matter block with `title` and `permalink`.
"""
import os
import re
from pathlib import Path


def slugify(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[^a-z0-9\- ]+", "", s)
    s = s.replace(" ", "-")
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def first_heading(lines):
    for ln in lines:
        ln = ln.strip()
        if ln.startswith("#"):
            # remove leading # characters and whitespace
            return ln.lstrip('#').strip()
    return None


def split_markdown(input_path: Path, output_dir: Path):
    text = input_path.read_text(encoding="utf-8")
    # Split on lines that are exactly '---' (optionally with surrounding whitespace)
    parts = []
    current = []
    for line in text.splitlines(True):
        if line.strip() == "---":
            parts.append(''.join(current).rstrip('\n'))
            current = []
        else:
            current.append(line)
    # append remainder
    if current:
        parts.append(''.join(current).rstrip('\n'))

    created = []
    for i, part in enumerate(parts, start=1):
        lines = part.splitlines()
        title = first_heading(lines) or f"Page {i}"
        slug = slugify(title) or f"page-{i:02d}"
        filename = f"{i:02d}-{slug}.md"
        permalink = f"/{input_path.parent.name}/{slug}/"
        front = ["---", f"title: \"{title}\"", f"permalink: {permalink}", "---", "\n"]
        out_path = output_dir / filename
        out_path.write_text('\n'.join(front) + part.lstrip('\n'), encoding="utf-8")
        created.append(out_path)

    return created


def main():
    # script is in proof/facultips/scripts; the index.md is in the parent directory
    script_dir = Path(__file__).resolve().parent
    input_md = script_dir.parent / "index.md"
    if not input_md.exists():
        print(f"Cannot find {input_md}; run this from the repo root")
        return 1
    out_dir = script_dir.parent
    created = split_markdown(input_md, out_dir)
    print("Created pages:")
    for p in created:
        print(" -", p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
