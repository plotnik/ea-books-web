# =======
# Note-AI
# =======
#
# This is kind of Notepad editor with AI functions.
#
# - To set up the environment you can install Miniconda_.
# - For details see `Environment Setup`_.
# - Get `Python Source`_.
#
# .. _Miniconda: https://docs.conda.io/projects/miniconda/en/latest/
# .. _Python Source: ../../ai_note.py
#
# .. contents::
#
# The provided Python code is a Streamlit_ application designed to interact with `OpenAI's language models`_, allowing users to generate and save notes based on prompts. 
#
# .. _Streamlit: https://docs.streamlit.io/
# .. _OpenAI's language models: https://platform.openai.com/docs/models
#
# **User Input**: 
#    - A text area is provided for users to input their notes.
#    - A sidebar allows users to select a prompt from the loaded prompts.
#
# By the way, we can use emojis in buttons.
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "Streamlit emoji shortcodes", https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
#    "Emoji Cheat Sheet", https://www.webfx.com/tools/emoji-cheat-sheet/
#
# ::

import streamlit as st
from openai import OpenAI
import yaml
import tiktoken
import textwrap
import platform
import time
import os
import ollama
import pyperclip

# Prints a stylized banner to the console when the application starts.
#
# ::

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

# An instance of the OpenAI client is created to facilitate communication with the `OpenAI API`_.
#
# .. _OpenAI API: https://platform.openai.com/docs/guides/text-generation
#
# ::

client = OpenAI()

# Load LLM prompts
# ----------------
#
# The application reads prompts from a YAML file (`openai_helper.yml`). Each prompt has a name and a corresponding note that describes what the prompt should do.
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "Prompt engineering", https://platform.openai.com/docs/guides/prompt-engineering
#
# ::

prompts_file = "openai_helper.yml"
with open(prompts_file, 'r') as file:
    prompts = yaml.safe_load(file)

text = st.text_area(f"Note", height=300)

# Prompt Tags
# -----------
#
# Read a list of strings from a file
#
# ::

def read_list_from_file(filename):
    try:
        with open(filename, 'r') as file:
            # Read all lines and remove leading/trailing whitespace
            lines = [line.strip() for line in file.readlines()]  
        return lines
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return []
      
# Write a list of strings to a text file
#
# ::

def write_list_to_file(filename, list_of_strings):
    try:
        with open(filename, 'w') as file:  
            for string in list_of_strings:
                file.write(string + '\n') 
    except Exception as e:
        print(f"Error writing {filename}: {e}")
      
# Removes specified strings from a list of strings.  
#
# ::

def remove_strings_from_list(string_list, strings_to_remove):
  return [s for s in string_list if s not in strings_to_remove]
       
# Collect all tags into a single set
#
# ::

tags_file = "openai_tags.txt"

def sort_by_pattern(all_tags):
    tags_order = read_list_from_file(tags_file)
  
    # Create a mapping from tag to priority index for known tags.
    tag_priority = { tag: index for index, tag in enumerate(tags_order) }
  
    # Sort the all_tags list.
    # For tags in tags_order, the key is (0, priority) and for others (1, tag)
    sorted_tags = sorted(all_tags,
                         key=lambda tag: (0, tag_priority[tag]) if tag in tag_priority
                                           else (1, tag))
    return sorted_tags 

all_tags_set = {tag for item in prompts for tag in item.get('tags', [])}
all_tags = sort_by_pattern(list(all_tags_set))
all_tags.insert(0, "all")

tag_name = st.sidebar.selectbox(
   "Tag",
   all_tags,
)

# Select the Prompt
# -----------------
#
# ::

def get_prompt(name):
    for entry in prompts:
        if entry['name'] == name:
            return entry.get('note')
    return None
  
if tag_name == "all":
    prompt_names = [item['name'] for item in prompts]
else:    
    prompt_names = [item['name'] for item in prompts if tag_name in item.get('tags', [])]

prompt_name = st.sidebar.selectbox(
   "Prompt",
   prompt_names,
)
prompt = get_prompt(prompt_name)
st.write(prompt)

# Select OpenAI LLM
# -----------------
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "OpenAI Models", https://platform.openai.com/docs/models
#
# ::

model_type = st.sidebar.radio("Model Type", ["Gemini", "OpenAI", "Ollama"])

if model_type=="Gemini":    
    llm_models = [
        "gemini-2.0-flash", 
    ]
elif model_type=="OpenAI":    
    llm_models = [
        "gpt-4o-mini", 
        "o3-mini",
        "gpt-4o", 
        "o1", 
        "gpt-4.5-preview",
    ]    
else:    
    llm_models = [
        "ollama llama3.2",
    ]
  
llm_temperatures = [0, 0.1, 0.7, 1]

openai_model = st.sidebar.selectbox(
   "LLM Model",
   llm_models,
   index = 0
)

llm_temperature = st.sidebar.select_slider(
   "LLM Temperature",
   options = llm_temperatures,
   value = 0.1
)

# Tokens & Price
# --------------
#
# If a button in the sidebar is clicked, the application counts the number of tokens in the user's input using the `tiktoken`_ library and displays the count.
#
# .. _tiktoken: https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "Model Pricing", https://platform.openai.com/docs/pricing#latest-models
#
# ::
    
if model_type=="OpenAI":

    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    tokens = encoding.encode(text)
  
    openai_prices = {
        "gpt-4o-mini": 0.15, 
        "o3-mini": 1.10,
        "gpt-4o": 2.5, 
        "o1": 15.0, 
        "gpt-4.5-preview": 75.0,
    }
    cents = round(len(tokens) * openai_prices[openai_model]/10000, 5)

    st.sidebar.write(f'''
        | Characters | Tokens | Cents |
        |---|---|---|
        | {len(text)} | {len(tokens)} | {cents} |
        ''')  

# Call OpenAI API
# ---------------
#
# ``openai_result`` is cached in a `session_state`_.
#
# .. _session_state: https://docs.streamlit.io/get-started/fundamentals/advanced-concepts#session-state
#
# ::

if "openai_result" not in st.session_state:
    st.session_state.openai_result = ''

st.write('---')
st.write(st.session_state.openai_result)

# Call ``o`` model
# ================
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "Reasoning with o1", https://learn.deeplearning.ai/courses/reasoning-with-o1/lesson/1/introduction
#
# ::

def call_o_model(prompt, text):
    messages = [
        #{"role": "user", "content": f"<instructions>{prompt}</instructions>\n<user_input>{text}</user_input>"},
        {"role": "developer", "content": prompt},
        {"role": "user", "content": text},
    ]
    response = client.chat.completions.create(
        model=openai_model,
        messages=messages,
    )
    return response.choices[0]

# Call ``gpt`` model
# ==================
#
# ::

def call_gpt_model(prompt, text):
    messages = [
        {"role": "developer", "content": prompt},
        {"role": "user", "content": text},
    ] 
    response = client.chat.completions.create(
            model=openai_model,
            messages=messages,
            temperature=llm_temperature,
        )
    return response.choices[0]

# Call Ollama
# ===========
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "Ollama", https://github.com/ollama/ollama?tab=readme-ov-file
#    "Ollama Python", https://github.com/ollama/ollama-python
#
# ::

def call_ollama(prompt, text):
    model = openai_model[len("ollama "):]
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": text},
    ] 
    return ollama.chat(
            model=model,
            messages=messages,
        )

# Call Gemini
# ===========
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "Text generation", https://ai.google.dev/gemini-api/docs/text-generation?lang=python
#    "OpenAI compatibility", https://ai.google.dev/gemini-api/docs/openai
#    "Example applications", https://ai.google.dev/gemini-api/docs/models/generative-models#example-applications
#    "Model variants", https://ai.google.dev/gemini-api/docs/models/gemini#model-variations
#    "Google Gen AI SDKs", https://ai.google.dev/gemini-api/docs/sdks
#
# ::

def call_gemini(prompt, text):
    g_key = os.getenv("GEMINI_API_KEY")
    g_client = OpenAI(
        api_key=g_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    messages = [
        {"role": "developer", "content": prompt},
        {"role": "user", "content": text},
    ] 
    response = g_client.chat.completions.create(
            model=openai_model,
            messages=messages,
            temperature=llm_temperature,
        )
    return response.choices[0]
   
# When the user clicks a button to call OpenAI:
#
# - The application sends the selected prompt and user input to the OpenAI API.
# - The response is stored in the session state and displayed to the user.
# - The execution time for the API call is calculated and can be used for monitoring performance.
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "OpenAI Chat API", https://platform.openai.com/docs/api-reference/chat
#
# Concatenate request
#
# ::
   
def concat_request(prompt, text):
    return prompt + "\n\n```\n" + text + "\n```\n"
  

st.sidebar.write('---')
if st.sidebar.button(':thinking_face: &nbsp; Query', type="primary", use_container_width=True):

    start_time = time.time()

    if openai_model.startswith(("o1", "o3")):
        response = call_o_model(prompt, text)

    elif openai_model.startswith("gemini"): 
        response = call_gemini(prompt, text)

    elif openai_model.startswith("ollama "): 
        response = call_ollama(prompt, text)

    else:
        response = call_gpt_model(prompt, text)

    st.session_state.openai_result = response.message.content
    st.write(st.session_state.openai_result)

    # Calculate and print execution time
    end_time = time.time()
    execution_time = end_time - start_time
    # print(f'Execution time: `{execution_time:.1f}` seconds')

    # Move selected tag to the beginning of the list
    all_tags = remove_strings_from_list(all_tags, ["all", tag_name])
    all_tags.insert(0, tag_name)
    write_list_to_file(tags_file, all_tags)
  
    if platform.system() == 'Darwin':
        os.system("afplay /System/Library/Sounds/Glass.aiff")
    st.rerun()

# Save note
# ---------
#
# Notes will be saved to ``ai_note`` folder which is expected to exist.
#
# Output format can be XML with request, response and prompt name, or just response markdown.
#
# ::


note_name = st.text_input("Note Name:")

save_formats = ["Markdown", "XML"]
out_format = st.radio(openai_model + ":", ["Clipboard", "Request"] + save_formats, horizontal=True)

button_name = "Save" if out_format in save_formats else "Copy"

def save_note_disabled():
    return len(note_name.strip())==0 and out_format in save_formats

if st.button(':spiral_note_pad: ' + button_name, disabled=save_note_disabled()):
    if out_format == "Clipboard":
        pyperclip.copy(st.session_state.openai_result)
        st.write(f'Copied to clipboard')
    if out_format == "Request":
        pyperclip.copy(concat_request(prompt, text))
        st.write(f'Request copied to clipboard')    
    elif out_format == "XML":
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

# Environment Setup
# -----------------
#
# To set up your environment using Miniconda_, follow the steps below.
# These instructions will guide you through installing Miniconda,
# configuring your environment, and running a Streamlit application
# tailored for AI tasks.
#
# Step 1: Install Miniconda
# =========================
#
# First, you need to install Miniconda. Visit the `Miniconda
# website <https://docs.conda.io/en/latest/miniconda.html>`__ and follow
# the installation instructions for your operating system.
#
# Step 2: Configure Your Environment
# ==================================
#
# 1. **Create the Environment File**
#
#    Create a file named ``environment.yml`` in your project directory.
#    Paste the following contents into this file:
#
#    .. code:: yaml
#
#       name: ai_note
#       channels:
#         - conda-forge
#         - defaults
#       dependencies:
#         - python=3.11.0
#         - openai
#         - tiktoken
#         - streamlit
#         - ollama
#         - pyperclip
#
# 2. **Select conda-forge Channel**
#
#    Open your terminal or command prompt and execute the following
#    commands to prioritize the ``conda-forge`` channel:
#
#    .. code:: shell
#
#       conda config --add channels conda-forge
#       conda config --set channel_priority strict
#
# 3. **Create the Environment**
#
#    Still in your terminal, navigate to the directory containing your
#    ``environment.yml`` file. Create the Conda environment by running:
#
#    .. code:: shell
#
#       conda env create -f environment.yml
#
# Step 3: Activate the Environment
# ================================
#
# Activate your newly created environment by executing:
#
# .. code:: shell
#
#    conda activate ai_note
#
# Step 4: Prepare Prompt File
# ===========================
#
# Create a file named ``openai_helper.yml`` in your project directory.
# This file should contain various prompts for the tasks you want to
# accomplish. 
# You can include tags in your prompts to categorize them.
# Here’s an example of how to structure the contents:
#
# .. code:: yaml
#
#    - name: grammar
#      note: You will be provided with statements in markdown, and your task is to convert them to standard English.  
#      tags:
#        - text
#
#    - name: improve_style
#      note: Improve style of the content you are provided.
#      tags:
#        - text
#       
#    - name: summarize_md
#      note: You will be provided with statements in markdown, and your task is to summarize the content.
#      tags:
#        - text
#       
#    - name: explain_python
#      note: Explain Python code you are provided.
#      tags:
#        - python
#       
#    - name: write_python
#      note: Write Python code to satisfy the description you are provided.
#      tags:
#        - python
#
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "Examples of OpenAI prompts", https://platform.openai.com/examples
#
#
# Step 5: Run Streamlit Script
# ============================
#
# With your environment set up and activated, and your
# ``openai_helper.yml`` file ready, you’re now set to run your Streamlit
# application. Execute the following command in your terminal:
#
# .. code:: shell
#
#    streamlit run ai_note.py
#
# And that’s it! Your Streamlit application should now be running, and you
# can interact with it through your web browser.