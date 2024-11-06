# Obsidian-AI
# ===========
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "Obsidian", https://obsidian.md/
#    "OpenAI API Examples", https://platform.openai.com/examples
#    "OpenAI Models", https://platform.openai.com/docs/models
#    "How to count tokens with tiktoken", https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
#    "reStructuredText Primer", https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
#    "PyLit Tutorial", https://slott56.github.io/PyLit-3/_build/html/tutorial/index.html
#
# ::

import streamlit as st
import yaml
import json
import os
import tiktoken
from openai import OpenAI

# Print banner.
#
# ::

@st.cache_data
def print_banner():
    print("""
                             d8b 
                             Y8P 
                                 
     .d88b.          8888b.  888 
    d88""88b            "88b 888 
    888  888 888888 .d888888 888 
    Y88..88P        888  888 888 
     "Y88P"         "Y888888 888                                          
    """)
    return 1

print_banner()

# Select OpenAI LLM.
#
# ::

openai_model = "gpt-4o"
openai_temperature = 0.7

# Certain models are not compatible with ``tiktoken 0.7.0``, 
# so we have added a separate configuration for them.
# 
# ::

openai_model_tiktoken = openai_model 

# Select Obsidian folder from recent vaults.
#
# ::

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
)

# Load LLM prompts.
#
# ::

prompts_file = "openai_helper.yml"
with open(prompts_file, 'r') as file:
    prompts = yaml.safe_load(file)

def get_prompt(name):
    for entry in prompts:
        if entry['name'] == name:
            return entry.get('note')
    return None

# Get ``num_files`` newest files from the provided ``directory``.
#
# ::
    
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

# Select ``note_name`` from 5 newest notes.
#
# ::

newest_files = get_newest_files(note_home, 5)
note_name = st.selectbox(
   "Note",
   newest_files,
)

# Get the number of tokens.
# 
# ::

file_path = os.path.join(note_home, note_name)
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()

encoding = tiktoken.encoding_for_model(openai_model_tiktoken)
tokens = encoding.encode(text)

st.write(f'Model: `{openai_model}`') 
st.write(f'Tokens: `{len(tokens)}`')  

# Select the prompt.
#
# ::

if False:
    prompt_names = [item['name'] for item in prompts]
    prompt_name = st.selectbox(
       "Prompt",
       prompt_names,
    )
    
    prompt = get_prompt(prompt_name)
    st.write(prompt)

prompt = """You will be provided with statements in markdown, 
and your task is to summarize the content you are provided."""

# Call OpenAI API.
#
# ::

client = OpenAI()

if st.button('Summarize'):
    response = client.chat.completions.create(
            model=openai_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
            temperature=openai_temperature,
        )

    choice = response.choices[0]
    out_text = choice.message.content
    st.session_state.openai_result = out_text

    st.write('---')
    st.write(out_text)
    st.write('---')
    st.write(f'finish_reason: `{choice.finish_reason}`')
    st.write(response.usage)
    st.write(f'Choices: {len(response.choices)}')

    out_file = 'ai_obsidian.txt'
    with open(out_file, 'w') as file:
        file.write(out_text)
    st.write(f'Result saved: `{out_file}`')    

if 'openai_result' in st.session_state:
    st.text_area("Result", st.session_state.openai_result)
