Udemy
=====

Summarize Udemy Transcript.

Similar to `Obsidian-AI`_, but directly from the book folder. 
Also can remove newlines from Udemy transcripts.


.. _Obsidian-AI: ai_obsidian.py.html

.. csv-table:: Useful Links
   :header: "Name", "URL"
   :widths: 10 30

   "Session State", https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
   "How to count tokens with tiktoken", https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
   "Model Pricing", https://platform.openai.com/docs/pricing#latest-models

.. contents::
 
::

  import streamlit as st
  import yaml
  import os
  import re
  import tiktoken
  from openai import OpenAI
  import platform
  import pyperclip
  import time
  import subprocess

See: PersistedList_

.. _PersistedList: PersistedList.py.html
  
::

  from PersistedList import PersistedList

Print banner.

::

  st.set_page_config(
      page_title="Udemy"
  )

  @st.cache_data
  def print_banner():
      print("""
       _____  _____      __                                       
      |_   _||_   _|    |  ]                                      
        | |    | |  .--.| | .---.  _ .--..--.    _   __           
        | '    ' |/ /'`\\' |/ /__\\\\[ `.-. .-. |  [ \\ [  ]      
         \\ \\__/ / | \\__/  || \\__., | | | | | |   \\ '/ /      
          `.__.'   '.__.;__]'.__.'[___||__||__][\\_:  /           
                                                \\__.'                  
      """)
      return 1

  print_banner()
  st.logo("https://ea-books.netlify.app/lit/udemy.svg")


Select OpenAI LLM.

::

  llm_prices = {
      "gpt-5.2": 1.75,
      "gpt-5.1": 1.25,

      "gpt-5.1-chat-latest": 1.25,
      "gpt-5.1-codex": 1.25,
    
      "gpt-5": 1.25,
      "gpt-5-mini": 0.25,
      "gpt-5-nano": 0.05,
        
      "o4-mini": 1.10,
      "o3-mini": 1.10,
      "o3": 2.0,
      "o3-pro": 20.0,
    
      "gemini-2.5-flash-preview-05-20": 0.0,
      "gemma-3-27b-it": 0.0,
      "gemini-2.0-flash": 0.0,
  }

  llm_temperature = 0.1

  def get_llm_properties(llm_model):
      if llm_model.startswith("gemini"):
          return {"google": True, "temperature": True, "xml": False}

      elif llm_model.startswith("gemma"):
          return {"google": True, "temperature": True, "xml": True}

      elif llm_model.startswith("gpt-4"):
          return {"google": False, "temperature": True, "xml": False}

      else: # o3 | gpt-5
          return {"google": False, "temperature": False, "xml": False}
        
  def reset_execution_time():
      if "execution_time" in st.session_state:
          del st.session_state["execution_time"]

Remember which LLM was used last time.

::

  llm_models = list(llm_prices.keys())
  llm_models_persisted = PersistedList(".udemy")
  llm_models = llm_models_persisted.sort_by_pattern(llm_models)

  llm_model = st.sidebar.selectbox(
      "LLM Models", 
      llm_models,
      on_change=reset_execution_time
  )

Obsidian folder
---------------

Find the Obsidian folder, which is the first subfolder within the current folder that has a name ending with " Book".

::

  current_folder = os.getcwd()
  home_folders = os.listdir(current_folder)
  book_folders = [item for item in home_folders if os.path.isdir(os.path.join(current_folder, item)) and item.endswith(" Book")]

  if (len(book_folders)==0):
      st.error('The folder should contain a subfolder with a name that ends with " Book".')
      st.stop()
  
  note_home =  book_folders[0]
  # print("OBSIDIAN_HOME: " + note_home)

Output file to save response.

::

  home_directory = os.path.expanduser("~")
  output_folder = os.path.join(home_directory, ".a-services")
  if not os.path.exists(output_folder):
      os.makedirs(output_folder)
    
  out_file = os.path.join(output_folder, 'udemy.txt')
  adoc_file = os.path.join(output_folder, 'udemy.adoc')

OpenAI and Gemini clients

::  

  client = OpenAI()

  g_key = os.getenv("GEMINI_API_KEY")
  g_client = OpenAI(
      api_key=g_key,
      base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
  )

Newest files 
------------

Get ``num_files`` newest files from the provided ``directory``.

::
    
  def get_newest_files(directory, num_files):
      # Check if the directory exists
      if not os.path.isdir(directory):
          raise ValueError(f"The directory {directory} does not exist.")

      # Get a list of files in the directory with their full paths and modification times
      files_with_paths = []
      for file_name in os.listdir(directory):
          file_path = os.path.join(directory, file_name)
          if os.path.isfile(file_path):
              files_with_paths.append((file_path, os.path.getmtime(file_path)))

      # Sort files by modification time in descending order (newest first)
      sorted_files = sorted(files_with_paths, key=lambda x: x[1], reverse=True)

      # Extract the num_files newest file names
      newest_files = [os.path.basename(file_with_path[0]) for file_with_path in sorted_files[:num_files]]

      return newest_files

Select ``note_name`` from 5 newest notes.

::

  newest_files = get_newest_files(note_home, 5)
  note_name = st.selectbox(
     "Note",
     newest_files,
  )

Load Obsidian note
------------------

::

  file_path = os.path.join(note_home, note_name)
  with open(file_path, 'r', encoding='utf-8') as file:
      text = file.read()

 
Write truncated input text

::
    
  # Truncate text to max len
  def max_len(text, k):
      if len(text) <= k:
          return text
      return text[:k] + '...'  

  st.write(f"""
 
  {max_len(text, 250)}
 
  """)

Tokens & price
--------------

::


  tiktoken_model = "o200k_base"
  #encoding = tiktoken.get_encoding(tiktoken_model) 
  encoding = tiktoken.encoding_for_model("gpt-4o-mini")
  tokens = encoding.encode(text)
  
Calculate price in cents.

::

  cents = round(len(tokens) * llm_prices[llm_model]/10000, 5)

  st.sidebar.write(f'''
      | Chars | Tokens | Cents |
      |---|---|---|
      | {len(text)} | {len(tokens)} | {cents} |
      ''')  
       
st.sidebar.divider()


Buttons to update text
----------------------

- Replace newlines with spaces, and
- Remove empty lines from text

::
    
  def remove_empty_lines_and_leading_hyphens(text):
      lines = text.splitlines()
      non_empty_lines = [line for line in lines if line.strip()]
    
      # Remove leading hyphens
      stripped = [
          line[1:].lstrip() if line.startswith('-') else line
          for line in non_empty_lines
      ]
    
      cleaned_text = '\n'.join(stripped)
      return cleaned_text

  def replace_newlines_with_spaces(input_string):
      # An inexpensive method to remove empty lines without using extra logic such as leading hyphens.
      return input_string.replace('\n', ' ')
 
  if st.button(':small_red_triangle_down: &nbsp; **Replace newlines with spaces**', use_container_width=True):
      text = remove_empty_lines_and_leading_hyphens(text)
    
      with open(file_path, 'w', encoding='utf-8') as file:
          file.write(text)
        
      st.rerun()    


Call OpenAI API
---------------

::
    
  prompt_summarize = """You will be provided with statements in markdown, 
  and your task is to summarize the content you are provided.
  """

  prompt_improve = """You will be provided with statements in markdown, 
  and your task is to improve the content you are provided.
  """
  prompt_questions = """
  You will be provided with context in markdown,
  and your task is to generate 3 questions this context can provide
  specific answers to which are unlikely to be found elsewhere.

  Higher-level summaries of surrounding context may be provided
  as well. Try using these summaries to generate better questions
  that this context can answer.
  """

  if 'openai_result' not in st.session_state:
      st.session_state.openai_result = ""
 
  def call_llm(text, prompt):
      llm_models_persisted.select(llm_model)
      props = get_llm_properties(llm_model)
      llm_client = g_client if props["google"] else client

      if props["xml"]:
          messages = [
              {"role": "user", "content": f"<prompt>{prompt}</prompt>\n<query>{text}</query>"},
          ]
      else:
          messages = [
              {"role": "developer", "content": prompt},
              {"role": "user", "content": text},
          ]

      if props["temperature"]:
          response = llm_client.chat.completions.create(
              model=llm_model,
              messages=messages,
              temperature=llm_temperature,
          )
      else:
          response = llm_client.chat.completions.create(
              model=llm_model,
              messages=messages,
          )

      choice = response.choices[0]
      out_text = choice.message.content
      st.session_state.openai_result = out_text

      st.write(st.session_state.openai_result)

      with open(out_file, 'w') as file:
          file.write(out_text)
      st.sidebar.write(f'Response saved: `{out_file}`')  

      if platform.system() == 'Darwin':
          os.system("afplay /System/Library/Sounds/Glass.aiff")

Show OpenAI result.

::

  # st.write('---')
  st.write(st.session_state.openai_result)
  # st.write('---')

  if st.sidebar.button(':sparkles: &nbsp; Summarize', use_container_width=True):
      start_time = time.time()
      call_llm(text, prompt_summarize)
      end_time = time.time()
      st.session_state.execution_time = end_time - start_time
      st.rerun()
    
  if st.sidebar.button(':question: &nbsp; Ask questions', use_container_width=True):
      start_time = time.time()
      call_llm(text, prompt_questions)
      end_time = time.time()
      st.session_state.execution_time = end_time - start_time
      st.rerun()
 
  if st.sidebar.button(':thumbsup: &nbsp; Improve', use_container_width=True):
      start_time = time.time()
      call_llm(text, prompt_improve)
      end_time = time.time()
      st.session_state.execution_time = end_time - start_time
      st.rerun()
 
Convert to Asciidoc

::

  def convert_to_asciidoc(markdown):
      subprocess.run(["pandoc", "-f", "gfm", "-s", out_file, "-o", adoc_file], check=True)
      with open(adoc_file, "r", encoding="utf-8") as fin:
          result = fin.read()    
      return result

Copy to clipboard

::

  if len(st.session_state.openai_result) > 0:
      if st.sidebar.button(':clipboard: &nbsp; Copy to clipboard', type='primary', use_container_width=True):
          pyperclip.copy(st.session_state.openai_result)
          st.toast(f'Copied to clipboard')
        
Copy Asciidoc to clipboard

::

  def bump_headers(text: str, n: int) -> str:
      """Add n '=' characters to the start of each AsciiDoc header line."""
      if n == 0:
          return text
        
      prefix = '=' * n
      # Match lines starting with one or more '=' but not lines with only '=' (adornments)
      pattern = re.compile(r'^(=+)(?=\s)', re.MULTILINE)
      return pattern.sub(lambda m: prefix + m.group(1), text)
    
  def asciidoc_headers(content):
      # This will remove the entire line if it matches, including the newline.
      cleaned_content = re.sub(r'^\[\[.*?\]\]\s*\n', '', content, flags=re.MULTILINE)
      return cleaned_content
    
  bump_headers_n = st.sidebar.number_input("Bump headers", value=0, min_value=0)

  if len(st.session_state.openai_result) > 0:
      if st.sidebar.button(':clipboard: &nbsp; Copy Asciidoc to clipboard', type='primary', use_container_width=True):
          pyperclip.copy(asciidoc_headers(bump_headers(convert_to_asciidoc(st.session_state.openai_result), bump_headers_n)))
          st.toast(f'Copied to clipboard')
        
Show last execution time

::

  if "execution_time" in st.session_state:
      st.sidebar.write(f"Execution time: `{round(st.session_state.execution_time, 2)}` sec")
 



