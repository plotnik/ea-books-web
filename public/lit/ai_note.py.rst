=======
Note-AI
=======

Running OpenAI prompts.

To set up the environment you can install Miniconda_.
For details see `Environment Setup`_.

.. _Miniconda: https://docs.conda.io/projects/miniconda/en/latest/

.. contents::

.. csv-table:: Useful Links
   :header: "Name", "URL"
   :widths: 10 30

   "Examples of OpenAI prompts", https://platform.openai.com/examples

::

  import streamlit as st
  from openai import OpenAI
  import yaml
  import tiktoken
  import textwrap
  import platform
  import time
  import os

Print banner.

::

  @st.cache_data
  def print_banner():
      print("""
          _   __      __             ___    ____
         / | / /___  / /____        /   |  /  _/
        /  |/ / __ \/ __/ _ \______/ /| |  / /  
       / /|  / /_/ / /_/  __/_____/ ___ |_/ /   
      /_/ |_/\____/\__/\___/     /_/  |_/___/                                                        
      """)
      return 1

  print_banner()

Select OpenAI LLM.

.. csv-table:: Useful Links
   :header: "Name", "URL"
   :widths: 10 30

   "OpenAI Models", https://platform.openai.com/docs/models

::

  openai_model = "gpt-4o-mini"
  openai_temperature = 0.7

Create OpenAI client.

::

  client = OpenAI()

Load LLM prompts
----------------

::

  prompts_file = "openai_helper.yml"
  with open(prompts_file, 'r') as file:
      prompts = yaml.safe_load(file)

  def get_prompt(name):
      for entry in prompts:
          if entry['name'] == name:
              return entry.get('note')
      return None

  text = st.text_area(f"Note", height=300)

Select the prompt.

::

  prompt_names = [item['name'] for item in prompts]
  prompt_name = st.sidebar.selectbox(
     "Prompt",
     prompt_names,
  )
  prompt = get_prompt(prompt_name)
  st.write(prompt)
  # print(f"Prompt: {prompt_name} for {openai_model}")

Count tokens
------------

We can use emojis in buttons

.. csv-table:: Useful Links
   :header: "Name", "URL"
   :widths: 10 30

   "Streamlit emoji shortcodes", https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
   "Emoji Cheat Sheet", https://www.webfx.com/tools/emoji-cheat-sheet/

::
    
  if st.sidebar.button(':thermometer: &nbsp; Count Tokens'):

      encoding = tiktoken.encoding_for_model(openai_model)
      tokens = encoding.encode(text)
      st.write('---')
      st.write(f'Tokens: `{len(tokens)}`')


Call OpenAI API
---------------

``openai_result`` is cached in ``session_state``.

::

  if "openai_result" not in st.session_state:
      st.session_state.openai_result = ''

  st.write('---')
  st.write(st.session_state.openai_result)

  st.sidebar.write('---')
  if st.sidebar.button(':thinking_face: &nbsp; Call OpenAI', type="primary"):

      start_time = time.time()
      response = client.chat.completions.create(
              model=openai_model,
              messages=[
                  {"role": "system", "content": prompt},
                  {"role": "user", "content": text},
              ],
              temperature=openai_temperature,
          )

      choice = response.choices[0]
      st.session_state.openai_result = choice.message.content
      st.write(st.session_state.openai_result)

      # print('---')
      # print(f'finish_reason: `{choice.finish_reason}`')
      # print(response.usage)
      # print(f'Choices: {len(response.choices)}')

      # Calculate and print execution time
      end_time = time.time()
      execution_time = end_time - start_time
      # print(f'Execution time: `{execution_time:.1f}` seconds')

      if platform.system() == 'Darwin':
          os.system("afplay /System/Library/Sounds/Glass.aiff")
      st.rerun()

Save note
---------

Notes will be saved to ``ai_note`` folder which is expected to exist.

Output format can be XML with request, response and prompt name, or just response markdown.

::

  def save_note_disabled():
      return len(note_name.strip())==0

  note_name = st.text_input("Note Name:")

  out_format = st.radio("Output Format:", ["XML", "Markdown"], horizontal=True)

  if st.button(':spiral_note_pad: Save', disabled=save_note_disabled()):
      if out_format == "XML":
          xml = textwrap.dedent(f"""
              <note>
                <question><![CDATA[{text}]]></question>
                <prompt>{prompt_name}</prompt>
                <answer><![CDATA[{st.session_state.openai_result}]]></answer>
              </note>
          """).strip()
          out_file = f"ai_note/{note_name}.xml"
          with open(out_file, 'w') as file:
              file.write(xml)
          st.write(f'Note saved: `{out_file}`')
      else:    
          out_file = f"ai_note/{note_name}.md"
          with open(out_file, 'w') as file:
              file.write(st.session_state.openai_result)
          st.write(f'Note saved: `{out_file}`')
      
Environment Setup
-----------------

To set up your environment using Miniconda_, follow the steps below.
These instructions will guide you through installing Miniconda,
configuring your environment, and running a Streamlit application
tailored for AI tasks.

Step 1: Install Miniconda
=========================

First, you need to install Miniconda. Visit the `Miniconda
website <https://docs.conda.io/en/latest/miniconda.html>`__ and follow
the installation instructions for your operating system.

Step 2: Configure Your Environment
==================================

1. **Create the Environment File**

   Create a file named ``environment.yml`` in your project directory.
   Paste the following contents into this file:

   .. code:: yaml

      name: ai_note
      channels:
        - conda-forge
        - defaults
      dependencies:
        - python=3.11.0
        - openai
        - tiktoken
        - streamlit

2. **Select conda-forge Channel**

   Open your terminal or command prompt and execute the following
   commands to prioritize the ``conda-forge`` channel:

   .. code:: shell

      conda config --add channels conda-forge
      conda config --set channel_priority strict

3. **Create the Environment**

   Still in your terminal, navigate to the directory containing your
   ``environment.yml`` file. Create the Conda environment by running:

   .. code:: shell

      conda env create -f environment.yml

Step 3: Activate the Environment
================================

Activate your newly created environment by executing:

.. code:: shell

   conda activate ai_note

Step 4: Prepare Prompt File
===========================

Create a file named ``openai_helper.yml`` in your project directory.
This file should contain various prompts for the tasks you want to
accomplish. Here’s an example of how to structure the contents:

.. code:: yaml

   - name: summarize_md
     note: You will be provided with statements in markdown, and your task is to summarize the content.

   - name: explain_python
     note: Explain Python code you are provided.

   - name: write_python
     note: Write Python code to satisfy the description you are provided.

   - name: write_groovy
     note: Write Groovy code to satisfy the description you are provided.

   - name: improve_style
     note: Improve style of the content you are provided.

Step 5: Run Streamlit Script
============================

With your environment set up and activated, and your
``openai_helper.yml`` file ready, you’re now set to run your Streamlit
application. Execute the following command in your terminal:

.. code:: shell

   streamlit run ai_note.py

And that’s it! Your Streamlit application should now be running, and you
can interact with it through your web browser.