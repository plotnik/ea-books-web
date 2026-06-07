# Ollama Chat
# -----------
#
# ``OLLAMA_HOST`` env variable should point to Ollama host
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "Ollama", https://github.com/ollama/ollama?tab=readme-ov-file
#    "Ollama Python", https://github.com/ollama/ollama-python
#  
# ::

import streamlit as st
import ollama 
import time
import os
import requests

llm_model = os.getenv("OLLAMA_MODEL", 'llama3.2')
st.sidebar.write(f"LLM model: `{llm_model}`")

ollama_host = os.getenv("OLLAMA_HOST", 'http://localhost:11434')

enable_thinking = False

# Call Ollama
#
# ::

question = st.text_input("Question")

# .. function:: ask_ollama(user_prompt: str) -> str

def ask_ollama(user_prompt: str) -> str:
    if not enable_thinking:
        user_prompt = f"/no_think {user_prompt}"

    payload = {
        "model": llm_model,
        "messages": [
            {"role": "user", "content": user_prompt},
        ],
        "think": enable_thinking,
        "stream": False,
        "options": {
            "num_predict": 80,
            "temperature": 0,
            "top_p": 0.1,
            "num_ctx": 1024,
        },
    }

    response = requests.post(
        f"{ollama_host}/api/chat",
        json=payload,
        timeout=180,
    )

    response.raise_for_status()
    
    return response.json()["message"]["content"]
    
    
def ask_ollama_client(question: str) -> str:
    response = ollama.chat(model=llm_model, messages=[
      {
        'role': 'user',
        'content': question,
      },
    ])
    return response.message.content

# Call Ollama

if st.button('🦙 &nbsp; Call Ollama', type="primary", width="stretch"):
    start_time = time.time()
    
    answer = ask_ollama(question)
    st.write(answer)
    
    end_time = time.time()
    execution_time = end_time - start_time
    st.session_state.execution_time = end_time - start_time
    
if "execution_time" in st.session_state:
    st.sidebar.write(f"Execution time: `{round(st.session_state.execution_time, 2)}` sec")
