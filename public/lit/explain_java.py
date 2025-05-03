# Explain Java
# ============
#
# .. contents::
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
import platform

from pathlib import Path
from typing import List

st.set_page_config(
    page_title="Explain-Java",
    layout="wide",
)

# Print current folder name as a title
#
# ::

current_folder = os.path.basename(os.getcwd())
st.write(f"### {current_folder}")
overwrite_files = True # st.toggle("Overwrite files")
hide_source_panel = st.toggle("Hide source panel", value=True)
st.write("---")

# Prints a stylized banner to the console when the application starts.
#
# ::

@st.cache_data
def print_banner():
    print(f"""
    ▗▞▀▚▖▄   ▄ ▄▄▄▄  █ ▗▞▀▜▌▄ ▄▄▄▄         ▗▖▗▞▀▜▌▄   ▄ ▗▞▀▜▌
    ▐▛▀▀▘ ▀▄▀  █   █ █ ▝▚▄▟▌▄ █   █  ▄▄    ▗▖▝▚▄▟▌█   █ ▝▚▄▟▌
    ▝▚▄▄▖▄▀ ▀▄ █▄▄▄▀ █      █ █   █     ▄  ▐▌      ▀▄▀       
               █     █      █           ▀▄▄▞▘                
               ▀  
               
    ██ {current_folder} ██
    """)
    return 1

print_banner()


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
    class_match = re.search(r'^\s*(?:\w+\s+)*(?:class|interface|enum)\s+([A-Za-z_]\w*)', java_code, re.MULTILINE)
    class_name = class_match.group(1) if class_match else None

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

def save_dict(classes_by_package, classes_by_package_json):
    cleaned = {k: v for k, v in classes_by_package.items() if k}
    with open(classes_by_package_json, 'w') as f:
        # Convert defaultdict to dict before saving
        json.dump(dict(cleaned), f)    

def load_dict(classes_by_package_json):
    with open(classes_by_package_json, 'r') as f:
        data = json.load(f)
        # Convert dict back to defaultdict(list)
        return defaultdict(list, data)    

try:
    classes_by_package = load_dict(classes_by_package_json)
except Exception as e: 
    st.warning(f"There are no Java files to explain. Please paste one.")  

# Load existing methods from json file
#
# ::

methods_by_class = defaultdict(list)
methods_by_class_json = "methods_by_class.json"

try:
    methods_by_class = load_dict(methods_by_class_json)
except Exception as e: 
    pass

# Persisted List   
# --------------    
#
# ::

class PersistedList:
    """
    A tiny helper that remembers a list of strings on disk.
    """

    def __init__(self, filename: str) -> None:
        self.filename = Path(filename)
        self.names: List[str] = self._read_from_file()

    # ──────────────────────────────────────────────────────────────
    # Private helpers
    # ──────────────────────────────────────────────────────────────

    def _read_from_file(self) -> List[str]:
        """
        Return the list stored on disk (empty if the file is missing).
        """
        if self.filename.exists():
            with self.filename.open("r", encoding="utf-8") as fh:
                return [line.strip() for line in fh if line.strip()]
        return []

    def _write_to_file(self) -> None:
        """
        Persist the current list to disk (one item per line).
        """
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        with self.filename.open("w", encoding="utf-8") as fh:
            fh.write("\n".join(self.names))

    @staticmethod
    def _remove_strings(source: List[str], to_remove: List[str]) -> List[str]:
        """
        Return a copy of *source* without any element that occurs in *to_remove*.
        """
        removal_set = set(to_remove)
        return [s for s in source if s not in removal_set]

    # ──────────────────────────────────────────────────────────────
    # Public API
    # ──────────────────────────────────────────────────────────────

    def sort_by_pattern(self, all_names: List[str]) -> List[str]:
        """
        Sort *all_names* so that previously‑stored names keep their old
        ordering, and every new name is appended alphabetically.
        The internal list is updated and re‑written to disk.
        """
        priority = {name: idx for idx, name in enumerate(self.names)}

        sorted_names = sorted(
            all_names,
            key=lambda n: (0, priority[n]) if n in priority else (1, n)
        )

        self.names = sorted_names
        self._write_to_file()
        return sorted_names

    def select(self, selected_name: str) -> None:
        """
        Move *selected_name* to the top of the list (inserting it if it
        wasn’t present) and persist the change.
        """
        self.names = self._remove_strings(self.names, [selected_name])
        self.names.insert(0, selected_name)
        self._write_to_file()

    # ──────────────────────────────────────────────────────────────
    # Convenience
    # ──────────────────────────────────────────────────────────────

    def __iter__(self):
        return iter(self.names)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.filename!s}, {self.names})"

# 1st row
# -------
#
# Select package, class and method
#
# ::

col1c, col2c, col3c = st.columns(3)

with col1c: 
    package_names = list(classes_by_package.keys())
    packages_persisted = PersistedList("packages.txt")
    package_names = packages_persisted.sort_by_pattern(package_names)
    package_name = st.selectbox("Package", package_names)

with col2c: 
    class_names = classes_by_package[package_name]
    classes_persisted = PersistedList("classes.txt")
    class_names = classes_persisted.sort_by_pattern(class_names)
    class_name = st.selectbox("Class", class_names) 

with col3c: 
    method_names = methods_by_class[f"{package_name}.{class_name}"]
    method_name = st.selectbox("Method", method_names)
  
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
    save_dict(classes_by_package, classes_by_package_json)
    st.rerun()

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

def file_path(package_name: str, class_name: str, method_name: str):
    method_suffix = f".{method_name}" if method_name else ""
    return os.path.join(dir_path(package_name), f"{class_name}{method_suffix}.md")
    
def load_markdown(package_name: str, class_name: str, method_name: str):
    with open(file_path(package_name, class_name, method_name), 'r', encoding='utf-8') as file:
        markdown = file.read()   
    
    return markdown  

def save_markdown(package_name: str, class_name: str, method_name: str, markdown: str, overwrite: bool):
    f_path = file_path(package_name, class_name, method_name)

    if (os.path.exists(f_path) and not overwrite):
        st.toast(f"File exists: {f_path}")
        return None, None
    
    # Save the file
    with open(f_path, 'w', encoding='utf-8') as f:
        f.write(markdown)

    # st.toast(f"Saved {class_name}.md in {d_path}")
    
# Select LLM    
# ----------    
#
# ::

llm_prices = {
    "gemini-2.5-pro-exp-03-25": 0.0,
    "gemini-2.0-flash": 0.0,
    "gemma-3-27b-it": 0.0,
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
llm_persisted = PersistedList("llm_models.txt")
llm_models = llm_persisted.sort_by_pattern(llm_models)

# Prompts 
# -------
#
# ::

def explain_prompt():
    return "Explain Java code you are provided."
    
def explain_method_prompt(method_name):
    return f"Explain method `{method_name}` in Java code you are provided."
    
def improve_prompt():
    return "Improve Java code you are provided."
    
def improve_method_prompt(method_name):
    return f"Improve method `{method_name}` in Java code you are provided."

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
    
    llm_persisted.select(llm_model)
    return response
  
# Get response from LLM and save it to file
#
# ::

def run_llm_op(llm_op, package_name, class_name, java_code):
    global method_name
    method_name = "" if method_name is None else method_name.strip()
    print(f"[run_llm_op] method_name: `{method_name}`")
    
    packages_persisted.select(package_name)
    classes_persisted.select(class_name)
    
    if llm_op == "Explain":
        if len(method_name) > 0: 
            response = call_llm(explain_method_prompt(method_name), java_code)
        else:    
            response = call_llm(explain_prompt(), java_code)
    elif llm_op == "Improve":
        if len(method_name) > 0: 
            response = call_llm(improve_method_prompt(method_name), java_code)
        else:    
            response = call_llm(improve_prompt(), java_code)
            
    markdown = response.message.content
    try:
        save_markdown(package_name, class_name, method_name, markdown, overwrite=overwrite_files)
    except ValueError as e:   
        st.toast(e)
        
    if platform.system() == 'Darwin':
        os.system("afplay /System/Library/Sounds/Glass.aiff")
        
    if len(method_name) > 0:
        class_key = f"{package_name}.{class_name}"
        if method_name not in methods_by_class[class_key]:
            methods_by_class[class_key].append(method_name)
            
        save_dict(methods_by_class, methods_by_class_json)
        st.rerun()
        

# 2nd row
# -------
#
# Buttons to "Paste" and "Explain"
#
# ::

col1b, col2b, col3b = st.columns(3)

llm_ops = ["Explain", "Improve"]

with col1b:
    if st.button(":clipboard: &nbsp; Paste", use_container_width=True):
        paste_java()
    llm_op = st.selectbox("Op", llm_ops, label_visibility="collapsed")
    
with col2b:
    llm_model = st.selectbox("LLM Model", llm_models, label_visibility="collapsed")

    llm_model_tiktoken = "gpt-4o-mini"

    encoding = tiktoken.encoding_for_model(llm_model_tiktoken)
    tokens = encoding.encode(java_code)

    cents = round(len(tokens) * llm_prices[llm_model]/10000, 5)

    st.write(f'**Tokens:** {len(tokens)}, **Cents:** {cents}')

with col3b:
    method_name = st.text_input("Method", value=method_name, label_visibility="collapsed")
    
    if st.button(f":exclamation: &nbsp; {llm_op}", use_container_width=True):
        f_path = file_path(package_name, class_name, method_name)

        if os.path.exists(f_path) and not overwrite_files:
            st.toast(f"File exists: {f_path}")
        else:
            run_llm_op(llm_op, package_name, class_name, java_code)
            
# Original java file and LLM explanation
#
# ::

if hide_source_panel:
    try:
        markdown = load_markdown(package_name, class_name, method_name)
        st.write(markdown)
    except Exception as e: 
        pass        
else:    
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