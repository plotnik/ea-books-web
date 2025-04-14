# Book Chat (LangChain)
# =====================
#
# Use Calibre to convert EPUB files into HTML format. 
# This script will then analyze the HTML content using RAG (Retrieval-Augmented Generation) with LangChain.
#
# ::

import streamlit as st
import os
import pyperclip
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_community.vectorstores import FAISS

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

index_folder = "vectors/langchain"
book_html = "html/index.html"
history_file = index_folder + "/history.txt"

# Print current folder
#
# ::

current_folder = os.path.basename(os.getcwd())
st.write(f"### {current_folder}")

# Select LLM
#
# ::

g_key = os.getenv("GEMINI_API_KEY")

llm_models = [
    "gemini-2.0-flash",
    "gemma-3-27b-it",
]
llm_model = st.sidebar.selectbox("LLM Model", llm_models)

llm = ChatGoogleGenerativeAI(model=llm_model, google_api_key=g_key)

# Select Embeddings
#
# ::

embed_model_names = [
    "models/embedding-001",  
    "models/text-embedding-004",
]
embed_model_name = st.sidebar.selectbox("Embedding Model", embed_model_names)

embedding = GoogleGenerativeAIEmbeddings(model=embed_model_name, google_api_key=g_key)

# Load history
#
# ::

history = ""

def update_history(new_text):
    with open(history_file, 'w', encoding="utf-8") as file:
        file.write(new_text + history)
        
if os.path.exists(history_file):
    with open(history_file, "r", encoding="utf-8") as fin:
        history = fin.read()
    
history = st.sidebar.text_area(f"History", value=history.strip(), height=200)

if st.sidebar.button(":recycle: &nbsp; Update history", use_container_width=True):
    update_history("")
    st.toast(f'History updated')   
    
# Create or load index
#
# ::

def create_index(input_file, persist_dir):
    loader = UnstructuredHTMLLoader(input_file)
    documents = loader.load()
    vectorstore = FAISS.from_documents(documents, embedding)
    vectorstore.save_local(persist_dir)
    st.session_state.vstore = vectorstore

def load_index(persist_dir):
    try:
        vectorstore = FAISS.load_local(persist_dir, embedding, allow_dangerous_deserialization=True)
        st.session_state.vstore = vectorstore
    except Exception as e:
        st.error(f"Error loading index: {e}")

# Handle indexing logic
#
# ::

if os.path.exists(index_folder):
    if "vstore" not in st.session_state:
        load_index(index_folder)
else:
    if st.sidebar.button(':construction: &nbsp; Create Index', type='primary', use_container_width=True):
        create_index(book_html, index_folder)
    else:
        st.stop()

# Setup QA chain
#
# ::

if "qa" not in st.session_state:
    retriever = st.session_state.vstore.as_retriever()
    st.session_state.qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff"
    )

# Ask a question
#
# ::

question = st.text_area(f"Question", height=200)

if st.button(":question: &nbsp; Ask", use_container_width=True):
    update_history(question + "\n\n---\n")
    st.session_state.response = st.session_state.qa.invoke(question)
    st.rerun()

if "response" in st.session_state:
    st.write(st.session_state.response)
    if st.sidebar.button(":clipboard: &nbsp; Copy to clipboard", use_container_width=True):
        pyperclip.copy(st.session_state.response)
        st.toast(f'Copied to clipboard')
