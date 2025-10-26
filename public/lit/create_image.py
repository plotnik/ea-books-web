# Create Image
# ============
#
# | **OpenAI Create image API:**
# | https://platform.openai.com/docs/api-reference/images/create
#
# ::

import streamlit as st
import os
import base64
from openai import OpenAI
from datetime import date
import time

# Print banner
#
# ::

st.set_page_config(
    page_title="Create-Image"
)

@st.cache_data
def print_banner():
    print("""
      .-._   .-._.                   .       .;;;;.                             
    .: (_)`-'                    ...;...    ' .;'  `                            
    ::       .;.::..-.  .-.       .'.-.      .;'    . ,';.,';. .-.   ,:.,' .-.  
    ::   _   .;  .;.-' ;   :    .;.;.-'`;;;..;'     ;;  ;;  ;;;   : :   ;.;.-'  
    `: .; ).;'    `:::'`:::'-'.;   `:::'   .;'     ';  ;;  '; `:::'-'`-:' `:::' 
      `--'                             .;;;;;;;;;'_;        `-'    -._:'        
    """)
    return 1

print_banner()

# File names
#
# ::


history_file = "image_prompts.txt"

image_title = st.sidebar.text_input("Title")
image_file = image_title + ".png"

# Select LLM model
# ----------------
#
# ::

llm_models = ["gpt-image-1", "dall-e-3", "dall-e-2"]

llm_model = st.sidebar.radio("LLM Model", llm_models)

# Select image sizes
#
# ::

image_size_names = {
    "gpt-image-1":["1024x1024", "1536x1024 (Landscape)", "1024x1536 (Portrait)"],
    "dall-e-3": ["1024x1024", "1792x1024", "1024x1792"],
    "dall-e-2": ["1024x1024", "512x512", "256x256"]
}

image_size_name = st.sidebar.radio("Image Size:", image_size_names[llm_model])
image_size = image_size_name.split(" ")[0]

# History functions
# -----------------
#
# ::

# Read history
history = ""
if os.path.exists(history_file):
    with open(history_file, "r", encoding="utf-8") as fin:
        history = fin.read()

def update_history(prompt):
    # Add current date in YYYY-MM-DD format
    current_date = date.today().strftime("%Y-%m-%d")
    new_text = f"{prompt}\n\n{current_date}\n---\n"
  
    # If contents of history_file already starts with new_text then don't update history.
    if history.startswith(new_text):
        return
  
    with open(history_file, 'w', encoding="utf-8") as file:
        file.write(new_text + history)

# Generate image
# --------------
#
# ::

revised_prompt = None
image_url = None

def generate_image(prompt):
    client = OpenAI()
  
    start_time = time.time()

    img = client.images.generate(
        model=llm_model,
        prompt=prompt,
        n=1,
        size=image_size
    )
  
    end_time = time.time()
    st.session_state.execution_time = end_time - start_time
  
    print("-------------------")
    print(img)
    print("-------------------")
    if img.data[0].b64_json is not None:
        image_bytes = base64.b64decode(img.data[0].b64_json)
        with open(image_file, "wb") as f:
            f.write(image_bytes)
          
    global revised_prompt
    revised_prompt = img.data[0].revised_prompt
  
    global image_url
    image_url = img.data[0].url

# Show prompt and history
#
# ::

col1, col2 = st.columns(2)

def button_disabled():
    return len(image_title) == 0
  
with col1:
    prompt = st.text_area(f"Prompt", height=300)
    if st.button("Generate", type="primary", use_container_width=True, disabled=button_disabled()):
        generate_image(prompt)
        update_history(prompt)

with col2:
    history = st.text_area(f"History", value=history.strip(), height=400)
    if st.button("Update", use_container_width=True):
        with open(history_file, 'w', encoding="utf-8") as file:
            file.write(history)
          
# Show image
#
# ::

if revised_prompt is not None:
    st.write("**Revised prompt:**")
    st.write(revised_prompt)

if os.path.exists(image_file):
    st.image(image_file)

if image_url is not None:
    st.image(image_url)

if "execution_time" in st.session_state:
    st.sidebar.write(f"Execution time: `{round(st.session_state.execution_time, 1)}` sec")