Obsidian-AI
===========

Summarize Obsidian_ page.

- Get `Python Source`_.

Script is written in `literate programming`_.

- See `PyLit Tutorial`_
- See `reStructuredText Primer`_

.. _Obsidian: https://obsidian.md/
.. _Python Source: ../../ai_obsidian.py
.. _literate programming: https://en.wikipedia.org/wiki/Literate_programming
.. _reStructuredText Primer: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _PyLit Tutorial: https://slott56.github.io/PyLit-3/_build/html/tutorial/index.html

.. csv-table:: Useful Links
   :header: "Name", "URL"
   :widths: 10 30

   "OpenAI API Examples", https://platform.openai.com/examples
   "How to count tokens with tiktoken", https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken

::

  import streamlit as st
  import yaml
  import json
  import os
  import tiktoken
  from openai import OpenAI
  import pyperclip
  from typing import List
  import time

  from pathlib import Path
  from typing import List
  from collections import namedtuple

Print banner.

::

  st.set_page_config(
      page_title="O-AI"
  )

  @st.cache_data
  def print_banner():
      print("""
         dBBBBP       dBBBBBb     dBP
        dB'.BP             BB        
       dB'.BP          dBP BB   dBP  
      dB'.BP dBBBBBP  dBP  BB  dBP   
     dBBBBP          dBBBBBBB dBP                                                                          
      """)
      return 1

  print_banner()
  st.logo("https://ea-books.netlify.app/lit/ai_obsidian.svg")

Prompts
-------

::

  prompt_summary = """You will be provided with statements in markdown, 
  and your task is to summarize the content you are provided."""

  prompt_summary_v2 = """You will be provided with statements in markdown, 
  and your task is to summarize the key topics and entities you are provided."""

  prompt_questions = """
  You will be provided with context in markdown, 
  and your task is to generate 3 questions this context can provide 
  specific answers to which are unlikely to be found elsewhere.

  Higher-level summaries of surrounding context may be provided 
  as well. Try using these summaries to generate better questions 
  that this context can answer.
  """

  prompt_questions_v2 = """
  Given the provided context, generate 3 highly specific questions that:

  - Can be answered precisely using only this context.
  - Are unlikely to have answers easily found elsewhere.
  - Benefit from any provided higher-level summaries of surrounding context.

  Prioritize specificity and uniqueness in each question.
  """

  prompt_improve = """You will be provided with statements in markdown,
  and your task is to improve the content you are provided.
  """

  prompt = prompt_summary

Select LLM
----------

.. csv-table:: Useful Links
   :header: "Name", "URL"
   :widths: 10 30

   "OpenAI Models", https://platform.openai.com/docs/models
   "Gemini Models", https://ai.google.dev/gemini-api/docs/models

::

  llm_prices = {
      "gemini-2.5-flash-preview-05-20": 0.0,
      "gemma-3-27b-it": 0.0,
      "gemini-2.0-flash": 0.0,

      "gpt-4.1-mini": 0.4,
      "gpt-4.1-nano": 0.1,
      "gpt-4.1": 2.0,
      "gpt-4o-mini": 0.15,
      "gpt-4o": 2.5,

      "o3-mini": 1.10,
      "o3": 2.0,
      "o3-pro": 20.0,
  }

  def get_llm_properties(llm_model):
      if llm_model.startswith("gemini"):
          return {"google": True, "temperature": True, "xml": False}
        
      elif llm_model.startswith("gemma"): 
          return {"google": True, "temperature": True, "xml": True}
    
      elif llm_model.startswith("gpt"): 
          return {"google": False, "temperature": True, "xml": False}
        
      else: #o3
          return {"google": False, "temperature": False, "xml": False}
        
Persisted List   
--------------    

.. csv-table:: History
   :header: "Date", "Comment"
   :widths: 10 30

   "2025-06-13", "New elements come first"
   "", "Copied from: `explain_java.py`_"

.. _explain_java.py: explain_java.py.html#persisted-list
  
::

  class PersistedList:
      """
      A tiny helper that remembers a list of strings on disk.
      """

      def __init__(self, filename: str) -> None:
          self.filename = Path(filename)
          self.names: List[str] = self._read_from_file()

      # ──────────────────────────────────────────────────────────────
      # Private helpers
      # ──────────────────────────────────────────────────────────────

      def _read_from_file(self) -> List[str]:
          """
          Return the list stored on disk (empty if the file is missing).
          """
          if self.filename.exists():
              with self.filename.open("r", encoding="utf-8") as fh:
                  return [line.strip() for line in fh if line.strip()]
          return []

      def _write_to_file(self) -> None:
          """
          Persist the current list to disk (one item per line).
          """
          self.filename.parent.mkdir(parents=True, exist_ok=True)
          with self.filename.open("w", encoding="utf-8") as fh:
              fh.write("\n".join(self.names))

      @staticmethod
      def _remove_strings(source: List[str], to_remove: List[str]) -> List[str]:
          """
          Return a copy of *source* without any element that occurs in *to_remove*.
          """
          removal_set = set(to_remove)
          return [s for s in source if s not in removal_set]

      # ──────────────────────────────────────────────────────────────
      # Public API
      # ──────────────────────────────────────────────────────────────

      def sort_by_pattern(self, all_names: List[str]) -> List[str]:
          """
          Sort *all_names* so that previously‑stored names keep their old
          ordering, and every new name is appended alphabetically.
          The internal list is updated and re‑written to disk.
          """
          priority = {name: idx for idx, name in enumerate(self.names)}

          sortd_names = sorted(
              all_names,
              key=lambda n: (1, priority[n]) if n in priority else (0, n)
          )

          self.names = sorted_names
          self._write_to_file()
          return sorted_names

      def select(self, selected_name: str) -> None:
          """
          Move *selected_name* to the top of the list (inserting it if it
          wasn’t present) and persist the change.
          """
          self.names = self._remove_strings(self.names, [selected_name])
          self.names.insert(0, selected_name)
          self._write_to_file()

      # ──────────────────────────────────────────────────────────────
      # Convenience
      # ──────────────────────────────────────────────────────────────

      def __iter__(self):
          return iter(self.names)

      def __repr__(self) -> str:
          return f"{self.__class__.__name__}({self.filename!s}, {self.names})"

Select LLM.
Remember which LLM was used last time.
::

  llm_models = list(llm_prices.keys())
  llm_models_persisted = PersistedList(".o-ai") 
  llm_models = llm_models_persisted.sort_by_pattern(llm_models)

  llm_temperatures = [0, 0.1, 0.7, 1]

  llm_model = st.sidebar.selectbox(
     "LLM Model",
     llm_models,
     index = 0
  )

  llm_temperature = st.sidebar.select_slider(
     "LLM Temperature",
     options = llm_temperatures,
     value = 0.1
  )

Select Obsidian folder from recent vaults.

::

  def reset_llm_result():
      if "llm_result" in st.session_state:
          del st.session_state["llm_result"]
      if "note_name" in st.session_state:
          del st.session_state["note_name"]
    
  home_folder = os.path.expanduser('~')
  obsidian_json_path = f"{home_folder}/Library/Application Support/obsidian/obsidian.json"
  with open(obsidian_json_path, "r") as json_file:
      obsidian_json = json.load(json_file)

  obsidian_vaults = obsidian_json.get('vaults')

  # Extract the values from the dictionary and sort them based on the 'ts' key
  sorted_vaults = sorted(obsidian_vaults.values(), key=lambda x: x['ts'], reverse=True)

  # Extract the 'path' from each sorted entry
  obsidian_folders = [vault['path'] for vault in sorted_vaults]

  note_home = st.selectbox(
     "Obsidian folder",
     obsidian_folders,
     on_change=reset_llm_result
  )

Load LLM prompts.

::

  prompts_file = "openai_helper.yml"
  with open(prompts_file, 'r') as file:
      prompts = yaml.safe_load(file)

  def get_prompt(name):
      for entry in prompts:
          if entry['name'] == name:
              return entry.get('note')
      return None

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
     on_change=reset_llm_result
  )

Get the number of tokens.

::

  file_path = os.path.join(note_home, note_name)
  with open(file_path, 'r', encoding='utf-8') as file:
      text = file.read()

Tokens & Price
--------------

Certain models are not compatible with ``tiktoken 0.7.0``, 
so we have added a separate configuration for them.

::

  def count_tokens():
      llm_model_tiktoken = "gpt-4o-mini"

      encoding = tiktoken.encoding_for_model(llm_model_tiktoken)
      tokens = encoding.encode(text)

      cents = round(len(tokens) * llm_prices[llm_model]/10000, 5)

      st.sidebar.write(f'''
          | Characters | Tokens | Cents |
          |---|---|---|
          | {len(text)} | {len(tokens)} | {cents} |
          ''')

  #if llm_model.startswith("gpt-") or llm_model.startswith("o-"):
  count_tokens()
 

OpenAI and Gemini clients

::

  client = OpenAI()

  g_key = os.getenv("GEMINI_API_KEY")
  g_client = OpenAI(
      api_key=g_key,
      base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
  )

Generic LLM call.

::

  def call_llm():
      start_time = time.time()

      st.write('')
      st.info(prompt, icon="🤔")

      # Remember LLM to push it to the top of selectbox
      llm_models_persisted.select(llm_model)

      # Call LLM
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
  
      # Save result in session       
      st.session_state.llm_result = choice.message.content 
      st.session_state.note_name = note_name

      # Save result to clipboard  
      pyperclip.copy(st.session_state.llm_result)
      st.write(f'Copied to clipboard')

      end_time = time.time()
      st.session_state.execution_time = end_time - start_time

      st.rerun()

Print result

::

  if "llm_result" in st.session_state:
      st.write('---')
      st.write(st.session_state.llm_result)
      st.write('---')  

  if "execution_time" in st.session_state:
      st.sidebar.write(f"Execution time: `{round(st.session_state.execution_time, 1)}` sec")    

Sidebar buttons

::    

  st.write('')
  if st.button(':bulb: &nbsp; Summarize', type='primary', use_container_width=True):
      prompt = prompt_summary
      call_llm()

  if st.sidebar.button(':question: &nbsp; Ask questions', use_container_width=True):
      prompt = prompt_questions
      call_llm()

  if st.sidebar.button(':exclamation: &nbsp; Improve', use_container_width=True):
      prompt = prompt_improve
      call_llm()

  if "llm_result" in st.session_state and st.sidebar.button(':clipboard: &nbsp; Copy to clipboard', use_container_width=True):
      pyperclip.copy(st.session_state.llm_result)
    
  st.sidebar.write('---')

  if st.sidebar.button(f' `Summarize` {"&nbsp;"*8} :test_tube: `v.2`'):
      prompt = prompt_summary_v2
      call_llm()

  if st.sidebar.button(f'`Ask questions` :test_tube: `v.2`'):
      prompt = prompt_questions_v2
      call_llm()




