Code Review
===========

Submit multiple `.java` files along with their corresponding `.patch` files
to ChatGPT for review.

::

  import os
  import fnmatch
  import tiktoken
  import streamlit as st
  from openai import OpenAI

Initialize OpenAI client

:: 

  openai_model = "gpt-4o"
  openai_temperature = 0.7

  client = OpenAI()
  encoding = tiktoken.encoding_for_model(openai_model)

Get names of Java files in current folder.

::
    
  java_files = [os.path.splitext(file)[0] for file in os.listdir('.') if fnmatch.fnmatch(file, '*.java')]
  st.write(java_files)

Collect ``messages`` for OpenAI request.

::
    
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

Button to send OpenAI request.

::
    
  if st.button("Call OpenAI"):
      response = client.chat.completions.create(
          model=openai_model,
          messages=messages,
          temperature=openai_temperature,
      )
      choice = response.choices[0]
      openai_result = choice.message.content
      st.write(openai_result)

Save OpenAI result.

::
    
      out_file = "code_review.md"
      with open(out_file, 'w') as file:
              file.write(openai_result)

