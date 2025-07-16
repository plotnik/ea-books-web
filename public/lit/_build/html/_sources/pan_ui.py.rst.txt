Pandoc UI
---------

- Get `Python Source`_.

.. _Python Source: ../../pan_ui.py  

.. csv-table:: Useful Links
   :header: "Name", "URL"
   :widths: 10 30

   "Pandoc User’s Guide", https://pandoc.org/MANUAL.html

::

  import streamlit as st
  import re
  import os
  import subprocess
  import pyperclip

Print banner.

::

  st.set_page_config(
      page_title="Pandoc-UI"
  )

  @st.cache_data
  def print_banner():
      print("""                 
                                  ,--.                            ,--. 
         ,---.  ,--,--.,--,--,  ,-|  | ,---.  ,---.,-----.,--.,--.`--' 
        | .-. |' ,-.  ||      \\' .-. || .-. || .--''-----'|  ||  |,--.
        | '-' '\\ '-'  ||  ||  |\\ `-' |' '-' '\\ `--.       '  ''  '| 
        |  |-'  `--`--'`--''--' `---'  `---'  `---'        `----' `--' 
        `--'                                                           
                                                                                             
      """)
      return 1

  print_banner()

Input and output formats.

::

  ext_names = {
      ".md": "Markdown",
      ".rst": "ReST",
      ".adoc": "AsciiDoc"
  }

  ext_formats = {
      ".md": "gfm", #"markdown",
      ".rst": "rst",
      ".adoc": "asciidoc"
  }

  def ext_name(name):
      return ext_names[name]

  i_ext = st.sidebar.radio(
      "Input format",
      options = [".md", ".rst"],
      format_func = ext_name,
  )

  o_ext = st.sidebar.radio(
      "Output format",
      options = [".md", ".rst", ".adoc"],
      format_func = ext_name,
      index = 2,
  )

Checks if ``output_folder`` exists in the user's home directory.

::

  home_directory = os.path.expanduser("~")
  output_folder = os.path.join(home_directory, ".a-services")
  if not os.path.exists(output_folder):
      os.makedirs(output_folder)

  temp_name = "pan_ui"
  input_file = os.path.join(output_folder, temp_name + i_ext)
  output_file = os.path.join(output_folder, temp_name + o_ext)    

When converting from ReST to Asciidoc using the Pandoc tool, the code snippets are surrounded by dots.
We can use a **custom Lua filter** in Pandoc to transform the code blocks into the desired format. 

::
    
  custom_codeblock = """
  function CodeBlock(el)
      local code = el.text
      local lang = el.classes[1] or "python" -- Get the first class as the language
      if lang ~= "" then
          return pandoc.RawBlock('asciidoc', '```' .. lang .. '\\n' .. code .. '\\n```\\n\\n')
      else
          return pandoc.RawBlock('asciidoc', '```\\n' .. code .. '\\n```\\n\\n')
      end
  end
  """

  lua_codeblock_file = os.path.join(output_folder, "custom_codeblock.lua")    
  with open(lua_codeblock_file, "w", encoding="utf-8") as fout:
      fout.write(custom_codeblock)
  
  lua_filter = "--lua-filter=" + lua_codeblock_file

Input number of headers to bump

::

  bump_headers_n = st.sidebar.number_input("Bump headers", value=0, min_value=0)

Convert text.

::

  text_area_height = 250

  text = st.text_area("Input text", height = text_area_height)

  cmd_line = ""

  def run_pandoc(input_file, output_file):
      with open(input_file, "w", encoding="utf-8") as fout:
          fout.write(text)

      cmd = ["pandoc", "-s", input_file, "-f", ext_formats[i_ext], "-t", ext_formats[o_ext], "-o", output_file]
      if o_ext == ".adoc": 
          cmd.insert(1, lua_filter)

      global cmd_line
      cmd_line = " ".join(cmd)
      subprocess.run(cmd, check=True)

      with open(output_file, "r", encoding="utf-8") as fin:
          result = fin.read()

      return result    
 
  def convert_text():
      try:
          result = run_pandoc(input_file, output_file)
          if o_ext == ".adoc": 
              result = asciidoc_headers(result)
              result = bump_headers(result, bump_headers_n)
    
          st.text_area(label = "Output text", value = result, height = text_area_height) 
        
          # Save result to clipboard
          pyperclip.copy(result)
          st.sidebar.write(f'Copied to clipboard')
        
      except Exception as e:
          st.error(e)
          st.write(f"```\n{cmd_line}\n```")

Remove lines that contain Pandoc's anchor markup: ``[[something]]``

::

  def asciidoc_headers(content):
      # This will remove the entire line if it matches, including the newline.
      cleaned_content = re.sub(r'^\[\[.*?\]\]\s*\n', '', content, flags=re.MULTILINE)
      return cleaned_content     

  def bump_headers(text: str, n: int) -> str:
      """Add n '=' characters to the start of each AsciiDoc header line."""
      if n == 0:
          return text

      prefix = '=' * n
      # Match lines starting with one or more '=' but not lines with only '=' (adornments)
      pattern = re.compile(r'^(=+)(?=\s)', re.MULTILINE)
      return pattern.sub(lambda m: prefix + m.group(1), text)
    
Click button.

::

  st.sidebar.write('---')
  if st.sidebar.button(':arrows_counterclockwise: &nbsp; Convert', type='primary', use_container_width=True):
      if i_ext == o_ext:
          st.error("Input and output formats shouldn't be the same!")
      elif text is None or text.strip() == '': 
          st.error("Input text is empty!")
      else:    
          convert_text()

    