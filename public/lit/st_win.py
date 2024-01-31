# Window for OpenAI prompts
# =========================
#
# ::

import streamlit as st
from openai import OpenAI
import yaml
import tiktoken

# Select OpenAI LLM.
#
# ::

openai_model = "gpt-4-0125-preview"

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

text = st.text_area(f"Prompt")

# Select the prompt.
# 
# ::

prompt_names = [item['name'] for item in prompts]
prompt_name = st.selectbox(
   "Prompt",
   prompt_names,
)
prompt = get_prompt(prompt_name)
st.write(prompt)


client = OpenAI()

# Count tokens.
# 
# ::

def count_tokens(text):
    encoding = tiktoken.encoding_for_model(openai_model)
    tokens = encoding.encode(text)
    st.write(f'Tokens: `{len(tokens)}`')
    
st.write('---')
if st.button('Count tokens'):
    count_tokens(text)

# Call OpenAI API.
# 
# ::

def call_openai(text, prompt):
    response = client.chat.completions.create(
            model=openai_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
            temperature=0.7,
        )

    choice = response.choices[0]
    out_text = choice.message.content

    st.write('---')
    st.write(out_text)
    st.write('---')
    st.write(f'finish_reason: `{choice.finish_reason}`')
    st.write(response.usage)
    st.write(f'Choices: {len(response.choices)}')

    out_file = 'st_win.txt'
    with open(out_file, 'w') as file:
        file.write(out_text)
    st.write(f'Response saved: `{out_file}`')
    
st.write('---')
if st.button('Call OpenAI'):
    call_openai(text, prompt)
