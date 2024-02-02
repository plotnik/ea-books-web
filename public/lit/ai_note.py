# Notepad-AI
# ==========
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

# Select OpenAI LLM.
#
# ::

openai_model = "gpt-4-0125-preview"
openai_temperature = 0.7

# Create OpenAI client.
#
# ::

client = OpenAI()

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


# Count tokens.
# 
# ::
    
if st.sidebar.button(':thermometer: &nbsp; Count Tokens'):
    
    encoding = tiktoken.encoding_for_model(openai_model)
    tokens = encoding.encode(text)
    st.write('---')
    st.write(f'Tokens: `{len(tokens)}`')
    

# Call OpenAI API.
# 
# ``openai_result`` is cached in ``session_state``.
#
# ::

if "openai_result" not in st.session_state:
    st.session_state.openai_result = ''
    
st.write('---')
st.write(st.session_state.openai_result)
    
st.sidebar.write('---')
if st.sidebar.button(':thinking_face: &nbsp; Call OpenAI', type="primary"):
    
    response = client.chat.completions.create(
            model=openai_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
            temperature=openai_temperature,
        )

    choice = response.choices[0]
    st.session_state.openai_result = choice.message.content
    st.write(st.session_state.openai_result)

    st.write('---')
    st.write(f'finish_reason: `{choice.finish_reason}`')
    st.write(response.usage)
    st.write(f'Choices: {len(response.choices)}')

# Save note.
# 
# ::

def save_note_disabled():
    return len(note_name.strip())==0
    
st.write('---')
note_name = st.text_input("Note Name")
if st.button(':spiral_note_pad: Save', disabled=save_note_disabled()):
    xml = textwrap.dedent(f"""
        <note>
          <question>
            {text}
          </question>
          <prompt>{prompt_name}<prompt>
          <answer>
            {st.session_state.openai_result}
          </answer>
        </note>
    """).strip()
    out_file = f"ai_note/{note_name}.xml"
    with open(out_file, 'w') as file:
        file.write(xml)
    st.write(f'Note saved: `{out_file}`')
      