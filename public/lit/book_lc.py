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
#    "LangGraph Studio", https://studio.langchain.com/
#    "Trace with LangSmith", https://docs.smith.langchain.com/observability/how_to_guides/trace_with_langchain
#    "tracers - LangChain documentation", https://python.langchain.com/api_reference/core/tracers.html
#    "Using Chroma in LangChain", https://python.langchain.com/docs/integrations/vectorstores/chroma/
#    "OpenAI Embeddings Prices", https://platform.openai.com/docs/pricing#embeddings
#    "Gemini Models", https://ai.google.dev/gemini-api/docs/models
#    "Gemini Rate Limits", https://ai.google.dev/gemini-api/docs/rate-limits
#
# ::

import streamlit as st
import os
import pyperclip
import time
from datetime import date

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import UnstructuredHTMLLoader
from langchain_chroma import Chroma 
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.tracers.context import tracing_v2_enabled
from contextlib import nullcontext
import tiktoken

# See: PersistedList_
#
# .. _PersistedList: PersistedList.py.html
#  
# ::

from PersistedList import PersistedList

# Prints a stylized banner to the console when the application starts.
#
# ::

st.set_page_config(
    page_title="Book-Chat",
)

@st.cache_data
def print_banner():
    print("""
    ___  ____ ____ _  _    ____ _  _ ____ ___                   
    |__] |  | |  | |_/  __ |    |__| |__|  |                    
    |__] |__| |__| | \\_    |___ |  | |  |  |                     
    """)
    return 1

print_banner()
st.logo("https://ea-books.netlify.app/lit/book_lc.svg")

# LangSmith tracing
#
# ::

langsmith_tracing = st.sidebar.toggle("LangSmith Tracing", value=False)
tracing_context = tracing_v2_enabled() if langsmith_tracing else nullcontext()

# Get ``GEMINI_API_KEY``
#
# ::

g_key = os.getenv("GEMINI_API_KEY")

# Select Embeddings
#
# ::

embedding_models = [
    "openai/text-embedding-3-small",
    "google/text-embedding-004",           # April 2024
    "google/gemini-embedding-exp-03-07",   # March 2025 # Exceeds rate limit when selected
    "google/embedding-001",                # December 2023
]

embedding_prices = {
    "openai/text-embedding-3-small": 0.02,
    "google/text-embedding-004": 0.0,          
    "google/gemini-embedding-exp-03-07": 0.0,  
    "google/embedding-001": 0.0,                
}

embedding_models_persisted = PersistedList(".book-chat-embeddings")
embedding_models = embedding_models_persisted.sort_by_pattern(embedding_models)

embedding_model = st.sidebar.selectbox("Embedding", embedding_models)

# split `embedding_model` into `model_vendor` before "/" and `embed_model_name` after
embedding_model_vendor, embed_model_name = embedding_model.split("/", 1)

if embedding_model_vendor == "google":
    embedding = GoogleGenerativeAIEmbeddings(model=f"models/{embed_model_name}", google_api_key=g_key)
elif embedding_model_vendor == "openai":
    embedding = OpenAIEmbeddings(model=embed_model_name)
  
# Folder to save index
#
# ::

index_folder = f"vectors/book-{embed_model_name}"

embedding_models_persisted.select(embedding_model)

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
    "google/gemini-2.5-flash-preview-04-17",
    "google/gemini-2.0-flash",
    "google/gemma-3-27b-it",
]

llm_prices = {
    "gpt-4.1-mini": 0.4,
    "gpt-4.1-nano": 0.1,
    "gpt-4.1": 2.0,
    "gpt-4o-mini": 0.15,
    "gpt-4o": 2.5,

    "o3-mini": 1.10,
    "o3": 2.0,
    "o3-pro": 20.0,
}

llm_models_persisted = PersistedList(".book-chat-models")
llm_models = llm_models_persisted.sort_by_pattern(llm_models)

llm_model_selected = st.sidebar.selectbox("LLM", llm_models)
llm_model_vendor, llm_model = llm_model_selected.split("/", 1)

if llm_model_vendor == "google":
    llm = ChatGoogleGenerativeAI(model=llm_model, google_api_key=g_key)
elif llm_model_vendor == "openai":
    llm = ChatOpenAI(model=llm_model, temperature=0.1)

llm_models_persisted.select(llm_model_selected)

# Load history
#
# ::

history = ""

def update_history(prompt):
    # Add current date in YYYY-MM-DD format
    current_date = date.today().strftime("%Y-%m-%d")
    new_text = f"{prompt}\n\n{current_date}\n---\n"

    # If contents of history_file already starts with new_text then don't update history.
    if history.startswith(new_text):
        return

    with open(history_file, 'w', encoding="utf-8") as file:
        file.write(new_text + history)

if os.path.exists(history_file):
    with open(history_file, "r", encoding="utf-8") as fin:
        history = fin.read()

history = st.sidebar.text_area(f"History", value=history.strip(), height=400)

#if st.sidebar.button(":recycle: &nbsp; Update history", use_container_width=True):
#    update_history("")
#    st.toast(f'History updated')   

# Chroma    
# ------
#
# Create or load index
#
# ::

def create_doc_chunks(input_file):
    loader = UnstructuredHTMLLoader(input_file)
    docs = loader.load()

    # split into 1,000‐char chunks with 200‐char overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )  

    chunks = text_splitter.split_documents(docs) 
    return chunks

def create_index(input_file, persist_dir, chunks):
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
    # if "vstore" not in st.session_state:
    load_index(index_folder)
else:
    # No index folder
    chunks = create_doc_chunks(book_html)

    enc = tiktoken.encoding_for_model("text-embedding-3-small")
    total_tokens = sum(len(enc.encode(chunk.page_content)) for chunk in chunks)
    cost = (total_tokens / 1_000_000) * embedding_prices[embedding_model]
    cents = cost/100
  
    st.sidebar.write("**Embeddings price**")
    st.sidebar.write(f'''
        | Chunks | Tokens | Cents |
        |---|---|---|
        | {len(chunks)} | {total_tokens} | {cents} |
        ''')  
  
    if st.sidebar.button(':construction: &nbsp; Create Index', type='primary', use_container_width=True):
        with tracing_context:
            create_index(book_html, index_folder, chunks)
        st.rerun()
    else:
        st.stop()

# Setup QA chain
#
# ::

prompt = ChatPromptTemplate.from_template("""
Answer the user's question based only on the following context.
If the context doesn't contain the answer, state that you don't have enough information.

Context:
{context}

Question: {input}

Answer:
""")

retriever = st.session_state.vstore.as_retriever()
doc_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, doc_chain)

# Ask a question
# --------------
#
# ::

question = st.text_area(f"Question")

if st.button(":question: &nbsp; Ask", use_container_width=True):
    update_history(question)
    start_time = time.time()
    with tracing_context:
        st.session_state.response = rag_chain.invoke({"input": question})
    end_time = time.time()
    st.session_state.execution_time = end_time - start_time
    st.rerun()

if "response" in st.session_state:
    st.write(st.session_state.response["answer"])
    if st.sidebar.button(":clipboard: &nbsp; Copy to clipboard", use_container_width=True):
        pyperclip.copy(st.session_state.response["answer"])
        st.toast(f'Copied to clipboard')

# Show last execution time
#
# ::

if "execution_time" in st.session_state:
    st.sidebar.write(f"Execution time: `{round(st.session_state.execution_time, 1)}` sec")