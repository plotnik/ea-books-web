LlamaIndex Extractors 
=====================

Use LlamaIndex Extractors with Gemini on Obsidian folder.

::

  import streamlit as st
  import os

  from llama_index.core import SimpleDirectoryReader, Settings
  from llama_index.llms.gemini import Gemini
  from llama_index.core.llms.mock import MockLLM
  from llama_index.core.node_parser import SentenceSplitter

  from llama_index.core.extractors import SummaryExtractor
  from llama_index.core.extractors import QuestionsAnsweredExtractor
  from llama_index.core.callbacks import (
      CallbackManager, 
      TokenCountingHandler
  )

  import google.generativeai as genai

.. csv-table:: LlamaImdex Links
   :header: "Name", "URL"
   :widths: 10 30
 
   "LlamaImdex Gemini Integration", https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/llms/llama-index-llms-gemini
   "LlamaImdex Gemini Example", https://docs.llamaindex.ai/en/stable/examples/llm/gemini/
   "LlamaIndex Google GenAI Embeddings", https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/embeddings/google_genai.ipynb
  
.. csv-table:: Gemini Links
   :header: "Name", "URL"
   :widths: 10 30
  
   "Gemini Model variants", https://ai.google.dev/gemini-api/docs/models/gemini#model-variations
   "Gemma Models", https://ai.google.dev/gemma/docs
   "Gemini Text generation", https://ai.google.dev/gemini-api/docs/text-generation?lang=python
   "Gemini Rate limits", https://ai.google.dev/gemini-api/docs/rate-limits
   "Gemini OpenAI compatibility", https://ai.google.dev/gemini-api/docs/openai
   "Gemini Example applications", https://ai.google.dev/gemini-api/docs/models/generative-models#example-applications
   "Google Gen AI SDKs", https://ai.google.dev/gemini-api/docs/sdks

Select Gemini LLM

::

  llm_models = [
      "mock",
      "gemini-2.0-flash",
      "gemini-2.0-flash-lite",
      "gemma-3-27b-it",    
  ]

  llm_model = st.sidebar.selectbox(
     "LLM Model",
     llm_models
  )

  if llm_model == "mock":
      Settings.llm = MockLLM(max_tokens=256)
  else:    
      Settings.llm = Gemini(model=f"models/{llm_model}")
    
  counter = TokenCountingHandler(verbose=False)
  callback_manager = CallbackManager([counter])
  Settings.callback_manager = CallbackManager([counter])

Find Obsidian folder
--------------------

Find Obsidian folder, which is the first subfolder within the current folder that has a name ending with " Book".

::

  current_folder = os.getcwd()
  home_folders = os.listdir(current_folder)
  book_folders = [item for item in home_folders if os.path.isdir(os.path.join(current_folder, item)) and item.endswith(" Book")]

  if (len(book_folders)==0):
      st.error('The folder should contain a subfolder with a name that ends with " Book".')
      st.stop()

  note_home =  book_folders[0]

Process Documents
-----------------

Read Documents

::

  reader = SimpleDirectoryReader(
      input_dir=note_home,
      recursive=False
  )
  documents = reader.load_data()

Parse Nodes

::

  parser = SentenceSplitter(include_prev_next_rel=True)
  nodes = parser.get_nodes_from_documents(documents)
  st.write(f"Documents: `{len(documents)}`, Nodes: `{len(nodes)}`")

List Google Models
------------------

::

  if st.sidebar.button("List Google Models", use_container_width=True):
      for m in genai.list_models():
          if "generateContent" in m.supported_generation_methods:
              st.write(m.name)
    
Extractors
----------

Extract Summaries

::

  st.warning("""
      For large documents you will get an error:  
      **google.api_core.exceptions.ResourceExhausted: 429 Resource has been exhausted (e.g. check quota).**
      """)

  if st.button("Extract Summaries", type='primary', use_container_width=True):
      summary_extractor = SummaryExtractor(summaries=["prev", "self", "next"])
      metadata_list = summary_extractor.extract(nodes)
    
      st.write(f"metadata_list: {len(metadata_list)}")
      st.write(metadata_list)
    
Ask Questions

::
    
  if st.button("Ask Questions", use_container_width=True):
      extractor = QuestionsAnsweredExtractor(show_progress=False)
      metadata_list = extractor.extract(nodes)
    
      st.write(f"metadata_list: {len(metadata_list)}")
      st.write(metadata_list)
    
Tokens Info

::

  st.sidebar.write("---")    
  st.sidebar.write(f"Prompt Tokens: {counter.prompt_llm_token_count}")
  st.sidebar.write(f"Completion Tokens: {counter.completion_llm_token_count}")
  st.sidebar.write(f"Total Token Count: {counter.total_llm_token_count}")
    

    

