AsciiDoc Defs
=============

This script collects named HTTPS links from AsciiDoc files in the current
directory and writes an index called ``useful_links.adoc``. For example,
running ``python extract_adoc_defs.py contents`` adds a link back to
``contents.html`` at the top of the index.

::

  from __future__ import annotations

  import re
  import sys
  from collections import defaultdict
  from pathlib import Path

Recognizing a link definition
-----------------------------

The single argument supplies the target of the Contents link. The search
directory comes from the working directory, independently of that argument.

::

  if len(sys.argv) != 2:
      print("Usage: extract_adoc_defs <content_link>")
      sys.exit(1)

  content_link = sys.argv[1]

A definition starts at the left margin with a name and a double colon.
Names may contain ASCII letters, digits, underscores, dots, hyphens and spaces.
The URL must occupy a line of its own. Indentation and intervening blank
lines are allowed. For example, the name ``PyLit`` in this input becomes
the visible link text::

    PyLit::
        https://example.org/pylit

::

  PATTERN = re.compile(
      r'^(?P<def_name>[A-Za-z0-9_. -]+)::\s*$\n^\s*(?P<url>https://\S+)\s*$',
      re.MULTILINE,
  )

The index lives alongside its sources. Reserving its filename also keeps
subsequent runs from reading the previous index as input.

::

  OUTPUT_FILE = "useful_links.adoc"
  EXCLUDED_FILES = {OUTPUT_FILE}


Each match contributes a (name, URL) pair. Reading the whole UTF-8
document lets one match span both the name and the URL lines.

::

  def find_definitions_in_file(path: Path) -> list[tuple[str, str]]:
      text = path.read_text(encoding="utf-8")
      return [(m.group("def_name"), m.group("url")) for m in PATTERN.finditer(text)]

Rendering the index
-------------------

Sorting by the case-folded name orders entries within each section while
preserving their original spelling for display. The uppercase initial
supplies the section heading, so names beginning with a digit or
punctuation also have a place in the index.

Each heading is ordinary AsciiDoc so it can appear in the table of
contents. Its list is an HTML passthrough block so each anchor can
specify ``target="_blank"``.

::

  def build_output(definitions: list[tuple[str, str]]) -> str:
      grouped: dict[str, list[tuple[str, str]]] = defaultdict(list)

      for def_name, url in sorted(definitions, key=lambda item: item[0].casefold()):
          first_letter = def_name[:1].upper()
          grouped[first_letter].append((def_name, url))

      lines: list[str] = []

      for letter in sorted(grouped.keys()):
          lines.append(f"=== {letter}")
          lines.append("")
          lines.append("++++")
          lines.append("<ul>")
          for def_name, url in grouped[letter]:
              lines.append(f'<li><a href="{url}" target="_blank">{def_name}</a></li>')
              lines.append("")
          lines.append("</ul>")  
          lines.append("++++")

      def_list = "\n".join(lines).rstrip()
      return f"""= Useful Links
  :toc: left

  link:{content_link}.html[<Contents>]

  ---

  {def_list}
  """    

Collecting links across files
-----------------------------

Only immediate ``*.adoc`` entries in the working directory are scanned.
The set merges repeated (name, URL) pairs across all sources. Two names
for one URL survive, as do two URLs listed under the same name.
Each run replaces the index, even when the collection is empty.

::

  def main():
      current_dir = Path.cwd()

      definitions: set[tuple[str, str]] = set()
      for path in sorted(current_dir.glob("*.adoc")):
          if path.name in EXCLUDED_FILES:
              continue
          definitions.update(find_definitions_in_file(path))

      output = build_output(definitions)
      (current_dir / OUTPUT_FILE).write_text(output, encoding="utf-8")
      print(f"Wrote {len(definitions)} definitions to {OUTPUT_FILE}")


  if __name__ == "__main__":
      main()
