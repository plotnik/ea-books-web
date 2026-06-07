Fonts
=====

Create a system font table in `fonts.html`.

Requires:
  pip install matplotlib
     
::


  from pathlib import Path
  from html import escape
  from matplotlib import font_manager


  def get_system_font_names():
      fonts = font_manager.findSystemFonts(fontpaths=None, fontext="ttf")
      fonts += font_manager.findSystemFonts(fontpaths=None, fontext="otf")

      names = set()

      for font_path in fonts:
          try:
              prop = font_manager.FontProperties(fname=font_path)
              name = prop.get_name()
              if name:
                  names.add(name)
          except Exception:
              # Some font files may be unreadable or unsupported
              pass

      return sorted(names, key=str.casefold)


  def main():
      font_names = get_system_font_names()

      html_parts = [
          """<html>
  <head>
    <title>System Fonts</title>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  </head>
  <body>
  <ul>
  """
      ]

      prev_ch = None

      for i, font_name in enumerate(font_names):
          first_ch = font_name[0].upper() if font_name else ""

          if first_ch != prev_ch:
              if prev_ch is not None:
                  html_parts.append("</li>\n")
              html_parts.append("<li>\n")
              prev_ch = first_ch

          print(f"{i}: {font_name}")

          safe_font_name = escape(font_name, quote=True)

          html_parts.append(
              f'<span style="font-family: \'{safe_font_name}\', sans-serif;">'
              f'{safe_font_name} '
              f'<span style="color: silver;">зпт</span>'
              f'</span>\n'
          )

      if prev_ch is not None:
          html_parts.append("</li>\n")

      html_parts.append(
          """</ul>
  </body>
  </html>
  """
      )

      Path("fonts.html").write_text("".join(html_parts), encoding="utf-8")

      print("---------------")
      print(f"total: {len(font_names)}")


  if __name__ == "__main__":
      main()