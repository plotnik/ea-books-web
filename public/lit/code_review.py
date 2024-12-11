# Code Review
# ===========
#
# Submit multiple ``.java`` files along with their corresponding ``.patch`` files
# to ChatGPT for review.
#
# Here is the example on how to create ``.patch`` file between branches 
# ``origin/develop`` and ``feature/JIRA-12345`` for file 
# ``path/to/file/MyClass.java``:
#
# ``git diff origin/develop feature/JIRA-12345 -- path/to/file/MyClass.java > ../MyClass.patch``
#
# ::

import os
import fnmatch
import tiktoken
import textwrap
import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
#
# :: 

openai_model = "gpt-4o"
openai_temperature = 0.7

client = OpenAI()
encoding = tiktoken.encoding_for_model(openai_model)

# Get names of files in current folder.
#
# ::
    
java_files = [os.path.splitext(file)[0] for file in os.listdir('.') if fnmatch.fnmatch(file, '*.java')]
st.write(java_files)

# Collect ``messages`` for OpenAI request.
#
# ::
    
messages = []

messages.append({
  "role": "system",
  "content": """
      You are a helpful assistant that reviews Java code 
      and compares it with corresponding patch files. 
      For each pair of files, analyze the differences, 
      check code quality, suggest improvements, and flag potential bugs. 
      Provide feedback for each set."""
})

# Extract ``.java`` and ``.patch`` files from the list 
# and add them to ``messages``.
#
# ::
    
tokens = 0
num = 0
for java_file in java_files:
        with open(java_file + ".java", 'r', encoding='utf-8') as file:
            java = file.read()
        with open(java_file + ".patch", 'r', encoding='utf-8') as file:
            patch = file.read()     
        tokens += len(encoding.encode(java))    
        tokens += len(encoding.encode(patch))
        num += 1
        messages.append({
            "role": "user",
        "content": f"### Java File {num} ###\n{java}"
        })
        messages.append({
            "role": "user",
        "content": f"### Patch File {num} ###\n{patch}"
        })
        messages.append({
            "role": "user",
        "content": f"Please review the changes in Patch File {num} for Java File {num}."
        })

st.write(f"Tokens: `{tokens}`") 

openai_result = ""

# Join the strings with their corresponding numbers
#
# ::
    
def format_list_with_numbers(string_list):
    formatted_strings = "\n".join(f"{index + 1}. {item}" for index, item in enumerate(string_list))
    return formatted_strings

# Write output file
#
# ::

def save_result(out_file):
    with open(out_file, 'w') as file:
        file.write(textwrap.dedent(f"""
            # Code Review
          
            ## Files
          
            """))
        file.write(format_list_with_numbers(java_files)) 
        file.write(textwrap.dedent(f"""
          
            ## Result
          
            """))
        file.write(openai_result)    
          
    st.write(f"File saved: `{out_file}`")  
  
# Button to send OpenAI request.
#
# ::

if st.button("Call OpenAI"):
    response = client.chat.completions.create(
        model=openai_model,
        messages=messages,
        temperature=openai_temperature,
    )
    choice = response.choices[0]
    openai_result = choice.message.content
    st.write(openai_result)

    save_result("code_review.md")


