# Markdown Converter
# ==================
#
# Convert all ``*.md`` files from a specified folder into HTML files in the
# current working directory.
#
# Usage:
#
# .. code-block:: console
#
#    python mark.py -b path/to/markdown_folder
#    python mark.py -t path/to/markdown_folder
#
# Options:
#
# ``-b``
#    Generate Bootstrap-styled HTML.
#
# ``-t``
#    Generate Tailwind-styled HTML.
#
# ::

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path
from md_utils import save_html


# .. function:: process_folder(folder: Path, html_format: str) -> None

def process_folder(folder: Path, html_format: str) -> None:
    if not folder.exists():
        raise FileNotFoundError(f"Folder does not exist: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(f"Not a folder: {folder}")

    md_files = sorted(folder.glob("*.md"))

    if not md_files:
        print(f"No .md files found in {folder}")
        return

    for md_file in md_files:
        html_file = Path.cwd() / f"{md_file.stem}.html"

        md_text = md_file.read_text(encoding="utf-8")
        save_html(md_text, md_file.stem, html_format)
        print(f"Created {html_file.name}")


# .. function:: parse_args() -> argparse.Namespace

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert Markdown files from a folder into HTML files in the current directory."
    )

    format_group = parser.add_mutually_exclusive_group(required=True)
    format_group.add_argument(
        "-b",
        "--bootstrap",
        action="store_true",
        help="Create Bootstrap-styled HTML files.",
    )
    format_group.add_argument(
        "-t",
        "--tailwind",
        action="store_true",
        help="Create Tailwind-styled HTML files.",
    )

    parser.add_argument(
        "folder",
        type=Path,
        help="Folder containing .md files to convert.",
    )

    return parser.parse_args()


# .. function:: main() -> None

def main() -> None:
    args = parse_args()
    html_format = "Bootstrap" if args.bootstrap else "Tailwind"
    process_folder(args.folder, html_format)


if __name__ == "__main__":
    main()
