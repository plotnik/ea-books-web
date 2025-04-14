# Book Chat (LlamaIndex)
# ======================
#
# Use Calibre to convert EPUB files into HTML format. 
# This script will then analyze the HTML content using RAG (Retrieval-Augmented Generation) with LlamaIndex.
#
#
# ::

import streamlit as st
import os

from llama_index.llms.google_genai import GoogleGenAI
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.core import (
    VectorStoreIndex, 
    SimpleDirectoryReader, 
    Settings, 
    StorageContext, 
    load_index_from_storage
)

# Prints a stylized banner to the console when the application starts.
#
# ::

@st.cache_data
def print_banner():
    print("""
        ___.                  __                    .__            __   
        \\_ |__   ____   ____ |  | __           ____ |  |__ _____ _/  |_ 
         | __ \\ /  _ \\ /  _ \\|  |/ /  ______ _/ ___\\|  |  \\\\__  \\\\   __\\
         | \\_\\ (  <_> |  <_> )    <  /_____/ \\  \\___|   Y  \\/ __ \\|  |  
         |___  /\\____/ \\____/|__|_ \\          \\___  >___|  (____  /__|  
             \\/                   \\/              \\/     \\/     \\/                                                    
    """)
    return 1

print_banner()

# Folder to save index
#
# ::

index_folder = "vectors/html"
book_html = "html/index.html"

# Select LLM
#
# ::

g_key = os.getenv("GEMINI_API_KEY")

llm_models = [
    "gemini-2.0-flash",
    "gemma-3-27b-it",
]

llm_model = st.sidebar.selectbox(
   "LLM Model",
   llm_models,
)

llm = GoogleGenAI(
    model=llm_model,
    api_key=g_key
)

Settings.llm = llm

# Select Embeddings
#
# ::

embed_model_names = [
    "text-embedding-004",  
    "gemini-embedding-exp-03-07",
]

embed_model_name = st.sidebar.selectbox(
   "Embedding Model",
   embed_model_names,
)

embed_model = GoogleGenAIEmbedding(
    model_name=embed_model_name,
    embed_batch_size=100,
    api_key=g_key,
)

Settings.embed_model = embed_model

# Create Index
# ------------
#
# Creates a new index from input document and persists it.
#
# ::

def create_index(input_file, persist_dir):
    reader = SimpleDirectoryReader(input_files=[input_file])
    documents = reader.load_data()
    print(f"Creating index from {len(documents)} document(s)...")
    st.session_state.index = VectorStoreIndex.from_documents(documents)
    st.session_state.index.storage_context.persist(persist_dir=persist_dir)

# Loads an existing index and refreshes it with current documents.
#
# ::

def load_index(input_dir, persist_dir):
    try:
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        st.session_state.index = load_index_from_storage(storage_context)
    except Exception as e:
        st.error(f"Error loading or refreshing index: {e}")

# Update or create index
#
# ::

if os.path.exists(index_folder):
    if "index" not in st.session_state:
        load_index(book_html, index_folder)
  
else:
    if st.sidebar.button('Create Index', type='primary', use_container_width=True):
        create_index(book_html, index_folder)
    else:
        st.stop()

  
# Query
# -----
#
# ::

if "query_engine" not in st.session_state:
    st.session_state.query_engine = st.session_state.index.as_query_engine()
  
question = st.text_area(f"Question", height=200)
  
if st.button('Ask', type='primary', use_container_width=True):
    response = st.session_state.query_engine.query(question)
    st.write(response.response)

