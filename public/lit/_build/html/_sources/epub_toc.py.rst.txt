EPUB TOC
========

::

  from bs4 import BeautifulSoup
  import re
  import argparse

  parser = argparse.ArgumentParser(description="EPUB TOC")
  parser.add_argument("html_name", help="HTML file extracted from EPUB")
  args = parser.parse_args()

  # Open and read the HTML file
  with open(args.html_name, 'r', encoding='utf-8') as file:
      html_content = file.read()

  # Parse the HTML content using BeautifulSoup
  soup = BeautifulSoup(html_content, 'html.parser')

  # Find all header tags (h1, h2, ..., h5)
  # Note: h6 is reserved for notes and figures
  headers = soup.find_all(re.compile('^h[1-5]$'))

  # Iterate over each header and print it with indentation
  for header in headers:
      # Extract header level from the tag name (e.g., 'h2' -> level 2)
      level = int(header.name[1])
      # Calculate indentation (2 spaces per level beyond 1)
      indent = '  ' * (level - 1)
      # Get the header text
      text = header.get_text(strip=True)
      print(f"{indent}{text}")
