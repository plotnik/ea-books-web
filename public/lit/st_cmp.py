# Compare CSV Lines
# =================
#
# Provides two text areas arranged in two columns and a **Compare** button.
#
# When the button is clicked, the script processes the text from each text area as follows:
#
# * Adds a newline after each comma (``","``)
# * Removes empty lines
# * Saves the resulting text to ``cmp_1.txt`` and ``cmp_2.txt``
# * Opens a VS Code diff view with the following command:
#
# .. code-block:: console
#
#      code --diff cmp_1.txt cmp_2.txt
#
# ----
#
# ::

import streamlit as st
import subprocess
from pathlib import Path


# Print banner

st.set_page_config(
    page_title="cmp-csv", 
    layout="wide",
)

@st.cache_data
def print_banner():
    print("""                                                                                                                                
    .d8888b. 88d8b.d8b. 88d888b.          .d8888b. .d8888b. dP   .dP 
    88'  `"" 88'`88'`88 88'  `88 88888888 88'  `"" Y8ooooo. 88   d8' 
    88.  ... 88  88  88 88.  .88          88.  ...       88 88 .88'  
    `88888P' dP  dP  dP 88Y888P'          `88888P' `88888P' 8888P'   
                        88                                           
                        dP                                           
    """)
    return 1

print_banner()

# Compare toggle

compare_mode = st.toggle("Compare")

# Fill text areas from the existing files

file_1 = Path("cmp_1.txt")
file_2 = Path("cmp_2.txt")

text_1 = ""
if file_1.exists():
    text_1 = file_1.read_text(encoding="utf-8")

text_2 = ""
if file_2.exists():
    text_2 = file_2.read_text(encoding="utf-8")

if compare_mode:
    col1, col2 = st.columns(2)
    
    with col1:
        text_1 = st.text_area("Text 1", height=400, value=text_1)
    
    with col2:
        text_2 = st.text_area("Text 2", height=400, value=text_2)
else:
    text_1 = st.text_area("Text 1", height=400, value=text_1)
    
# .. function:: normalize_text(text: str) -> str

def normalize_text(text: str) -> str:
    # Add newline after each comma
    text = text.replace(",", ",\n")

    # Remove empty lines
    lines = [line for line in text.splitlines() if line.strip()]

    return "\n".join(lines) + "\n"

# Compare 

button_title = "Compare" if compare_mode else "Normalize"
if st.button(button_title, type="primary", width="stretch"):
  
    normalized_1 = normalize_text(text_1)
    file_1.write_text(normalized_1, encoding="utf-8")
    
    if compare_mode:
        normalized_2 = normalize_text(text_2)
        file_2.write_text(normalized_2, encoding="utf-8")
    
        try:
            subprocess.Popen(
                [
                    "code",
                    "--diff",
                    str(file_1),
                    str(file_2),
                ]
            )
            st.success("Files saved and VS Code started.")
        except Exception as e:
            st.error(f"Failed to start VS Code: {e}")
            
    else:
        st.success("Normalized.")