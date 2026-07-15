#!/usr/bin/env python3
"""Validate local Markdown paths and heading anchors."""

import argparse
import re
from pathlib import Path
from urllib.parse import unquote

_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
_HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)


def github_anchor(text: str) -> str:
    text = re.sub(r"[*_`~]", "", text.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return re.sub(r"\s+", "-", text)


def headings(path: Path) -> set[str]:
    return {github_anchor(match) for match in _HEADING.findall(path.read_text(encoding="utf-8"))}


def check(root: Path) -> list[str]:
    errors: list[str] = []
    for source in sorted(root.rglob("*.md")):
        text = source.read_text(encoding="utf-8")
        for raw_target in _LINK.findall(text):
            target = raw_target.strip().split(" ", 1)[0].strip("<>")
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            path_part, _, anchor = target.partition("#")
            destination = (
                source if not path_part else (source.parent / unquote(path_part)).resolve()
            )
            try:
                destination.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{source.relative_to(root)}: link escapes repository: {target}")
                continue
            if not destination.is_file():
                errors.append(f"{source.relative_to(root)}: missing target: {target}")
                continue
            if (
                anchor
                and destination.suffix.lower() == ".md"
                and unquote(anchor) not in headings(destination)
            ):
                errors.append(f"{source.relative_to(root)}: missing anchor: {target}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", nargs="?", type=Path, default=Path.cwd())
    args = parser.parse_args()
    errors = check(args.root.resolve())
    if errors:
        raise SystemExit("\n".join(errors))
    count = sum(1 for _ in args.root.rglob("*.md"))
    print(f"validated local links in {count} Markdown files")


if __name__ == "__main__":
    main()
