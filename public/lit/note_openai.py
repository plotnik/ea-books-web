# Note-OpenAI
# ===========
#
# This application is a lightweight text editor, 
# something like Notepad in Windows, 
# but with web interface, and
# enhanced with AI-assisted features powered by OpenAI.
#
# It integrates with OpenAI's |robot| `Responses API`_ to provide intelligent text operations.
#
# .. _Responses API: https://developers.openai.com/api/reference/resources/responses/methods/create
#
# .. |jigsaw|     unicode:: 0x1F9E9 U+2002
# .. |label|      unicode:: 0x1F3F7 U+2002
# .. |compass|    unicode:: 0x1F9ED U+2002
# .. |robot|      unicode:: 0x1F916 U+2002
# .. |control_knobs| unicode:: 0x1F39B 0xFE0F U+2002
# .. |brain|      unicode:: 0x1F9E0 U+2002
# .. |magic_wand| unicode:: 0x1FA84 U+2002
# .. |books|      unicode:: 0x1F4DA U+2002
# .. |1234|       unicode:: 0x1F522 U+2002
# .. |straight_ruler| unicode:: 0x1F4CF U+2002
# .. |snake|      unicode:: 0x1F40D U+2002
# .. |memo|       unicode:: 0x1F4DD U+2002
# .. |computer|   unicode:: 0x1F4BB U+2002
# .. |swan|       unicode:: 0x1F9A2 U+2002
# .. |yin_yang|   unicode:: 0x262F U+2002
# .. |eyeglasses| unicode:: 0x1F453 U+2002
# .. |test_tube|  unicode:: 0x1F9EA U+2002
# .. |chart_with_upwards_trend| unicode:: 0x1F4C8 U+2002
# .. |feather|    unicode:: 0x1FAB6 U+2002
# .. |speech_balloon|     unicode:: 0x1F4AC U+2002
# .. |hammer_and_wrench|  unicode:: 0x1F6E0 U+2002
# .. |page_facing_up|     unicode:: 0x1F4C4 U+2002
#
# ----
#
# |jigsaw| **OpenAI Models**
#    https://developers.openai.com/api/docs/models
#
# |label| **OpenAI Model Pricing**
#    https://developers.openai.com/api/docs/pricing#latest-models
#   
# ----   
#
# .. _Prompt Examples:
#
# .. admonition:: |speech_balloon| Prompt Examples
#    :class: note
#
#    - `Awesome AI Prompts <https://github.com/0x2e-Tech/awesome-ai-prompts>`_
#    - `Prompts.chat <https://github.com/f/prompts.chat/blob/main/README.md>`_
#
# ----
#
# |compass| **Model guidance**
#    https://developers.openai.com/api/docs/guides/latest-model
#
# |chart_with_upwards_trend| **Prompt Optimizer**
#    https://platform.openai.com/chat/edit?optimize=true
#
# |brain| **Reasoning models**
#    https://developers.openai.com/api/docs/guides/reasoning
#
# |feather| **Text generation**
#    https://developers.openai.com/api/docs/guides/text
#
# |magic_wand| **Prompt engineering**
#    https://developers.openai.com/api/docs/guides/prompt-engineering
#
# |books| **OpenAI Cookbook**
#    https://developers.openai.com/cookbook
#   
#
# ----
#
# |1234| **Tiktoken in CodeWiki**
#    https://codewiki.google/github.com/openai/tiktoken
#
# |straight_ruler| **Tiktoken How-to Cookbook**
#    https://developers.openai.com/cookbook/examples/how_to_count_tokens_with_tiktoken
#
# ----
#
# .. admonition:: |yin_yang| Literate Programming
#    :class: note
#   
#     - Get |snake| `Python Source`_. Save it as ``note_openai.py``. 
#     - Save |snake| `PersistedList.py`_ in the same folder.
#    
#    
#     Script is written in |eyeglasses| `literate programming`_.
#    
#     - See |yin_yang| `PyLit Tutorial`_
#     - See |compass| `reStructuredText Primer`_
#
# .. _Python Source: ../../note_openai.py
# .. _PersistedList.py: ../../PersistedList.py
# .. _literate programming: https://en.wikipedia.org/wiki/Literate_programming
# .. _reStructuredText Primer: https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
# .. _PyLit Tutorial: https://slott56.github.io/PyLit-3/_build/html/tutorial/index.html
#
# ----
#
# ::

import streamlit as st
from openai import OpenAI
import yaml
import tiktoken
import platform
import time
import os
import pyperclip

# Prints a stylized banner to the console when the application starts.
#
# ::
    
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

# OpenAI client.
#
# ::

client = OpenAI()

# Reads prompts from a YAML configuration file (``openai_helper.yml``).  
# Each prompt entry includes a unique name, a descriptive note explaining its purpose, and an optional list of tags for categorization.
#
# .. _expected YAML structure:
#
# The expected YAML structure is:
#
# .. code-block:: yaml
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
# Each item in the list represents a single prompt and must define:
#
# - ``name``: A short, unique identifier for the prompt.
# - ``note``: Prompt body.
# - ``tags``: A list of categories (for example, ``text`` or ``python``) that describe the prompt’s domain or usage.
#
# ::

prompts_file = "openai_helper.yml"
with open(prompts_file, 'r') as file:
    prompts = yaml.safe_load(file)

# Text area to provide input text
#
# ::
    
input_text = st.text_area(f"Note", height=300)

# See: PersistedList_
#
# .. _PersistedList: PersistedList.py.html
#
# ::

from PersistedList import PersistedList
tags_persisted = PersistedList(".tags")  
prompts_persisted = PersistedList(".prompts")  
llms_persisted = PersistedList(".llms") 
efforts_persisted = PersistedList(".efforts") 

# 1) Select **category**, aka **group**, aka **tag**.
#
# ::

all_tags_set = {tag for item in prompts for tag in item.get('tags', [])}
all_tags = tags_persisted.sort_by_pattern(list(all_tags_set))

tag_name = st.sidebar.selectbox(
   "Category",
   all_tags,
)  

# .. function:: get_prompt(name)
#
# Select prompt body by its name
#
# ::

def get_prompt(name):
    for entry in prompts:
        if entry['name'] == name:
            return entry.get('note')
    return None

# .. function:: has_tag(name, tag_name)
#
# ::

def has_tag(name, tag_name):  
    for entry in prompts:
        if entry['name'] == name:
            return tag_name in entry.get('tags', [])
    return False

# 2) Select **prompt**.
#
# ::

all_prompt_names_set = {item['name'] for item in prompts}

all_prompt_names = prompts_persisted.sort_by_pattern(
    list(all_prompt_names_set), 
    group=tag_name
)
prompt_names = [name for name in all_prompt_names if has_tag(name, tag_name)]

prompt_name = st.sidebar.selectbox(
   "Prompt",
   prompt_names,
)
prompt = get_prompt(prompt_name)
st.write(prompt)  


# LLM Prices - (Short context, Long context)
#
# ::

llm_prices = {
    "gpt-6-luna": ((0.10, 0.50), (0.20, 0.75)),
    "gpt-6.1-sol": ((2.00, 10.00), (4.00, 15.00)),
    "gpt-6-astra": ((10.00, 50.00), (20.00, 75.00)),
}    

LONG_LIMIT_TOKENS = 272 * 1024

# 3) Select **OpenAI LLM model**
#
# ::

llm_models = list(llm_prices.keys())

all_llm_models = llms_persisted.sort_by_pattern(
    llm_models, 
    group=f"{tag_name}/{prompt_name}"
)

llm_model = st.sidebar.selectbox(
   "LLM Model",
   all_llm_models
)

# 4) Select **reasoning effort**
#
# ::

reasoning_efforts = [
    "none",
    "low",
    "medium",
    "high",
    "xhigh",
    "max",
]

all_reasoning_efforts = efforts_persisted.sort_by_pattern(
    reasoning_efforts, 
    group=f"{tag_name}/{prompt_name}/{llm_model}"
)

reasoning_effort = st.sidebar.selectbox(
   "Reasoning",
   all_reasoning_efforts
)

# Count the number of tokens in the user’s input using the ``tiktoken`` library, 
# and display both the token count and the corresponding price.
#
# ::

encoding = tiktoken.get_encoding("o200k_base")
tokens = encoding.encode(input_text)
token_count = len(tokens)

prices = llm_prices[llm_model][1] if token_count > LONG_LIMIT_TOKENS else llm_prices[llm_model][0]
cents = round(token_count * prices[0] / 10000, 5)

st.sidebar.write(f'''
    | Chars | Tokens | Cents |
    |---|---|---|
    | {len(input_text)} | {len(tokens)} | {cents} |
    ''') 

# .. function:: call_llm(text, prompt)
#
# ::

def call_llm(text, prompt):
    response = client.responses.create(
        model=llm_model,
        reasoning={"effort": reasoning_effort},
        instructions=prompt,
        input=input_text
    )

    return response.output_text

# Run Query
#
# ::

if st.button('Query', type="primary", icon=":material/cyclone:", width="stretch"):
    start_time = time.time()

    # Call LLM
    st.session_state.llm_output = call_llm(input_text, prompt)
    # st.write(st.session_state.llm_output)

    # Calculate and print execution time
    end_time = time.time()
    execution_time = end_time - start_time
    st.session_state.execution_time = end_time - start_time

    # Calculate output price
    tokens = encoding.encode(st.session_state.llm_output)
    st.session_state.output_price = len(tokens) * prices[1]/10000

    # Remember persisted selections
    tags_persisted.select(tag_name)
    prompts_persisted.select(prompt_name, group=tag_name)
    llms_persisted.select(llm_model, group=f"{tag_name}/{prompt_name}")
    efforts_persisted.select(reasoning_effort, group=f"{tag_name}/{prompt_name}/{llm_model}")

    if platform.system() == 'Darwin':
        os.system("afplay /System/Library/Sounds/Glass.aiff")
    st.rerun()

# LLM output is cached in ``session_state``.
#
# ::

if "llm_output" not in st.session_state:
    st.stop()

st.write('---')
st.write(st.session_state.llm_output)

if st.button("Clipboard", icon=":material/content_copy:"):
    pyperclip.copy(st.session_state.llm_output)
    st.write(f'Copied to clipboard') 

# Show last execution time
#
# ::

if "execution_time" in st.session_state:
    st.sidebar.write(f"Execution time: `{round(st.session_state.execution_time, 2)}` sec")

if "output_price" in st.session_state:
    st.sidebar.write(f"Output price: `{round(st.session_state.output_price, 5)}` cents")  

# -----
#
# Environment Setup 
# -----------------
#
# - `Option 1. With Miniconda`_
# - `Option 2. With venv`_
#
# Option 1. With Miniconda
# ************************
#
# .. _Miniconda: https://www.anaconda.com/docs/getting-started/concepts/anaconda-or-miniconda
# .. _Miniconda installation page: https://www.anaconda.com/docs/getting-started/miniconda/install/windows-gui-install
#
# To set up your environment using |snake| Miniconda_, follow the steps below.
# These instructions will guide you through installing Miniconda,
# configuring your environment, and running a Streamlit application
# tailored for AI tasks.
#
# Step 1: Install Miniconda
# ~~~~~~~~~~~~~~~~~~~~~~~~~
#
# First, you need to install Miniconda. Visit |hammer_and_wrench| `Miniconda installation page`_ 
# and follow the instructions for your operating system.
#
# Step 2: Configure Your Environment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1. **Create the Environment File**
#
#    Create a file named ``environment.yml`` in your project directory.
#    Paste the following contents into this file:
#
#    .. code:: yaml
#
#       name: ai-0.1
#       channels:
#         - conda-forge
#         - defaults
#       dependencies:
#         - python=3.12.0
#         - openai
#         - tiktoken
#         - streamlit
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
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Activate your newly created environment by executing:
#
# .. code:: shell
#
#    conda activate ai-0.1
#
# Step 4: Prepare Prompt File
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Create a file named ``openai_helper.yml`` in your project directory.
# This file should contain various prompts for the tasks you want to
# accomplish. 
# You can include tags in your prompts to categorize them.
#
# ----       
#
# - See an example of the |page_facing_up| `expected YAML structure`_.
# - See |speech_balloon| `Prompt Examples`_.
#
# ----
#
# Step 5: Run Streamlit Script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# With your environment set up and activated, and your
# ``openai_helper.yml`` file ready, you’re now set to run your Streamlit
# application. Execute the following command in your terminal:
#
# .. code:: shell
#
#    streamlit run note_openai.py
#
# And that’s it! Your Streamlit application should now be running, and you
# can interact with it through your web browser.     
#
# ----
#
# Option 2. With venv
# *******************
#
# .. _Python: https://www.python.org/
# .. _Python download page: https://www.python.org/downloads/
# .. _Python virtual environments: https://docs.python.org/3/library/venv.html
#
# To set up your environment using Python's built-in `venv` module,
# follow the steps below. These instructions will guide you through
# installing Python, creating a virtual environment, installing the
# required packages, and running a Streamlit application tailored for
# AI tasks.
#
# Step 1: Install Python
# ~~~~~~~~~~~~~~~~~~~~~~
#
# First, make sure Python is installed on your computer. 
# Version 3.12 was used, but other recent Python 3 versions should work as well.
# Visit the
# |snake| `Python download page`_ and download an appropriate Python 
# release for your operating system.
#
# On Windows, select the option to add Python to your ``PATH`` during
# installation.
#
# After installation, open a terminal or command prompt and verify the
# Python version:
#
# .. code:: shell
#
#    python --version
#
# Step 2: Configure Your Environment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# 1. **Create the Requirements File**
#
#    Create a file named ``requirements.txt`` in your project directory.
#    Paste the following contents into this file:
#
#    .. code:: text
#
#        openai
#        tiktoken
#        streamlit
#        pyperclip
#
# 2. **Create the Virtual Environment**
#
#    Open a terminal or command prompt and navigate to your project
#    directory:
#
#    .. code:: shell
#
#        cd path/to/your/project
#
#    Create a virtual environment named ``.venv`` by running:
#
#    .. code:: shell
#
#        python -m venv .venv
#
#    The ``.venv`` directory contains an isolated Python environment for
#    this project. It should not normally be committed to version control.
#
# Step 3: Activate the Environment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Activate the newly created virtual environment using the command for
# your operating system and terminal.
#
# **Windows Command Prompt:**
#
# .. code:: bat
#
#    .venv\Scripts\activate.bat
#
# **Windows PowerShell:**
#
# .. code:: powershell
#
#    .\.venv\Scripts\Activate.ps1
#
# **macOS or Linux:**
#
# .. code:: shell
#
#    source .venv/bin/activate
#
# After activation, your terminal prompt should display ``(.venv)``.
#
# Step 4: Install the Dependencies
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# With the virtual environment activated, update ``pip``:
#
# .. code:: shell
#
#     python -m pip install --upgrade pip
#
# Install the packages listed in ``requirements.txt``:
#
# .. code:: shell
#
#     python -m pip install -r requirements.txt
#
# You can verify that the required packages were installed by running:
#
# .. code:: shell
#
#     python -m pip list
#
# Step 5: Prepare Prompt File
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# Create a file named ``openai_helper.yml`` in your project directory.
# This file should contain the prompts for the tasks you want to
# accomplish.
#
# You can include tags in your prompts to organize them into categories.
#
# ----
#
# - See an example of the |page_facing_up| `expected YAML structure`_.
# - See |speech_balloon| `Prompt Examples`_.
#
# ----
#
# Step 6: Run Streamlit Script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# With the virtual environment activated and the
# ``openai_helper.yml`` file ready, run the Streamlit application by
# executing:
#
# .. code:: shell
#
#     streamlit run note_openai.py
#
# The Streamlit application should start locally and open in your default
# web browser.
#
# Step 7: Deactivate the Environment
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# When you are finished working with the application, deactivate the
# virtual environment by running:
#
# .. code:: shell
#
#    deactivate
#
# To use the application again later, navigate to the project directory,
# activate ``.venv``, and run the Streamlit command again.
