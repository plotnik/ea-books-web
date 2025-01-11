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

Print banner.

::

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

  def ext_name(name):
      return ext_names[name]

  i_ext = st.sidebar.radio(
      "Input format",
      options = [".md", ".rst"],
      format_func = ext_name,
  )

  o_ext = st.sidebar.radio(
      "Output format",
      options = [".rst", ".adoc"],
      format_func = ext_name,
  )

Checks if ``output_folder`` exists in the user's home directory.

::

  home_directory = os.path.expanduser("~")
  output_folder = os.path.join(home_directory, ".a-services")
  if not os.path.exists(output_folder):
      os.makedirs(output_folder)

Convert text.

::

  text_area_height = 250

  text = st.text_area("Input text", height = text_area_height)
  
  def run_pandoc(input_file, output_file):
      with open(input_file, "w", encoding="utf-8") as fout:
          fout.write(text)
  
      if i_ext == ".md":
          subprocess.run(["pandoc", "-f", "gfm", "-s", input_file, "-o", output_file], check=True)   
      else:    
          subprocess.run(["pandoc", "-s", input_file, "-o", output_file], check=True)

      with open(output_file, "r", encoding="utf-8") as fin:
          result = fin.read()
  
      return result    
 
  def convert_text():
      temp_name = "pan_ui"
      input_file = os.path.join(output_folder, temp_name + i_ext)
      output_file = os.path.join(output_folder, temp_name + o_ext)    

      result = run_pandoc(input_file, output_file)
      if o_ext == ".adoc": 
          result = asciidoc_headers(result)
  
      st.text_area(label = "Output text", value = result, height = text_area_height) 
  
Remove lines that contain Pandoc's anchor markup: ``[[something]]``

::

  def asciidoc_headers(content):
      # This will remove the entire line if it matches, including the newline.
      cleaned_content = re.sub(r'^\[\[.*?\]\]\s*\n', '', content, flags=re.MULTILINE)
      return cleaned_content     

Click button.

::

  st.sidebar.write('---')
  if st.sidebar.button('Convert', type='primary'):
      if i_ext == o_ext:
          st.error("Input and output formats shouldn't be the same!")
      elif text is None or text.strip() == '': 
          st.error("Input text is empty!")
      else:    
          convert_text()

      