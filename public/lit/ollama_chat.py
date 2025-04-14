# Ollama Chat
# -----------
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "Ollama", https://github.com/ollama/ollama?tab=readme-ov-file
#    "Ollama Python", https://github.com/ollama/ollama-python
#   
# ::

import ollama 
import streamlit as st


# Call Ollama
#
# ::

question = st.text_input("Question")

if st.button(':thinking_face: &nbsp; Call LLama'):
  response = ollama.chat(model='llama3.2', messages=[
    {
      'role': 'user',
      'content': question,
    },
  ])

  st.write(response.message.content)

