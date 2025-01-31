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
# ::

prompts_file = "openai_helper.yml"
with open(prompts_file, 'r') as file:
    prompts = yaml.safe_load(file)

def get_prompt(name):
    for entry in prompts:
        if entry['name'] == name:
            return entry.get('note')
    return None

text = st.text_area(f"Note", height=300)

# Select the prompt.
#
# ::

prompt_names = [item['name'] for item in prompts]
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

openai_models = [
    "gemini-2.0-flash-exp", 
    "gemini-1.5-pro", 
    "gemini-1.5-flash", 
    "gemini-1.5-flash-8b", 

    "gpt-4o", 
    "gpt-4o-mini", 
    "o1-mini", 
    "o1", 

    "ollama llama3.2"
]
  
openai_temperatures = [0, 0.7, 1]

openai_model = st.sidebar.selectbox(
   "OpenAI Model",
   openai_models,
   index = 0
)

openai_temperature = st.sidebar.select_slider(
   "OpenAI Temperature",
   options = openai_temperatures,
   value = 0.7
)

# Count tokens
# ------------
#
# If a button in the sidebar is clicked, the application counts the number of tokens in the user's input using the `tiktoken`_ library and displays the count.
#
# .. _tiktoken: https://cookbook.openai.com/examples/how_to_count_tokens_with_tiktoken
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
    
if st.sidebar.button('Count Tokens', use_container_width=True):

    encoding = tiktoken.encoding_for_model("gpt-4o-mini")
    tokens = encoding.encode(text)
    #st.write('---')
    st.sidebar.write(f'Tokens: `{len(tokens)}`')


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

# Call ``o1`` model
# =================
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "Reasoning with o1", https://learn.deeplearning.ai/courses/reasoning-with-o1/lesson/1/introduction
#
# ::

def call_o1_model(prompt, text):
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

# Call ``o1``-predecessor model
# =============================
#
# ::

def call_earlier_model(prompt, text):
    messages = [
        {"role": "developer", "content": prompt},
        {"role": "user", "content": text},
    ] 
    response = client.chat.completions.create(
            model=openai_model,
            messages=messages,
            temperature=openai_temperature,
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
            temperature=openai_temperature,
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
# ::

# Concatenate request
#
# ::
   
def concat_request(prompt, text):
    return prompt + "\n\n```\n" + text + "\n```\n"
        
    
st.sidebar.write('---')
if st.sidebar.button(':thinking_face: &nbsp; Query', type="primary", use_container_width=True):

    start_time = time.time()

    if "o1" in openai_model:
        response = call_o1_model(prompt, text)
      
    elif openai_model.startswith("gemini"): 
        response = call_gemini(prompt, text)
      
    elif openai_model.startswith("ollama "): 
        response = call_ollama(prompt, text)
      
    else:
        response = call_earlier_model(prompt, text)

    st.session_state.openai_result = response.message.content
    st.write(st.session_state.openai_result)

    # Calculate and print execution time
    end_time = time.time()
    execution_time = end_time - start_time
    # print(f'Execution time: `{execution_time:.1f}` seconds')

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
out_format = st.radio("Output:", ["Clipboard", "Request"] + save_formats, horizontal=True)

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
# accomplish. Here’s an example of how to structure the contents:
#
# .. code:: yaml
#
#    - name: grammar
#      note: You will be provided with statements in markdown, and your task is to convert them to standard English.  
#  
#    - name: improve_style
#      note: Improve style of the content you are provided.
#
#    - name: summarize_md
#      note: You will be provided with statements in markdown, and your task is to summarize the content.
#
#    - name: explain_python
#      note: Explain Python code you are provided.
#
#    - name: write_python
#      note: Write Python code to satisfy the description you are provided.
#
#    - name: improve_style
#      note: Improve style of the content you are provided.
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