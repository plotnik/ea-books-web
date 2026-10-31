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

::

  import os
  import time
  from dataclasses import dataclass
  from pathlib import Path

  import pyperclip
  import streamlit as st

  from PersistedList import PersistedList

Print banner in ASCII graphics

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

Prompts and models
------------------

Resolve the user's Documents folder on Windows and Unix-like systems.
Remember selected prompt names separately from model names.

::

  prompts_folder = Path.home() / "Documents" / "prompts"
  prompt_files = {
      path.stem: path for path in sorted(prompts_folder.glob("*.md"))
      if path.is_file()
  }
  if not prompt_files:
      st.error(f"No Markdown prompts found in {prompts_folder}.")
      st.stop()

  prompts_persisted = PersistedList(".o-ai-prompts")
  prompt_names = prompts_persisted.sort_by_pattern(sorted(prompt_files))
  prompt_name = st.sidebar.selectbox("Prompt", prompt_names)
  prompts_persisted.select(prompt_name)
  prompt = prompt_files[prompt_name].read_text(encoding="utf-8")

  # Prices are USD per 1 million input/output tokens.
  llm_prices = {
      "gemini-4-argon": (2.00, 10.00),
      "gemini-3.8-flash": (0.75, 3.75),
      "gpt-6-luna": (0.10, 0.50),
      "gpt-6.1-terra": (1.00, 5.00),
      "gpt-6.1-sol": (2.00, 10.00),
  }
  llm_models = list(llm_prices.keys())
  llm_models_persisted = PersistedList(".o-ai")
  llm_models = llm_models_persisted.sort_by_pattern(llm_models)
  llm_model = st.sidebar.selectbox("LLM Model", llm_models)

Obsidian notes
--------------

Find the first book folder in the working directory and select a recent note.

::

  def reset_llm_result():
      for key in ("llm_result", "note_name", "execution_time", "llm_cost", "llm_usage"):
          st.session_state.pop(key, None)


  def find_obsidian_folder():
      current_folder = os.getcwd()
      home_folders = os.listdir(current_folder)
      book_folders = [
          item for item in home_folders
          if os.path.isdir(os.path.join(current_folder, item)) and item.endswith(" Book")
      ]
      if len(book_folders) == 0:
          raise ValueError('The folder should contain a subfolder with a name that ends with " Book".')
      return book_folders[0]


  def get_newest_files(directory, num_files):
      if not os.path.isdir(directory):
          raise ValueError(f"The directory {directory} does not exist.")
      files = [path for path in Path(directory).iterdir() if path.is_file()]
      files.sort(key=lambda path: path.stat().st_mtime, reverse=True)
      return [path.name for path in files[:num_files]]


  note_home = find_obsidian_folder()
  newest_files = get_newest_files(note_home, 5)
  if not newest_files:
      st.info(f"No notes found in {note_home}.")
      st.stop()
  note_name = st.selectbox("Note", newest_files, on_change=reset_llm_result)
  text = (Path(note_home) / note_name).read_text(encoding="utf-8")

LLM clients and pricing
-----------------------

Set OPENAI_API_KEY and GEMINI_API_KEY in the environment for the providers
you use. Clients are created only when processing a note.
Pre-request token counts are estimates; cost uses reported usage.

::

  @dataclass(frozen=True)
  class LLMResult:
      text: str
      input_tokens: int
      output_tokens: int


  def count_tokens(value: str) -> int:
      import tiktoken

      try:
          encoding = tiktoken.encoding_for_model(llm_model)
      except KeyError:
          # General-purpose fallback; Gemini counts are estimates only.
          encoding = tiktoken.get_encoding("o200k_base")
      return len(encoding.encode(value))


  def process_with_openai(text: str, prompt: str) -> LLMResult:
      from openai import OpenAI

      client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
      response = client.responses.create(
          model=llm_model,
          instructions=prompt.strip(),
          input=text,
      )
      return LLMResult(
          text=response.output_text,
          input_tokens=response.usage.input_tokens,
          output_tokens=response.usage.output_tokens,
      )


  def process_with_gemini(text: str, prompt: str) -> LLMResult:
      from google import genai
      from google.genai import types

      client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
      response = client.models.generate_content(
          model=llm_model,
          contents=text,
          config=types.GenerateContentConfig(system_instruction=prompt.strip()),
      )
      usage = response.usage_metadata
      # Gemini bills response and reasoning tokens at the output-token rate.
      output_tokens = (usage.candidates_token_count or 0) + (
          usage.thoughts_token_count or 0
      )
      return LLMResult(
          text=response.text or "",
          input_tokens=usage.prompt_token_count or 0,
          output_tokens=output_tokens,
      )


  def process_text(text: str, prompt: str) -> LLMResult:
      if llm_model.startswith("gpt-"):
          return process_with_openai(text, prompt)
      if llm_model.startswith("gemini-"):
          return process_with_gemini(text, prompt)
      raise ValueError(f"Unsupported model: {llm_model}")


  OPENAI_LONG_LIMIT_TOKENS = 272 * 1024


  def calculate_cost(result: LLMResult) -> float:
      input_price, output_price = llm_prices[llm_model]
      if llm_model.startswith("gpt-") and result.input_tokens > OPENAI_LONG_LIMIT_TOKENS:
          input_price *= 2
          output_price *= 1.5
      return (
          result.input_tokens * input_price + result.output_tokens * output_price
      ) / 1_000_000


  estimated_tokens = count_tokens(text) + count_tokens(prompt.strip())
  st.sidebar.write(f"Estimated input tokens: `{estimated_tokens:,}`")

Process and display the result
------------------------------

Store the cost with the result so changing the model does not reprice it.

::

  def call_llm():
      start_time = time.time()
      st.info(prompt)
      llm_models_persisted.select(llm_model)
      result = process_text(text, prompt)
      st.session_state.llm_result = result.text
      st.session_state.llm_usage = (result.input_tokens, result.output_tokens)
      st.session_state.llm_cost = calculate_cost(result)
      st.session_state.note_name = note_name
      st.session_state.execution_time = time.time() - start_time
      pyperclip.copy(result.text)
      st.rerun()


  if st.button("Process", type="primary", width="stretch"):
      call_llm()

  if "llm_result" in st.session_state:
      st.write("---")
      st.write(st.session_state.llm_result)
      st.write("---")

  if "execution_time" in st.session_state:
      st.sidebar.write(f"Execution time: `{st.session_state.execution_time:.1f}` sec")

  if "llm_cost" in st.session_state:
      input_tokens, output_tokens = st.session_state.llm_usage
      st.sidebar.write(f"Input tokens: `{input_tokens:,}`")
      st.sidebar.write(f"Output tokens: `{output_tokens:,}`")
      st.sidebar.write(f"Cents: `${st.session_state.llm_cost*100:.4f}`")

  if "llm_result" in st.session_state and st.sidebar.button("Copy to clipboard", width="stretch"):
      pyperclip.copy(st.session_state.llm_result)
