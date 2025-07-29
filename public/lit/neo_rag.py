# Neo RAG
# =======
#
# *Creates RAG pipeline that combines OpenAI embedding model with Neo4J graph database 
# to enable semantic search.*
#
# ::

import streamlit as st
import os
import tiktoken
from bs4 import BeautifulSoup

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.neo4j_vector import Neo4jVector
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

# Print banner
#
# ::

st.set_page_config(
    page_title="NEO-RAG",
    layout="wide",
)

@st.cache_data
def print_banner():
    print("""
    _  _ ____ ____    ____ ____ ____                            
    |\\ | |___ |  | __ |__/ |__| | __                            
    | \\| |___ |__|    |  \\ |  | |__]                                                                                       
    """)
    return 1

print_banner()

# Input file and embedding model
#
# ::

INPUT_FILE = "html/index.html"
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_PRICE_PER_1M_TOKENS = 0.02

encoding = tiktoken.encoding_for_model(EMBEDDING_MODEL)

# Check if current directory ends with ``_code``
#
# ::

current_dir = os.getcwd()
if not current_dir.endswith("_code"):
    st.error(f"Current directory '{current_dir}' must end with '_code'")
    st.stop()

# Check if ``INPUT_FILE`` exists
#
# ::

if not os.path.exists(INPUT_FILE):
    st.error(f"Input file '{INPUT_FILE}' not found")
    st.stop()

# Name for the Neo4j vector index is based on the book code.
#
# ::

book_code = os.path.basename(current_dir[:-len("_code")])
NEO4J_INDEX_NAME = "vectors_" + book_code

LLM_MODEL = "gpt-4o-mini"

# Prices for different LLMs. 
#
# ::
    
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

# Save history
#
# ::

HISTORY_FILE = "neo-rag.md"

history = ""

def update_history(new_text):
    with open(HISTORY_FILE, 'w', encoding="utf-8") as file:
        file.write(new_text + history)

if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "r", encoding="utf-8") as fin:
        history = fin.read()
    
# Get environment variables
#
# ::

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Check if Neo4j vector index already exists.
#
# A simple way to check is to try to initialize the store.
# If it fails with a specific error (e.g., index not found), it doesn't exist.
#
# We can also potentially use a direct Cypher query for this purpose.
#
# ::
    
def check_index_exists():
    try:
        Neo4jVector.from_existing_index(
            embedding=OpenAIEmbeddings(model=EMBEDDING_MODEL),
            url=NEO4J_URI,
            username=NEO4J_USERNAME,
            password=NEO4J_PASSWORD,
            index_name=NEO4J_INDEX_NAME,
        )
        return True
    except Exception as e:
        # Print exception info for debugging
        # st.error(f"Exception checking index: {e}")
        return False

# Initialize session state to keep track of whether the index is created
#
# ::

if 'index_created' not in st.session_state:
    with st.spinner("Checking for existing index in Neo4j..."):
        st.session_state.index_created = check_index_exists()

# App has two main states: ``Indexing`` or ``Q&A``
#
# State 1: Index Creation
# -----------------------
#
# ::

if not st.session_state.index_created:
    st.header("Step 1: Create Vector Index")
    st.write(f"Index name: `'{NEO4J_INDEX_NAME}'`.")

    # Load and process the file to calculate cost
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    document_text = soup.get_text(separator=" ", strip=True)

    # Calculate token count

    token_count = len(encoding.encode(document_text))

    # Calculate and display cost
    cost = (token_count / 1_000_000) * EMBEDDING_PRICE_PER_1M_TOKENS
    st.info(f"""
    **Cost Calculation:**
    - **Embedding Model:** `{EMBEDDING_MODEL}`
    - **Total Tokens:** `{token_count:,}`
    - **Estimated Cost:** `{cost*100:.6f}` cents
    """)

    if st.button("Create Index", type="primary", use_container_width=True):
        with st.spinner("Processing... This may take a moment."):
            # Chunk the document
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            docs = text_splitter.create_documents([document_text])

            # Create embeddings and store in Neo4j
            Neo4jVector.from_documents(
                documents=docs,
                embedding=OpenAIEmbeddings(model=EMBEDDING_MODEL),
                url=NEO4J_URI,
                username=NEO4J_USERNAME,
                password=NEO4J_PASSWORD,
                index_name=NEO4J_INDEX_NAME, # This will be the name of the node label
                node_label=NEO4J_INDEX_NAME, # And the vector index
                embedding_node_property="embedding",
                text_node_property="text"
            )

            # Update session state and rerun the app
            st.session_state.index_created = True
            st.success("Index created successfully in Neo4j! The app will now reload.")
            st.rerun()
    else:
         st.stop()

# State 2: Question Answering
# ---------------------------
#
# ::

st.header(book_code)
st.success("The document index is available in Neo4j. You can now ask questions!")

# Initialize components for the RAG chain
vectorstore = Neo4jVector.from_existing_index(
    embedding=OpenAIEmbeddings(model=EMBEDDING_MODEL),
    url=NEO4J_URI,
    username=NEO4J_USERNAME,
    password=NEO4J_PASSWORD,
    index_name=NEO4J_INDEX_NAME,
)
retriever = vectorstore.as_retriever()
llm = ChatOpenAI(model=LLM_MODEL, temperature=0.3)

# Define the prompt template
prompt = ChatPromptTemplate.from_template("""
Answer the user's question based only on the following context.
If the context doesn't contain the answer, state that you don't have enough information.

Context:
{context}

Question: {input}

Answer:
""")

# Create the RAG chain
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#   
#     "create_stuff_documents_chain", https://python.langchain.com/api_reference/langchain/chains/langchain.chains.combine_documents.stuff.create_stuff_documents_chain.html?utm_source=chatgpt.com
#
# ::

doc_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, doc_chain)

def update_history_note():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    answer_note = f"""
### {timestamp}

> {st.session_state.user_question}

{st.session_state.answer}

---
"""
    update_history(answer_note)
    st.toast("Saved to history!")
      
if 'user_question' not in st.session_state:
    st.session_state.user_question = ""
  
if 'answer' not in st.session_state:
    st.session_state.answer = ""
  
if 'context' not in st.session_state:
    st.session_state.context = None   
  
# Get user input
#
# ::

st.session_state.user_question = st.text_input("Enter your question here:", value=st.session_state.user_question)


if st.button("Ask", type="primary", use_container_width=True):
    # Invoke the chain to get a response
    response = rag_chain.invoke({"input": st.session_state.user_question})

    # Display the answer
    st.markdown("### Answer")
    st.session_state.answer = response["answer"]
    st.session_state.context = response["context"]

if len(st.session_state.answer) == 0:
    st.stop()
  
st.write(st.session_state.answer)    

if st.button("Save", use_container_width=True):
    update_history_note()

# Display the sources (optional but good practice)
input_tokens = 0
with st.expander("Show Retrieved Context"):
    for i, doc in enumerate(st.session_state.context):
        st.info(f"**Source Chunk {i+1}**\n\n" + doc.page_content)
        input_tokens += len(encoding.encode(doc.page_content))

# Calculate cost (prices are per 1M tokens)
llm_cost = (input_tokens / 1_000_000) * llm_prices.get(LLM_MODEL, 0)

st.info(f"""
**LLM Cost Calculation:**
- **Model:** `{LLM_MODEL}`
- **Input Tokens:** `{input_tokens:,}`
- **Estimated Cost:** `{llm_cost*100:.6f} cents`
""")
      



       