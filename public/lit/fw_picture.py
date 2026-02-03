# FW Picture
# ==========
#
# Streamlit + LangChain app to suggest a picture plot for a diary entry.
#
# - Select among popular OpenAI and Google models (order is persisted).
# - Enter diary text and get a suggested picture plot.
#
# API keys:
#   - Set environment variables ``OPENAI_API_KEY`` and ``GEMINI_API_KEY``
#     or enter them in the sidebar inputs.
#
# ::

import os
import json
from pathlib import Path

import streamlit as st

# LangChain components
#
# ::

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Prompt
#
# ::

PICTURE_PROMPT = """
You are a creative assistant. Given a personal diary entry, 
propose a single, vivid, camera-ready picture plot that could illustrate the entry. 
Keep it concise (60–120 words). Include: subject, setting, mood, style/medium, key visual elements. 
"Avoid first person; write as a scene description.
"""

# Model specifications
#
# ::

MODEL_ORDER_DEFAULT = [
    "openai/gpt-5",
    "google/gemma-3-27b-it",
    "openai/gpt-5-mini",
    "google/gemini-2.5-pro",
    "google/gemini-2.5-flash",
    "google/gemini-2.5-flash-lite",
]

# Extracts provider and model name from a model ID.
# Args:
#   model_id: The model ID in the format "provider/model".
# Returns:
#   A tuple (provider, model).
# ::

def extract_model_spec(model_id: str) -> dict:
    provider, model = model_id.split("/")
    return {"provider": provider, "model": model}

# See: PersistedList_
#
# .. _PersistedList: PersistedList.py.html
#   
# ::

from PersistedList import PersistedList

# LLM
# ---
#
# ::
    
def get_llm(model_id: str):
    spec = extract_model_spec(model_id)
    provider = spec["provider"]
    model_name = spec["model"]
    temperature = 0.1

    if provider == "openai":
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            raise RuntimeError(
                "Missing dependency: pip install langchain-openai"
            )
        # ChatOpenAI will read OPENAI_API_KEY from env
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is not set.")
        return ChatOpenAI(model=model_name, temperature=temperature)

    if provider == "google":
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
        except ImportError:
            raise RuntimeError(
                "Missing dependency: pip install langchain-google-genai"
            )
        # ChatGoogleGenerativeAI will read GEMINI_API_KEY from env
        if not os.environ.get("GEMINI_API_KEY"):
            raise RuntimeError("GEMINI_API_KEY is not set.")
        return ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

    raise ValueError(f"Unknown provider: {provider}")


# Use ``ChatPromptTemplate`` to separate prompt and user input

def build_chain(llm):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                PICTURE_PROMPT,
            ),
            ("human", "{diary}"),
        ]
    )
    return prompt | llm | StrOutputParser()

# main
#
# ::

st.set_page_config(page_title="FW Picture", page_icon="🎨")
st.title("🎨 FW Picture")

# Persisted order

model_order_persisted = PersistedList(".fw_picture")
order = model_order_persisted.sort_by_pattern(MODEL_ORDER_DEFAULT)

# Determine current selection id (persisted across reruns)
selected_id = st.session_state.get("model_selected_id")

# Build options by current order
option_labels = order

# Always show the last-selected model first in the list (index 0)
new_selected_id = st.selectbox("Model", options=option_labels, index=0, key="model_select_label")

# Update selected_id and persist ordering if changed
if new_selected_id != selected_id:
    model_order_persisted.select(new_selected_id)

diary_text = st.text_area(
    "Freewrite",
    height=200,
    key="diary_text",
)

if st.button("Suggest picture plot", type="primary", width="stretch"):
    if not diary_text.strip():
        st.warning("Please enter a diary entry.")
        st.stop()
    try:
        llm = get_llm(st.session_state.model_selected_id)
    except Exception as e:
        st.error(f"Model initialization failed: {e}")
        st.stop()

    chain = build_chain(llm)
    with st.spinner("Thinking up a picture plot..."):
        try:
            suggestion = chain.invoke({"diary": diary_text})
        except Exception as e:
            st.error(f"Generation failed: {e}")
            st.stop()

    st.subheader("Suggested picture plot")
    st.write(suggestion)



