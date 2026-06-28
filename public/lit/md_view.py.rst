Markdown Viewer
===============

::

  import os
  import streamlit as st
  from md_utils import save_html

Print banner.

::

  st.set_page_config(
      page_title="MD-View",
  )

  @st.cache_data
  def print_banner():
    print("""                                                    
      d s   sb d ss         d    b d d sss   d  d  b                   
      S  S S S S   ~o       S    S S S       S  S  S                   
      S   S  S S     b      S    S S S       S  S  S                   
      S      S S     S sSSs S    S S S sSSs  S  S  S                   
      S      S S     P      S    S S S       S  S  S                   
      S      S S    S        S   S S S        S  S S                   
      P      P P ss\"          \"ssS P P sSSss   \"ss\"S                                                                                           
    """)
    return 1

  print_banner()

We can show ``.q.md`` files only.

::
    
  if st.sidebar.toggle("Questions only"):
      md_files = [f for f in os.listdir('.') if f.endswith('.q.md')]

  else:

Find all files in the current directory with a ``.md`` extension (these may contain LLM-generated text).

Exclude any question files with the ``.q.md`` suffix. If a response file corresponds to a specific question, that question will be stored separately in a file sharing the same base name and ending in ``.q.md``; do not include those ``.q.md`` files in the final list.

::

      md_files = [f for f in os.listdir('.') if f.endswith('.md') and not f.endswith('.q.md')]

Sort files based on their modification time

::

  md_files.sort(key=os.path.getmtime, reverse=True)

Create radio buttons to select a file

::

  selected_file = st.sidebar.radio("Markdown file:", md_files)

Adds a prefix to each line of a multi-line string.

::

  def prefix_lines(query, prefix):
      lines = query.splitlines()
      prefixed_lines = [prefix + line for line in lines]
      return "\n".join(prefixed_lines)

Check if query file exists.

::

  query_file_path = selected_file[:-3] + ".q.md"
  if os.path.exists(query_file_path):
      with open(query_file_path, 'r', encoding='utf-8') as file:
          query = file.read()
      st.write("### Query")      
      st.write(prefix_lines(query, "> "))     
      st.write("---");
    
Check if summary file exists.

::

  summary_file_path = f".md-view/{selected_file[:-3]}.summary.md"
  if os.path.exists(summary_file_path):
      with open(summary_file_path, 'r', encoding='utf-8') as file:
          summary = file.read()
      st.write("### Summary")     
      st.write(prefix_lines(summary, "> ")) 
      st.write("---");
    
Read the contents of selected file

::

  with open(selected_file, 'r', encoding='utf-8') as file:
      md_text = file.read()

Display the contents of the file that has been selected.

::
    
  st.write(md_text)    

  html_format = st.sidebar.radio("Output HTML:", options=["Tailwind", "Bootstrap"], horizontal=True)

Add a button to save the markdown text as an HTML file

::

  if st.sidebar.button("Save HTML", use_container_width=True):
      save_html(md_text, selected_file[:-3], html_format)
      st.toast(f"HTML file saved")  

Summarize

::

  prompt_summarize = """You will be provided with statements in markdown,
  and your task is to summarize the content you are provided.
  """

  from openai import OpenAI

  class OpenAI_Helper:
     
      def __init__(self):
          self.client = OpenAI()
          self.llm_model = "gpt-5-mini"
        
      def call_llm(self, input_text, prompt):
          response = self.client.responses.create(
              model=self.llm_model,
              instructions=prompt,
              input=input_text
          )
    
          return response.output_text

  openai_helper = OpenAI_Helper()

  def summarize(md_text, filename):
      summary = openai_helper.call_llm(md_text, prompt_summarize)
      print(summary)
    
  if st.sidebar.button("Summarize", use_container_width=True):
      summarize(md_text, selected_file[:-3])