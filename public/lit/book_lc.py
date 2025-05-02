# Book Chat (LC)
# ==============
#
# *Answer Questions About Book Contents Using RAG with LangChain and Chroma*
#
# 1. Use Calibre to convert EPUB files into HTMLZ format.
# 2. Unpack the HTMLZ archive into an ``html`` folder.
# 3. This script will analyze the ``html/index.html`` file and save the embeddings into a Chroma database.
#
#
# .. _RAG: https://en.wikipedia.org/wiki/Retrieval-augmented_generation
# .. _LangChain: https://python.langchain.com/docs/introduction/
# .. _Chroma: https://www.trychroma.com/
#
# .. code:: shell
#
#     pip install -U chromadb langchain-chroma
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "Using Chroma in LangChain", https://python.langchain.com/docs/integrations/vectorstores/chroma/
#  
# ::

import streamlit as st
import os
import pyperclip
import time

from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_chroma import Chroma 
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Prints a stylized banner to the console when the application starts.
#
# ::

st.set_page_config(
    page_title="Book-Chat",
)

@st.cache_data
def print_banner():
    print("""                                                                            
        ,---,.                           ,-.             ,----..    ,---,                   ___     
      ,'  .'  \\                      ,--/ /|            /   /   \\ ,--.' |                 ,--.'|_   
    ,---.' .' |   ,---.     ,---.  ,--. :/ |     ,---,.|   :     :|  |  :                 |  | :,'  
    |   |  |: |  '   ,'\\   '   ,'\\ :  : ' /    ,'  .' |.   |  ;. /:  :  :                 :  : ' :  
    :   :  :  / /   /   | /   /   ||  '  /   ,---.'   ,.   ; /--` :  |  |,--.  ,--.--.  .;__,'  /   
    :   |    ; .   ; ,. :.   ; ,. :'  |  :   |   |    |;   | ;    |  :  '   | /       \\ |  |   |    
    |   :     \\'   | |: :'   | |: :|  |   \\  :   :  .' |   : |    |  |   /' :.--.  .-. |:__,'| :    
    |   |   . |'   | .; :'   | .; :'  : |. \\ :   |.'   .   | '___ '  :  | | | \\__\\/: . .  '  : |__  
    '   :  '; ||   :    ||   :    ||  | ' \\ \\`---'     '   ; : .'||  |  ' | : ,\" .--.; |  |  | '.'| 
    |   |  | ;  \\   \\  /  \\   \\  / '  : |--'           '   | '/  :|  :  :_:,'/  /  ,.  |  ;  :    ; 
    |   :   /    `----'    `----'  ;  |,'              |   :    / |  | ,'   ;  :   .'   \\ |  ,   /  
    |   | ,'                       '--'                 \\   \\ .'  `--''     |  ,     .-./  ---`-'   
    `----'                                               `---`               `--`---'                                             
    """)
    return 1

print_banner()
st.logo("https://ea-books.netlify.app/lit/book_lc.svg")

# Get ``GEMINI_API_KEY``
#
# ::

g_key = os.getenv("GEMINI_API_KEY")

# Select Embeddings
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "Gemini Models", https://ai.google.dev/gemini-api/docs/models
#    "Gemini Rate Limits", https://ai.google.dev/gemini-api/docs/rate-limits
# 
# ::

embedding_models = [
    "text-embedding-004",           # April 2024
    "gemini-embedding-exp-03-07",   # March 2025 # Exceeds rate limit when selected
    "embedding-001",                # December 2023
]
embed_model_name = st.sidebar.selectbox("Embedding", embedding_models)

embedding = GoogleGenerativeAIEmbeddings(model=f"models/{embed_model_name}", google_api_key=g_key)

# Folder to save index
#
# ::

index_folder = f"vectors/book-{embed_model_name}"

# Input HTML file with the book's contents and a log of the questions asked.
#
# ::

book_html = "html/index.html"
history_file = "vectors/questions.txt"

# Print current folder name as a title
#
# ::

current_folder = os.path.basename(os.getcwd())
st.write(f"### {current_folder}")

# Select LLM
#
# ::

llm_models = [
    "gemini-2.5-pro-exp-03-25",
    "gemini-2.0-flash",
    "gemma-3-27b-it",
]
llm_model = st.sidebar.selectbox("LLM", llm_models)

llm = ChatGoogleGenerativeAI(model=llm_model, google_api_key=g_key)

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
  
# Chroma    
# ------
#
# Create or load index
#
# ::

def create_index(input_file, persist_dir):
    loader = UnstructuredHTMLLoader(input_file)
    docs = loader.load()
  
    # split into 1,000‐char chunks with 200‐char overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )  
  
    chunks = text_splitter.split_documents(docs) 

    # Create a *persistent* Chroma collection in one step
    vectorstore = Chroma.from_documents(
        chunks,
        embedding,
        persist_directory=persist_dir,     # <- where it lives on disk
        collection_name="book"             # any name you like
    )

    st.session_state.vstore = vectorstore

def load_index(persist_dir):
    try:
        # Load an existing collection directly
        vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=embedding,  # same embedder you used to build it
            collection_name="book",        # must match create_index
        )
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
        st.rerun()
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
# --------------
#
# ::

question = st.text_area(f"Question", height=200)

if st.button(":question: &nbsp; Ask", use_container_width=True):
    update_history(question + "\n\n---\n")
    start_time = time.time()
    st.session_state.response = st.session_state.qa.invoke(question)
    end_time = time.time()
    st.session_state.execution_time = end_time - start_time
    st.rerun()

if "response" in st.session_state:
    st.write(st.session_state.response["result"])
    if st.sidebar.button(":clipboard: &nbsp; Copy to clipboard", use_container_width=True):
        pyperclip.copy(st.session_state.response["result"])
        st.toast(f'Copied to clipboard')

# Show last execution time
#
# ::

if "execution_time" in st.session_state:
    st.sidebar.write(f"Execution time: `{round(st.session_state.execution_time, 2)}` sec")