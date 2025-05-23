# Obsidian-AI
# ===========
#
# Summarize Obsidian_ page.
#
# - Get `Python Source`_.
#
# Script is written in `literate programming`_.
#
# - See `PyLit Tutorial`_
# - See `reStructuredText Primer`_
#
# .. _Obsidian: https://obsidian.md/
# .. _Python Source: ../../ai_obsidian.py
# .. _literate programming: https://en.wikipedia.org/wiki/Literate_programming
# .. _reStructuredText Primer: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
# .. _PyLit Tutorial: https://slott56.github.io/PyLit-3/_build/html/tutorial/index.html
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "OpenAI API Examples", https://platform.openai.com/examples
#    "OpenAI Models", https://platform.openai.com/docs/models
#    "How to count tokens with tiktoken", https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
#
# ::

import streamlit as st
import yaml
import json
import os
import tiktoken
from openai import OpenAI
import pyperclip
from typing import List
import time

# Print banner.
#
# ::

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

# Prompts
# -------
#
# ::

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

# Select LLM
# ----------
#
# ::

llm_prices = {
    "gemma-3-27b-it": 0.0,
    "gemini-2.0-flash": 0.0,
    "gpt-4.1-mini": 0.4,
    "gpt-4.1-nano": 0.1,
    "gpt-4.1": 2.0,
    "gpt-4o-mini": 0.15,
    "o3-mini": 1.10,
    "gpt-4o": 2.5,
    "o1": 15.0,
}

# Remember which LLM was used last time
#
# ::

llm_names_file = ".o-ai"

# Writes a list of strings to a file, one per line.
#
# ::

def write_list_to_file(filename: str, lines: List[str]) -> None:
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('\n'.join(lines) + '\n')
      
# Reads non-empty, stripped lines from a text file into a list.
# Returns an empty list if the file does not exist or an error occurs.
#
# ::

def read_list_from_file(filename: str) -> None:
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []
      
# Compare two lists of strings for equality based on their sorted versions
#
# ::

def lists_are_equal(a: List[str], b: List[str]) -> bool:
    return sorted(a) == sorted(b)
  
# Removes all occurrences of ``string_to_remove`` from ``lst``.   
#
# ::

def remove_string(lines: List[str], string_to_remove: str) -> List[str]:
    return [s for s in lines if s != string_to_remove]
  
# Select LLM
#
# ::

llm_models = list(llm_prices.keys())
llm_names = read_list_from_file(llm_names_file) 
if lists_are_equal(llm_models, llm_names):
    llm_models = llm_names

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

# Select Obsidian folder from recent vaults.
#
# ::

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
   on_change=reset_llm_result
)
    
# Get the number of tokens.
#
# ::

file_path = os.path.join(note_home, note_name)
with open(file_path, 'r', encoding='utf-8') as file:
    text = file.read()
  
# Tokens & Price
# --------------
#
# Certain models are not compatible with ``tiktoken 0.7.0``, 
# so we have added a separate configuration for them.
#
# ::

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
 

# Call OpenAI API.
#
# ::

client = OpenAI()

def call_openai():
    response = client.chat.completions.create(
            model=llm_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
            temperature=llm_temperature,
        )

    return response.choices[0]
  
# Call Gemini.
#
# ::

g_key = os.getenv("GEMINI_API_KEY")
g_client = OpenAI(
    api_key=g_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def call_gemini():
    messages = [
        {"role": "developer", "content": prompt},
        {"role": "user", "content": text},
    ]
    response = g_client.chat.completions.create(
            model=llm_model,
            messages=messages,
            temperature=llm_temperature,
        )
    return response.choices[0]
  
def call_gemma():
    messages = [
        {"role": "user", "content": f"<prompt>{prompt}</prompt>\n<query>{text}</query>"},
    ]
    response = g_client.chat.completions.create(
            model=llm_model,
            messages=messages
        )
    return response.choices[0]
  
# Generic LLM call.
#
# ::

def call_llm():
    start_time = time.time()
    
    st.write('')
    st.info(prompt, icon="🤔")
  
    # Remember which LLM was used last time
    global llm_models
    llm_models = remove_string(llm_models, llm_model)
    llm_models.insert(0, llm_model)
    write_list_to_file(llm_names_file, llm_models)
  
    # Call LLM
    if llm_model.startswith("gemini"):
        choice = call_gemini()
    elif llm_model.startswith("gemma"): 
        choice = call_gemma()
    else:
        choice = call_openai()
      
    # Save result in session       
    st.session_state.llm_result = choice.message.content 
    st.session_state.note_name = note_name
    
    # Save result to clipboard  
    pyperclip.copy(st.session_state.llm_result)
    st.write(f'Copied to clipboard')
    
    end_time = time.time()
    st.session_state.execution_time = end_time - start_time
    
    st.rerun()
    
# Print result
#
# ::

if "llm_result" in st.session_state:
    st.write('---')
    st.write(st.session_state.llm_result)
    st.write('---')  
    
if "execution_time" in st.session_state:
    st.sidebar.write(f"Execution time: `{round(st.session_state.execution_time, 1)}` sec")    
    
# Sidebar buttons
#
# ::    

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
  

  
  
