Doc-Note
========

Convert Note-AI_ XML results to AsciiDoc

.. _Note-AI: ai_note.py.html

::

  import streamlit as st
  import xml.etree.ElementTree as ET
  import os
  import subprocess
  import textwrap

Print banner.

::

  @st.cache_data
  def print_banner():
      print("""
           _                             _                
        __| | ___   ___      _ __   ___ | |_ ___          
       / _` |/ _ \\ / __|____| '_ \\ / _ \\| __/ _ \\     
      | (_| | (_) | (_|_____| | | | (_) | ||  __/         
       \\__,_|\\___/ \\___|    |_| |_|\\___/ \\__\\___|   
      """)
      return 1

  print_banner()

Get ``num_files`` newest files with ``extension``
from the provided ``directory``.

::
    
  def get_newest_files(directory, num_files, extension):
      # Check if the directory exists
      if not os.path.isdir(directory):
          raise ValueError(f"The directory {directory} does not exist.")

      # Get a list of files in the directory with their full paths and modification times
      files_with_paths = []
      for file_name in os.listdir(directory):
          file_path = os.path.join(directory, file_name)
          if os.path.isfile(file_path) and file_name.endswith(extension):
              files_with_paths.append((file_path, os.path.getmtime(file_path)))

      # Sort files by modification time in descending order (newest first)
      sorted_files = sorted(files_with_paths, key=lambda x: x[1], reverse=True)

      # Extract the num_files newest file names
      newest_files = [os.path.basename(file_with_path[0]) for file_with_path in sorted_files[:num_files]]

      return newest_files

  newest_files = get_newest_files(".", 5, ".xml")
  note_name = st.selectbox(
     "Note",
     newest_files,
  )

  with open(note_name, 'r') as file:
      xml_data = file.read()

Parse XML

::
    
  root = ET.fromstring(xml_data)

Extract the question and answer

::
    
  question = root.find('question').text
  answer = root.find('answer').text
  prompt = root.find('prompt').text

Button

::
    
  if st.button("Convert to AsciiDoc"):
      fname = note_name[:-len(".xml")]

      # Step 1: Save the markdown content to a "{fname}.md" file
      md_filename = f"a/{fname}.md"
      with open(md_filename, 'w') as file:
          file.write(answer)

      # Step 2: Run pandoc to convert markdown to asciidoc
      adoc_filename = f"a/{fname}.adoc"
      subprocess.run(["pandoc", "-s", md_filename, "-o", adoc_filename], check=True)

      # Step 3: Delete the markdown file
      os.remove(md_filename)

      # Step 4: Add header to the "{fname}.adoc" file
      header = textwrap.dedent(f"""\
          = {fname}.java
          :icons: font
          :source-highlighter: coderay
          """)
      with open(adoc_filename, 'r+') as adoc_file:
          original_content = adoc_file.read()
          # Move to the start of the file
          adoc_file.seek(0)  
          # Write the new header and original content
          adoc_file.write(header + 
              f"\n*{prompt}*\n\n" + 
              original_content + 
              f"\n---\n```java\n{question}\n```\n") 
    
      # Step 5: Run asciidoctor to convert asciidoc to html
      subprocess.run(["asciidoctor", adoc_filename], check=True)

      st.write(f'AsciiDoc generated')

  st.divider()
  st.write(answer)