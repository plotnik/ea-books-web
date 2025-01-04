# Llamaindex Router
# -----------------
#
# Read Markdown documents from the folder, index them using OpenAI embeddings, and provide answers to questions regarding the content.
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "Building Agentic RAG with Llamaindex", https://learn.deeplearning.ai/courses/building-agentic-rag-with-llamaindex/
#    "LlamaIndex", https://docs.llamaindex.ai/en/stable/
#    "Getting Started", https://docs.llamaindex.ai/en/stable/#getting-started
#    "Starter Tutorial (Local Models)", https://docs.llamaindex.ai/en/stable/getting_started/starter_example_local/#starter-tutorial-local-models
#    "RAG CLI", https://docs.llamaindex.ai/en/stable/getting_started/starter_tools/rag_cli/
#    "RAG CLI using Local Model", https://github.com/run-llama/llama_index/issues/17013
#
#
# Python code in this chapter demonstrates the use of the LlamaIndex library to process and query text data, specifically from a directory containing Markdown files. The code sets up a system to summarize documents and retrieve specific information, using two types of query engines: one for summarization and one for context retrieval.
#
# **Data Loading:**
#
# - The `data_dir` variable specifies the directory containing the text documents.
# - The `SimpleDirectoryReader` class from LlamaIndex is used to load documents from this directory.
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#   
#    "SimpleDirectoryReader", https://docs.llamaindex.ai/en/stable/module_guides/loading/simpledirectoryreader/#simpledirectoryreader
#   
# ::
    
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("data_dir", help="Directory containing Markdown documents")
args = parser.parse_args()

print("Data dir: " + args.data_dir)

from llama_index.core import SimpleDirectoryReader

# load documents
documents = SimpleDirectoryReader(args.data_dir).load_data()

# Define LLM and Embedding model
#
# **Text Processing:**
#
# - The `SentenceSplitter` is initialized with a `chunk_size` of 1024, which means documents will be split into chunks of 1024 characters.
# - `get_nodes_from_documents` breaks down the documents into manageable nodes (chunks of text).
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#   
#    "SentenceSplitter", https://docs.llamaindex.ai/en/stable/api_reference/node_parsers/sentence_splitter/#llama_index.core.node_parser.SentenceSplitter
#    "Using LLMs", https://docs.llamaindex.ai/en/stable/module_guides/models/llms/
#
# ::

from llama_index.core.node_parser import SentenceSplitter

splitter = SentenceSplitter(chunk_size=1024)
nodes = splitter.get_nodes_from_documents(documents)

# **Model Setup:**
#
# - The code defines a language model (LLM) and an embedding model using the OpenAI `gpt-4o-mini` model for language processing and `text-embedding-3-small` for generating text embeddings.
# - This setup is made using the `Settings` class from the LlamaIndex library.
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#   
#    "Settings", https://docs.llamaindex.ai/en/stable/module_guides/supporting_modules/settings/
#    "Ollama", https://docs.llamaindex.ai/en/stable/examples/llm/ollama/
#    "OpenAIEmbedding", https://docs.llamaindex.ai/en/stable/api_reference/embeddings/openai/#llama_index.embeddings.openai.OpenAIEmbedding
#    "OllamaEmbedding", https://docs.llamaindex.ai/en/stable/api_reference/embeddings/ollama/#llama_index.embeddings.ollama.OllamaEmbedding
#
# ::  
  
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding

Settings.llm = OpenAI(model="gpt-4o-mini")
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")

# **Index Creation:**
#
# Two types of indices are created:
#
# - `SummaryIndex`: Used for summarizing documents.
# - `VectorStoreIndex`: Used for retrieving specific context or information from the documents.
#
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#   
#    "Document Summary Index", https://docs.llamaindex.ai/en/stable/examples/index_structs/doc_summary/DocSummary/
#    "VectorStoreIndex", https://docs.llamaindex.ai/en/stable/examples/vector_stores/SimpleIndexDemoLlama2/
#    "Starter Tutorial (OpenAI)", https://docs.llamaindex.ai/en/stable/getting_started/starter_example/
#    
# ::

from llama_index.core import SummaryIndex, VectorStoreIndex

summary_index = SummaryIndex(nodes)
vector_index = VectorStoreIndex(nodes)


# **Query Engine Initialization:**
#
# Two query engines are initialized:
#
# - `summary_query_engine`: Configured for summarization tasks, using a tree-based summarization response mode and asynchronous processing.
# - `vector_query_engine`: Configured for retrieving specific contexts from the documents.
#
# ::

summary_query_engine = summary_index.as_query_engine(
    response_mode="tree_summarize",
    use_async=True,
)
vector_query_engine = vector_index.as_query_engine()

# **Tool Definition:**
#
# `QueryEngineTool` instances are created for each query engine to facilitate query processing:
#
# - `summary_tool`: For summarization queries.
# - `vector_tool`: For context retrieval queries.
#     
# ::
    
from llama_index.core.tools import QueryEngineTool

summary_tool = QueryEngineTool.from_defaults(
    query_engine=summary_query_engine,
    description=(
        "Useful for summarization questions related to the book"
    ),
)

vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description=(
        "Useful for retrieving specific context from the book."
    ),
)

# **Router Query Engine:**
#
# - A `RouterQueryEngine` is set up to handle queries using a selector (`LLMSingleSelector`) that chooses the appropriate query engine tool based on the query type.
# - `verbose=True` enables detailed logging of the query processing.
#
# ::

from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector

query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults(),
    query_engine_tools=[
        summary_tool,
        vector_tool,
    ],
    verbose=True
)

# **Query Execution:**
#
# - The `query_engine` is used to execute a query asking for a summary of the document.
# - The response is printed, along with the number of source nodes (chunks of text) involved in generating the response.
#
# ::
    
response = query_engine.query("What is the summary of the document?")
print(str(response))

print(len(response.source_nodes))

# In summary, this code sets up a system to load and process text data from a directory, create indices for summarization and context retrieval, and execute queries using a router query engine that selects the appropriate processing tool based on the query type.  