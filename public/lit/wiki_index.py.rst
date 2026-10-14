Wiki Index
==========

Build a Markdown or AsciiDoc index of questions in a Markdown wiki.

Expected entry format:

.. code-block:: text

    # Entry title

    > Question text (possibly spanning multiple lines)

    ---

    Answer text

----

::

  from __future__ import annotations

  import argparse
  import os
  import re
  import sys
  from dataclasses import dataclass
  from pathlib import Path
  from urllib.parse import quote


  TITLE_RE = re.compile(r"^#(?!#)\s+(.+?)\s*$")
  SEPARATOR_RE = re.compile(r"^\s*-{3,}\s*$")
  BLOCKQUOTE_RE = re.compile(r"^\s*> ?(.*)$")


  @dataclass(frozen=True)
  class Entry:
      title: str
      question: str
      line_number: int


.. function:: extract_entries(markdown: str) -> list[Entry]

::

  def extract_entries(markdown: str) -> list[Entry]:
      """Extract valid title/question pairs from Markdown text."""
      lines = markdown.splitlines()
      entries: list[Entry] = []

      for index, line in enumerate(lines):
          title_match = TITLE_RE.match(line)
          if not title_match:
              continue

          question_start = index + 1
          while question_start < len(lines) and not lines[question_start].strip():
              question_start += 1

          # A wiki entry is recognized only when its first content line is quoted.
          if question_start >= len(lines) or not BLOCKQUOTE_RE.match(lines[question_start]):
              continue

          separator = question_start + 1
          while separator < len(lines) and not SEPARATOR_RE.match(lines[separator]):
              separator += 1
          if separator >= len(lines):
              continue

          question_lines = lines[question_start:separator]
          while question_lines and not question_lines[-1].strip():
              question_lines.pop()

          # Remove Markdown's blockquote marker. Lines without a marker are kept:
          # Markdown permits them as lazy continuation lines in a blockquote.
          cleaned_lines = []
          for question_line in question_lines:
              match = BLOCKQUOTE_RE.match(question_line)
              cleaned_lines.append(match.group(1) if match else question_line)

          question = "\n".join(cleaned_lines).strip()
          if question:
              entries.append(
                  Entry(
                      title=title_match.group(1).strip(),
                      question=question,
                      line_number=index + 1,
                  )
              )

      return entries


.. function:: asciidoc_text(text: str) -> str

::

  def asciidoc_text(text: str) -> str:
      """Prevent accidental AsciiDoc substitutions in displayed prose."""
      return text.replace("\\", "\\\\").replace("{", "\\{")


.. function:: link_target(source: Path, output: Path) -> str

::

  def link_target(source: Path, anchor: str, output: Path) -> str:
      relative = os.path.relpath(source, output.parent).replace(os.sep, "/")
      return quote(relative, safe="/._-~") + "#" + anchor

.. function:: header_to_anchor(header: str) -> str

::

  def header_to_anchor(header: str) -> str:
      """
      Convert a header into a URL-friendly HTML anchor ID.

      Example:
          "GitLab Pipeline 2nd Error After Updating `.gitlab-ci.yml`"
          -> "gitlab-pipeline-2nd-error-after-updating-gitlab-ciyml"
      """
      # Convert to lowercase
      anchor = header.lower()

      # Remove punctuation, while preserving letters, numbers, spaces, and hyphens
      anchor = re.sub(r"[^a-z0-9\s-]", "", anchor)

      # Replace whitespace with a single hyphen
      anchor = re.sub(r"\s+", "-", anchor)

      # Collapse repeated hyphens and remove leading/trailing ones
      return re.sub(r"-+", "-", anchor).strip("-")
    
.. function:: render_asciidoc_index(files_and_entries: list[tuple[Path, list[Entry]]], output: Path, root: Path) -> str

::

  def truncate(line, maxlen):
      return line if len(line) <= maxlen else line[:maxlen] + "..."
    
  def render_asciidoc_index(
      files_and_entries: list[tuple[Path, list[Entry]]], output: Path, root: Path
  ) -> str:
      total = sum(len(entries) for _, entries in files_and_entries)
      lines = [
          f"= {root.name}",
          ":icons: font",
          ":toc: left",
          ":toclevels: 2",
          "",
          f"Indexed {total} question{'s' if total != 1 else ''} "
          f"from {len(files_and_entries)} file{'s' if len(files_and_entries) != 1 else ''}.",
          "",
      ]

      for source, entries in files_and_entries:
          relative_name = source.relative_to(root).as_posix()
          lines.extend([f"== {asciidoc_text(relative_name)}", ""])

          for entry in reversed(entries):
              label = asciidoc_text(f"{relative_name[0:-3]} ({entry.line_number})")
              anchor = header_to_anchor(entry.title)
              target = link_target(source, anchor, output)
              lines.extend(
                  [
                      f"=== {asciidoc_text(entry.title)}",
                      "",
                      "[CAUTION]",
                      "====",
                  ]
              )
              for question_line in asciidoc_text(truncate(entry.question, 200)).splitlines():
                  # Avoid prematurely closing the quote block.
                  #lines.append("\\____" if question_line == "____" else question_line)
                  lines.append(question_line)
              #lines.extend(["====", ""])
              #lines.append("")
              lines.extend(
                  [
                      "",
                      f"link:{target}[{label}]",
                      "",
                      "====", 
                      "",
                  ]
              )
            
      return "\n".join(lines).rstrip() + "\n"


.. function:: markdown_label(text: str) -> str

::

  def markdown_label(text: str) -> str:
      """Escape text used as a Markdown link label."""
      return text.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")


.. function:: render_markdown_index(files_and_entries: list[tuple[Path, list[Entry]]], output: Path, root: Path) -> str

::

  def render_markdown_index(
      files_and_entries: list[tuple[Path, list[Entry]]], output: Path, root: Path
  ) -> str:
      total = sum(len(entries) for _, entries in files_and_entries)
      lines = [
          f"# {root.name}",
          "",
          f"Indexed {total} question{'s' if total != 1 else ''} "
          f"from {len(files_and_entries)} file{'s' if len(files_and_entries) != 1 else ''}.",
          "",
      ]

      for source, entries in files_and_entries:
          relative_name = source.relative_to(root).as_posix()
          display_name = relative_name.replace("`", "\\`")
          lines.extend([f"## `{display_name}`", ""])

          for entry in entries:
              label = markdown_label(f"{relative_name}:{entry.line_number}")
              anchor = header_to_anchor(entry.title)
              target = link_target(source, anchor, output)
              lines.extend(
                  [
                      f"### {entry.title}",
                      "",
                      f"Source: [{label}]({target}#L{entry.line_number})",
                      "",
                  ]
              )
              for question_line in entry.question.splitlines():
                  lines.append(f"> {question_line}" if question_line else ">")
              lines.append("")

      return "\n".join(lines).rstrip() + "\n"


.. function:: markdown_files(root: Path) -> list[Path]

::

  def markdown_files(root: Path) -> list[Path]:
      return sorted(
          (path for path in root.rglob("*.md") if path.is_file()),
          key=lambda path: path.relative_to(root).as_posix().casefold(),
          reverse=True,
      )


.. function:: parse_args() -> argparse.Namespace

::

  def parse_args() -> argparse.Namespace:
      parser = argparse.ArgumentParser(
          description="Recursively create a Markdown or AsciiDoc wiki question index."
      )
      parser.add_argument(
          "root",
          nargs="?",
          type=Path,
          default=Path.cwd(),
          help="wiki directory to scan (default: current directory)",
      )
      parser.add_argument(
          "-f",
          "--format",
          choices=("markdown", "asciidoc"),
          default="markdown",
          help="index format (default: markdown)",
      )
      parser.add_argument(
          "-o",
          "--output",
          type=Path,
          help="output file (default: wiki_index.md or wiki_index.adoc)",
      )
      return parser.parse_args()


.. function:: main() -> int

::

  def main() -> int:
      args = parse_args()
      root = args.root.expanduser().resolve()
      default_name = "wiki_index.md" if args.format == "markdown" else "wiki_index.adoc"
      output = (args.output or Path(default_name)).expanduser().resolve()

      if not root.is_dir():
          print(f"error: wiki root is not a directory: {root}", file=sys.stderr)
          return 2

      indexed: list[tuple[Path, list[Entry]]] = []
      for source in markdown_files(root):
          try:
              entries = extract_entries(source.read_text(encoding="utf-8"))
          except (OSError, UnicodeError) as error:
              print(f"warning: cannot read {source}: {error}", file=sys.stderr)
              continue
          if entries:
              indexed.append((source, entries))

      output.parent.mkdir(parents=True, exist_ok=True)
      renderer = (
          render_markdown_index if args.format == "markdown" else render_asciidoc_index
      )
      output.write_text(renderer(indexed, output, root), encoding="utf-8")
      count = sum(len(entries) for _, entries in indexed)
      print(f"Wrote {count} question(s) from {len(indexed)} file(s) to {output}")
      return 0


  if __name__ == "__main__":
      raise SystemExit(main())
