AsciiDoc Defs
=============

*Extract useful links from ADOC files*

::

  from __future__ import annotations

  import re
  import sys
  from collections import defaultdict
  from pathlib import Path

First argument used to create backlink to home page.

::
    
  if len(sys.argv) != 2:
      print("Usage: extract_adoc_defs <content_link>")
      sys.exit(1)
  
  content_link = sys.argv[1]

  PATTERN = re.compile(
      r'^(?P<def_name>[A-Za-z0-9_.-]+)::\s*$\n^\s*(?P<url>https://\S+)\s*$',
      re.MULTILINE,
  )

Output file

::
  
  OUTPUT_FILE = "useful_links.adoc"
  EXCLUDED_FILES = {OUTPUT_FILE}


.. method:: find_definitions_in_file(path: Path) -> list[tuple[str, str]]

::
    
  def find_definitions_in_file(path: Path) -> list[tuple[str, str]]:
      text = path.read_text(encoding="utf-8")
      return [(m.group("def_name"), m.group("url")) for m in PATTERN.finditer(text)]

.. method:: build_output(definitions: list[tuple[str, str]]) -> str

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

          for def_name, url in grouped[letter]:
              lines.append(f"{def_name}::")
              lines.append(url)
              lines.append("")

      def_list = "\n".join(lines).rstrip()
      return f"""= Useful Links
  :toc: left


  link:{content_link}.html[<Contents>]

  ---

  {def_list}
  """    

.. method:: main()

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
