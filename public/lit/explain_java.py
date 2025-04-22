# Explain Java
# ============
#
# ::

import streamlit as st
from openai import OpenAI
import os
import re
import pyperclip
from typing import Tuple
import json
from collections import defaultdict
import tiktoken

st.set_page_config(
    page_title="Explain Java",
    layout="wide",
)

# Prints a stylized banner to the console when the application starts.
#
# ::

@st.cache_data
def print_banner():
    print("""
    ▗▞▀▚▖▄   ▄ ▄▄▄▄  █ ▗▞▀▜▌▄ ▄▄▄▄         ▗▖▗▞▀▜▌▄   ▄ ▗▞▀▜▌
    ▐▛▀▀▘ ▀▄▀  █   █ █ ▝▚▄▟▌▄ █   █  ▄▄    ▗▖▝▚▄▟▌█   █ ▝▚▄▟▌
    ▝▚▄▄▖▄▀ ▀▄ █▄▄▄▀ █      █ █   █     ▄  ▐▌      ▀▄▀       
               █     █      █           ▀▄▄▞▘                
               ▀                                             
                                           
    """)
    return 1

print_banner()

# Print current folder name as a title
#
# ::

current_folder = os.path.basename(os.getcwd())
st.write(f"### {current_folder}")
overwrite_files = st.toggle("Overwrite files")
st.write("---")

# Save Java class
#
# ::

base_dir = 'src'

def dir_path(package_name: str) -> str:
    # Build directory path
    if package_name:
        package_path = package_name.replace('.', os.sep)
        dir_path = os.path.join(base_dir, package_path)
    else:
        dir_path = base_dir
    return dir_path    

def save_java_class(java_code: str, overwrite: bool) -> Tuple[str, str]:
    # Extract package name
    package_match = re.search(r'^\s*package\s+([\w\.]+)\s*;', java_code, re.MULTILINE)
    package_name = package_match.group(1) if package_match else None

    # Extract class name (public class, interface, or enum)
    class_match = re.search(r'^\s*(public\s+)?(class|interface|enum)\s+(\w+)', java_code, re.MULTILINE)
    class_name = class_match.group(3) if class_match else None

    if not class_name:
        raise ValueError("Could not find class name in the provided Java code.")

    # Build directory path
    d_path = dir_path(package_name)

    # Ensure directory exists
    os.makedirs(d_path, exist_ok=True)

    # File path
    file_path = os.path.join(d_path, f"{class_name}.java")

    if (os.path.exists(file_path) and not overwrite):
        st.toast(f"File exists: {file_path}")
        return None, None
      
    # Save the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(java_code)

    st.toast(f"Saved {class_name}.java in {d_path}")
    return package_name, class_name
 
# Load existing classes from json file
#
# ::

package_names: list[str] = []
class_names = []
classes_by_package = defaultdict(list)

classes_by_package_json = "classes_by_package.json"

def save_classes_by_package():
    with open(classes_by_package_json, 'w') as f:
        # Convert defaultdict to dict before saving
        json.dump(dict(classes_by_package), f)    

def load_classes_by_package():
    with open(classes_by_package_json, 'r') as f:
        data = json.load(f)
        # Convert dict back to defaultdict(list)
        return defaultdict(list, data)    

try:
    classes_by_package = load_classes_by_package()
except Exception as e: 
    st.warning(f"There are no Java files to explain. Please paste one.")  
  
# Select package, class and method
#
# ::

col1c, col2c, col3c = st.columns(3)

with col1c: 
    package_names = list(classes_by_package.keys())
    package_name = st.selectbox("Package", package_names)
  
with col2c: 
    class_names = classes_by_package[package_name]
    class_name = st.selectbox("Class", class_names) 

with col3c: 
    method_name = st.text_input("Method")
    
# Get java code from clipboard and save it to file
#
# ::

def paste_java():
    java_code = pyperclip.paste()
    try:
        package_name, class_name = save_java_class(java_code, overwrite=overwrite_files)
    except ValueError as e:   
        st.toast(e)
        return
      
    classes_by_package[package_name].append(class_name)  
    save_classes_by_package()
  
# Load Java code
#       
# ::

def load_java_code(package_name: str, class_name: str):
    # File path
    file_path = os.path.join(dir_path(package_name), f"{class_name}.java")
    with open(file_path, 'r', encoding='utf-8') as file:
        java_code = file.read()   
      
    return java_code 

try:
    java_code = load_java_code(package_name, class_name)    
except Exception as e:
    java_code = ""
    
# Load and save markdown result of LLM prompt
#
# :: 

def load_markdown(package_name: str, class_name: str, method_name: str):
    method_suffix = f"-{method_name}" if method_name else ""
    file_path = os.path.join(dir_path(package_name), f"{class_name}{method_suffix}.md")
    with open(file_path, 'r', encoding='utf-8') as file:
        markdown = file.read()   
      
    return markdown  
  
def save_markdown(package_name: str, class_name: str, method_name: str, markdown: str, overwrite: bool):
    d_path = dir_path(package_name)
    method_suffix = f"-{method_name}" if method_name else ""
    file_path = os.path.join(d_path, f"{class_name}{method_suffix}.md")
  
    if (os.path.exists(file_path) and not overwrite):
        st.toast(f"File exists: {file_path}")
        return None, None
      
    # Save the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    st.toast(f"Saved {class_name}.md in {d_path}")
  

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
    "o4-mini": 1.10,
    "o3-mini": 1.10,
    "gpt-4o": 2.5,
    "o1": 15.0,
}
llm_models = list(llm_prices.keys())

# Explain Java  
#
# ::

explain_prompt = "Explain Java code you are provided."
explain_method_prompt = f"Explain method `{method_name}` in Java code you are provided."

# OpenAI client
#
# ::

client = OpenAI()
llm_temperature = 0.1

# Google client
#
# ::

g_key = os.getenv("GEMINI_API_KEY")
g_client = OpenAI(
    api_key=g_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Calling different LLMs
#
# ::

def call_o_model(prompt, text):
    messages = [
        {"role": "developer", "content": prompt},
        {"role": "user", "content": text},
    ]
    response = client.chat.completions.create(
        model=llm_model,
        messages=messages,
    )
    return response.choices[0]
  
def call_gpt(prompt, text):
    messages = [
        {"role": "developer", "content": prompt},
        {"role": "user", "content": text},
    ]
    response = client.chat.completions.create(
            model=llm_model,
            messages=messages,
            temperature=llm_temperature,
        )
    return response.choices[0]
  
def call_gemini(prompt, text):
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

def call_gemma(prompt, text):
    g_client = OpenAI(
        api_key=g_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    messages = [
        {"role": "user", "content": f"<instructions>{prompt}</instructions>\n<user_input>{text}</user_input>"},
        {"role": "user", "content": text},
    ]
    response = g_client.chat.completions.create(
            model=llm_model,
            messages=messages,
            temperature=llm_temperature,
        )
    return response.choices[0]

def call_llm(prompt, text):

    if llm_model.startswith("gemini"):
        response = call_gemini(prompt, text)

    elif llm_model.startswith("gemma"):
        response = call_gemma(prompt, text)
      
    elif llm_model.startswith("gpt"):
        response = call_gpt(prompt, text)  
      
    elif llm_model.startswith("o"):
        response = call_o_model(prompt, text)

    else:
        st.error(f"Unknown model: {llm_model}")
        st.stop()
      
    return response
    
# Get response from LLM and save it to file
#
# ::

def explain(package_name, class_name, java_code):
    global method_name
    method_name = method_name.strip()
    if len(method_name) > 0:
        response = call_llm(explain_method_prompt, java_code)
    else:    
        response = call_llm(explain_prompt, java_code)
      
    markdown = response.message.content
    try:
        save_markdown(package_name, class_name, method_name, markdown, overwrite=overwrite_files)
    except ValueError as e:   
        st.toast(e)

# Buttons to "Paste" and "Explain"
#
# ::

col1b, col2b, col3b = st.columns(3)

with col1b:
    if st.button(":clipboard: &nbsp; Paste", use_container_width=True):
        paste_java()

with col2b:
    llm_model = st.selectbox("LLM Model", llm_models, label_visibility="collapsed")

    llm_model_tiktoken = "gpt-4o-mini"

    encoding = tiktoken.encoding_for_model(llm_model_tiktoken)
    tokens = encoding.encode(java_code)

    cents = round(len(tokens) * llm_prices[llm_model]/10000, 5)

    st.write(f'**Tokens:** {len(tokens)}, **Cents:** {cents}')
  
with col3b:
    if st.button(":exclamation: &nbsp; Explain", use_container_width=True):
        explain(package_name, class_name, java_code)

# Original java file and LLM explanation
#
# ::

col1j, col2j = st.columns(2)

with col1j:
    if len(java_code) > 0:
        st.write(f"```java\n{java_code}\n```\n")
  
with col2j:
    try:
        markdown = load_markdown(package_name, class_name, method_name)
        st.write(markdown)
    except Exception as e: 
        pass    