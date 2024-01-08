Call OpenAI API
===============

.. csv-table:: Useful Links
   :header: "Name", "URL"
   :widths: 10 30

   "How to count tokens with tiktoken", https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken

::

  import streamlit as st
  import yaml
  import os
  from dotenv import load_dotenv
  import tiktoken
  from openai import OpenAI

Select OpenAI LLM.

::

  openai_model = "gpt-4-1106-preview"

Get Obsidian folder from ``.env`` file.

::

  load_dotenv()
  note_home =  os.getenv("OBSIDIAN_HOME")

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
  )

Get the number of tokens.

::

  file_path = os.path.join(note_home, note_name)
  with open(file_path, 'r', encoding='utf-8') as file:
      text = file.read()

  encoding = tiktoken.encoding_for_model(openai_model)
  tokens = encoding.encode(text)

  st.write(f'Tokens: `{len(tokens)}`')  

Select the prompt.

::

  prompt_names = [item['name'] for item in prompts]
  prompt_name = st.selectbox(
     "Prompt",
     prompt_names,
  )

  prompt = get_prompt(prompt_name)
  st.write(prompt)

Call OpenAI API.

::

  client = OpenAI()

  def call_openai(text, prompt):
      response = client.chat.completions.create(
              model="gpt-4-1106-preview",
              messages=[
                  {"role": "system", "content": prompt},
                  {"role": "user", "content": text},
              ],
              temperature=0.7,
          )

      choice = response.choices[0]
      out_text = choice.message.content

      st.write('---')
      st.write(out_text)
      st.write('---')
      st.write(f'finish_reason: `{choice.finish_reason}`')
      st.write(response.usage)
      st.write(f'Choices: {len(response.choices)}')

      out_file = 'st_openai.txt'
      with open(out_file, 'w') as file:
          file.write(out_text)
      st.write(f'Response saved: `{out_file}`')    

  if st.button('Call OpenAI'):
      call_openai(text, prompt)