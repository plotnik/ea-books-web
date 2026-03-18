Udemy HTML TOC
==============

::

  from pathlib import Path
  from bs4 import BeautifulSoup

Input and output file

::

  INPUT_FILE = "toc.html"
  OUTPUT_FILE = "toc.txt"

Remove inner spaces

::

  def normalize_inner_spaces(text: str) -> str:
      return " ".join(text.split())

Extract TOC

::

  def extract_toc(html_text: str) -> str:
      soup = BeautifulSoup(html_text, "html.parser")
      lines = []

      section_no = 0
      lecture_no = 0

      # Each curriculum section panel
      panels = soup.select("div[class*='curriculum-section-module'][class*='panel']")

      for panel in panels:
          # Section title
          title_el = panel.select_one("span[class*='section-title']")
          if not title_el:
              continue

          section_title = normalize_inner_spaces(title_el.get_text(" ", strip=True))
          if not section_title:
              continue

          section_no += 1
          lines.append(f"### {section_no}. {section_title}")
          lines.append("")

          # Lecture items inside the section
          item_rows = panel.select("div.ud-block-list-item-content")

          for item in item_rows:
              lecture_el = item.select_one("span[class*='course-lecture-title']")
              if lecture_el:
                  lecture_title = normalize_inner_spaces(
                      lecture_el.get_text(" ", strip=True)
                  )
                  if lecture_title:
                      lecture_no += 1
                      lines.append(f"  {lecture_no}. {lecture_title}")

          lines.append("")

      return "\n".join(lines).rstrip() + "\n"

Main

::

  def main():
      input_path = Path(INPUT_FILE)
      output_path = Path(OUTPUT_FILE)

      html_text = input_path.read_text(encoding="utf-8")
      toc_text = extract_toc(html_text)
      output_path.write_text(toc_text, encoding="utf-8")

      print(f"Created {output_path}")


  if __name__ == "__main__":
      main()