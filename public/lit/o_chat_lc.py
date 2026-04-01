# Obsidian Chat (LC)
# ==================
#
# *Obsidian Chat using LancChain*
#
# ::

import streamlit as st
import os
import json
import hashlib
from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import tiktoken

# Print banner.
#
# ::

st.set_page_config(
    page_title="O-Chat"
)

@st.cache_data
def print_banner():
    print("""
     _____        _____ _           _          
    |  _  |      /  __ \\ |         | |        
    | | | |______| /  \\/ |__   __ _| |_       
    | | | |______| |   | '_ \\ / _` | __|      
    \\ \\_/ /      | \\__/\\ | | | (_| | |_    
     \\___/        \\____/_| |_|\\__,_|\\__|                                                          
    """)
    return 1

print_banner()

# Embeddings and LLM costs
#
# ::

embedding_models = {
    "text-embedding-3-small": 0.02,
}

EMBEDDING_MODEL = list(embedding_models.keys())[0]
EMBEDDING_COST_PER_1M = embedding_models[EMBEDDING_MODEL]

index_folder = f"vectors/o-{EMBEDDING_MODEL}"

llm_models = {
    "gpt-5.4": (2.50, 15.00),
    "gpt-5.4-mini": (0.75, 4.50),
    "gpt-5.4-nano": (0.20, 1.25),
    "gpt-4o-mini": (0.15, 0.60),
}

LLM_MODEL = list(llm_models.keys())[3]
LLM_INPUT_COST_PER_1M, LLM_OUTPUT_COST_PER_1M = llm_models[LLM_MODEL]

embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

# Find Obsidian folder, which is the first subfolder within the current folder that has a name ending with " Book".
#
# ::

current_folder = os.getcwd()
home_folders = os.listdir(current_folder)
book_folders = [item for item in home_folders if os.path.isdir(os.path.join(current_folder, item)) and item.endswith(" Book")]

if (len(book_folders)==0):
    st.error('The folder should contain a subfolder with a name that ends with " Book".')
    st.stop()

obsidian_path =  book_folders[0]
st.title(obsidian_path)

# Helpers
# -------
#
# .. method:: count_tokens(text: str, model: str = "cl100k_base") -> int
#
# ::

def count_tokens(text: str, model: str = "cl100k_base") -> int:
    """Return the number of tokens for the given text."""
    enc = tiktoken.get_encoding(model)
    return len(enc.encode(text))

# .. method:: file_md5(path: str) -> str
#
# ::

def file_md5(path: str) -> str:
    """Return MD5 hex-digest for a file."""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

# .. method:: load_hashes(index_folder: str) -> dict
#
# ::

HASH_FILE = ".file_hashes.json"

def load_hashes(index_folder: str) -> dict:
    """Load the previously stored file-hash map."""
    hash_path = os.path.join(index_folder, HASH_FILE)
    if os.path.exists(hash_path):
        with open(hash_path, "r") as f:
            return json.load(f)
    return {}

# .. method:: save_hashes(index_folder: str, hashes: dict)
#
# ::

def save_hashes(index_folder: str, hashes: dict):
    """Persist the file-hash map."""
    os.makedirs(index_folder, exist_ok=True)
    hash_path = os.path.join(index_folder, HASH_FILE)
    with open(hash_path, "w") as f:
        json.dump(hashes, f, indent=2)

# .. method:: detect_changes(obsidian_path: str, index_folder: str)
#
# ::

def detect_changes(obsidian_path: str, index_folder: str):
    """Compare current markdown files against stored hashes.

    Returns:
        changed_files: list of file paths that are new or modified
        deleted_files: list of file paths that no longer exist
        current_hashes: full hash map for the current state
    """
    old_hashes = load_hashes(index_folder)
    current_hashes: dict[str, str] = {}

    md_files = list(Path(obsidian_path).rglob("*.md"))
    for p in md_files:
        fp = str(p)
        current_hashes[fp] = file_md5(fp)

    changed_files = [
        fp for fp, h in current_hashes.items()
        if old_hashes.get(fp) != h
    ]
    deleted_files = [
        fp for fp in old_hashes
        if fp not in current_hashes
    ]
    return changed_files, deleted_files, current_hashes

# Core pipeline
# -------------
#
# .. method:: load_and_split(file_paths: list[str]) -> list
#
# ::

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def load_and_split(file_paths: list[str]) -> list:
    """Load markdown files and split into chunks."""

    documents: list[Document] = []
    for fp in file_paths:
        try:
            loader = TextLoader(fp, encoding="utf-8")
            documents.extend(loader.load())
        except Exception as e:
            st.warning(f"  ⚠ Skipping {fp}: {e}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)

# .. method:: update_index(obsidian_path: str, index_folder: str, embeddings) -> Chroma
#
# ::

def update_index(obsidian_path: str, index_folder: str, embeddings) -> Chroma:
    """Create or incrementally update the Chroma vector store."""
    changed, deleted, current_hashes = detect_changes(obsidian_path, index_folder)

    # Open (or create) the persistent store
    vectorstore = Chroma(
        persist_directory=index_folder,
        embedding_function=embeddings,
        collection_name="obsidian_docs",
    )

    if not changed and not deleted:
        st.sidebar.write("✓ Index is up-to-date — no files changed.")
        return vectorstore

    # --- handle deletions ---------------------------------------------------
    if deleted:
        st.sidebar.write(f"  Removing {len(deleted)} deleted file(s) from index …")
        existing = vectorstore.get()
        ids_to_delete = [
            doc_id
            for doc_id, meta in zip(existing["ids"], existing["metadatas"])
            if meta.get("source") in deleted
        ]
        if ids_to_delete:
            vectorstore.delete(ids=ids_to_delete)

    # --- handle new / modified files ----------------------------------------
    if changed:
        st.sidebar.write(f"  Indexing {len(changed)} new/modified file(s) …")

        # Remove old chunks for modified files first
        existing = vectorstore.get()
        ids_to_delete = [
            doc_id
            for doc_id, meta in zip(existing["ids"], existing["metadatas"])
            if meta.get("source") in changed
        ]
        if ids_to_delete:
            vectorstore.delete(ids=ids_to_delete)

        chunks = load_and_split(changed)
        if chunks:
            # --- Embedding cost estimation ----------------------------------
            total_embed_tokens = sum(count_tokens(c.page_content) for c in chunks)
            embed_cost = (total_embed_tokens / 1000000) * EMBEDDING_COST_PER_1M
            st.sidebar.write(f"  Embedding tokens: {total_embed_tokens:,}  "
                     f"(est. cost ${embed_cost*100:.6f} cents)")

            vectorstore.add_documents(chunks)

    save_hashes(index_folder, current_hashes)
    st.sidebar.write("✓ Index updated.")
    return vectorstore

# .. method:: ask(question: str, vectorstore: Chroma, llm) -> str
#
# ::

def ask(question: str, vectorstore: Chroma, llm) -> str:
    """Run a RAG query and print cost estimates."""
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    template = """Answer the question based only on the following context.
If you cannot answer from the context, say so.

Context:
{context}

Question: {question}
"""
    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n---\n\n".join(d.page_content for d in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    # Retrieve docs to estimate input tokens
    retrieved_docs = retriever.invoke(question)
    context_text = format_docs(retrieved_docs)
    full_input = prompt.format(context=context_text, question=question)
    input_tokens = count_tokens(full_input)

    answer = chain.invoke(question)

    output_tokens = count_tokens(answer)

    input_cost = (input_tokens / 1000000) * LLM_INPUT_COST_PER_1M
    output_cost = (output_tokens / 1000000) * LLM_OUTPUT_COST_PER_1M
    total_cost = input_cost + output_cost

    # Embedding cost for the question itself
    q_embed_tokens = count_tokens(question)
    q_embed_cost = (q_embed_tokens / 1000000) * EMBEDDING_COST_PER_1M

    st.sidebar.write("\n--- Cost Breakdown ---")
    st.sidebar.write(f"  Question embedding : {q_embed_tokens:,} tokens  → ${q_embed_cost:.6f}")
    st.sidebar.write(f"  LLM input          : {input_tokens:,} tokens  → ${input_cost:.6f}")
    st.sidebar.write(f"  LLM output         : {output_tokens:,} tokens  → ${output_cost:.6f}")
    st.sidebar.write(f"  Total LLM answer   : ${total_cost:.6f}")
    st.sidebar.write("----------------------")

    return answer

# Main
# ----
#
# ::

vectorstore = update_index(obsidian_path, index_folder, embeddings)

question = st.text_area(f"Question", height=200)

if st.button('Ask', type='primary', width="stretch"):
    response = ask(question, vectorstore, llm)
    st.write(response)