Note-OpenAI
===========

This application is a lightweight text editor, similar to Notepad, enhanced with AI-assisted features powered by OpenAI.

It integrates with OpenAI's **Responses API** to provide intelligent text operations.

----

🧩 **OpenAI Models**
   https://platform.openai.com/docs/models

🏷️ **OpenAI Model Pricing**
   https://platform.openai.com/docs/pricing#latest-models

----

🧠 **Text generation**
   https://platform.openai.com/docs/guides/text

🪄 **Prompt engineering**
   https://platform.openai.com/docs/guides/prompt-engineering

🎛️ **Prompt Optimizer**
   https://platform.openai.com/chat/edit?models=gpt-5.2&optimize=true

🧭 **GPT-5.2 Prompting Guide**
   https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide

📚 **OpenAI Cookbook**
   https://cookbook.openai.com/
   
----

🔢 **Tiktoken CodeWiki**
   https://codewiki.google/github.com/openai/tiktoken

📏 **Tiktoken How-to Cookbook**
   https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken

----

::

  import streamlit as st
  from openai import OpenAI
  import yaml
  import tiktoken
  import platform
  import time
  import os
  import pyperclip

Prints a stylized banner to the console when the application starts.

::
    
  st.set_page_config(
      page_title="Note-AI",
  )

  @st.cache_data
  def print_banner():
      print("""
          _   __      __             ___    ____              
         / | / /___  / /____        /   |  /  _/              
        /  |/ / __ \\/ __/ _ \\______/ /| |  / /                
       / /|  / /_/ / /_/  __/_____/ ___ |_/ /                 
      /_/ |_/\\____/\\__/\\___/     /_/  |_/___/                                                       
      """)
      return 1

  print_banner()
  st.logo("https://ea-books.netlify.app/lit/ai_note.svg")

OpenAI client.

::

  client = OpenAI()

Reads prompts from a YAML configuration file (``openai_helper.yml``).  
Each prompt entry includes a unique name, a descriptive note explaining its purpose, and an optional list of tags for categorization.

The expected YAML structure is:

.. code-block:: yaml

   - name: grammar
     note: You will be provided with statements in markdown, and your task is to convert them to standard English.
     tags:
       - text

   - name: improve_style
     note: Improve style of the content you are provided.
     tags:
       - text

   - name: summarize_md
     note: You will be provided with statements in markdown, and your task is to summarize the content.
     tags:
       - text

   - name: explain_python
     note: Explain Python code you are provided.
     tags:
       - python

   - name: write_python
     note: Write Python code to satisfy the description you are provided.
     tags:
       - python

Each item in the list represents a single prompt and must define:

- ``name``: A short, unique identifier for the prompt.
- ``note``: Prompt body.
- ``tags``: A list of categories (for example, ``text`` or ``python``) that describe the prompt’s domain or usage.
   
::

  prompts_file = "openai_helper.yml"
  with open(prompts_file, 'r') as file:
      prompts = yaml.safe_load(file)

Text area to provide input text

::
    
  input_text = st.text_area(f"Note", height=300)

See: PersistedList_

.. _PersistedList: PersistedList.py.html

::

  from PersistedList import PersistedList
  tags_persisted = PersistedList(".tags")  
  prompts_persisted = PersistedList(".prompts")  

Read a list of strings from a file

::

  all_tags_set = {tag for item in prompts for tag in item.get('tags', [])}
  all_tags = tags_persisted.sort_by_pattern(list(all_tags_set))

  tag_name = st.sidebar.selectbox(
     "Category",
     all_tags,
  )  

Select prompt body by its name

::

  def get_prompt(name):
      for entry in prompts:
          if entry['name'] == name:
              return entry.get('note')
      return None

  def has_tag(name, tag_name):  
      for entry in prompts:
          if entry['name'] == name:
              return tag_name in entry.get('tags', [])
      return False
  
  all_prompt_names_set = {item['name'] for item in prompts}
  all_prompt_names = prompts_persisted.sort_by_pattern(list(all_prompt_names_set))
  prompt_names = [name for name in all_prompt_names if has_tag(name, tag_name)]

  prompt_name = st.sidebar.selectbox(
     "Prompt",
     prompt_names,
  )
  prompt = get_prompt(prompt_name)
  st.write(prompt)  

Select OpenAI LLM

::

  openai_prices = {
      "gpt-5.2": 1.75,
      "gpt-5.1": 1.25,
      "gpt-5": 1.25,
      "gpt-5-mini": 0.25,
      "gpt-5-nano": 0.05,

      "gpt-5.1-chat-latest": 1.25,
      "gpt-5.1-codex": 1.25,
  }    

  llm_models = list(openai_prices.keys())

Select LLM model

::

  llm_model = st.sidebar.selectbox(
     "LLM Model",
     llm_models
  )

Count the number of tokens in the user’s input using the ``tiktoken`` library, 
and display both the token count and the corresponding price.
 
::

  encoding = tiktoken.get_encoding("o200k_base")
  tokens = encoding.encode(input_text)

  cents = round(len(tokens) * openai_prices[llm_model]/10000, 5)

  st.sidebar.write(f'''
      | Chars | Tokens | Cents |
      |---|---|---|
      | {len(input_text)} | {len(tokens)} | {cents} |
      ''') 
    
.. function:: call_llm(text, prompt)

::

  def call_llm(text, prompt):
      response = client.responses.create(
          model=llm_model,
          instructions=prompt,
          input=input_text
      )
  
      return response.output_text

Run Query

::

  if st.button('Query', type="primary", icon=":material/cyclone:", width="stretch"):
      start_time = time.time()
  
      # Call LLM
      st.session_state.llm_output = call_llm(input_text, prompt)
      # st.write(st.session_state.llm_output)
  
      # Calculate and print execution time
      end_time = time.time()
      execution_time = end_time - start_time
      st.session_state.execution_time = end_time - start_time

      # Move selected tag to the beginning of the list
      all_tags = tags_persisted.select(tag_name)

      if platform.system() == 'Darwin':
          os.system("afplay /System/Library/Sounds/Glass.aiff")
      st.rerun()
    
LLM output is cached in ``session_state``.

::

  if "llm_output" not in st.session_state:
      st.stop()

  st.write('---')
  st.write(st.session_state.llm_output)
    
Show last execution time

::

  if "execution_time" in st.session_state:
      st.sidebar.write(f"Execution time: `{round(st.session_state.execution_time, 2)}` sec")
    
  if st.button("Clipboard", icon=":material/content_copy:"):
      pyperclip.copy(st.session_state.llm_output)
      st.write(f'Copied to clipboard')        