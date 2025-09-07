Obsidian Chat (LI)
==================

*Obsidian Chat using LlamaIndex*

To find the Obsidian folder, this script searches the current directory for the first subfolder whose name ends with " Book".

.. csv-table:: LlamaIndex Links
   :header: "Name", "URL"
   :widths: 10 30

   "LlamaIndex Google GenAI Embeddings", https://github.com/run-llama/llama_index/blob/main/docs/docs/examples/embeddings/google_genai.ipynb  
   "Google Embeddings", https://ai.google.dev/gemini-api/docs/embeddings
   "Using VectorStoreIndex - Guide", https://github.com/run-llama/llama_index/blob/main/docs/docs/module_guides/indexing/vector_store_index.md
   "Gemini Model variants", https://ai.google.dev/gemini-api/docs/models/gemini#model-variations

::

  import streamlit as st
  import os
  import json
  from pathlib import Path

  from llama_index.llms.google_genai import GoogleGenAI
  from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
  from llama_index.core import (
      VectorStoreIndex, 
      SimpleDirectoryReader, 
      Settings, 
      StorageContext, 
      load_index_from_storage
  )

Prints a stylized banner to the console when the application starts.

::

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

Folder to save index

::

  index_folder = "vectors/obsidian"

Select LLM

::

  g_key = os.getenv("GEMINI_API_KEY")

  llm_models = [
      "gemini-2.5-flash-preview-05-20",
      "gemini-2.5-pro-preview-05-06",
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

Select Embeddings

::

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

Find Obsidian folder
--------------------

Find Obsidian folder, which is the first subfolder within the current folder that has a name ending with " Book".

::

  current_folder = os.getcwd()
  home_folders = os.listdir(current_folder)
  book_folders = [item for item in home_folders if os.path.isdir(os.path.join(current_folder, item)) and item.endswith(" Book")]

  if (len(book_folders)==0):
      raise Exception('The folder should contain a subfolder with a name that ends with " Book".')

  note_home =  book_folders[0]
  st.title(note_home)

File change detection based on modified timestamps

::

  timestamp_file = os.path.join(index_folder, ".file_timestamps.json")

  def get_all_file_timestamps(folder):
      return {
          str(f): os.path.getmtime(f)
          for f in Path(folder).glob("*.md") if f.is_file()
      }

  def load_previous_timestamps():
      if os.path.exists(timestamp_file):
          with open(timestamp_file, "r") as f:
              return json.load(f)
      return {}

  def save_timestamps(timestamps):
      with open(timestamp_file, "w") as f:
          json.dump(timestamps, f)

  def get_changed_files(current, previous):
      changed = []
      for path, mtime in current.items():
          if path not in previous or previous[path] != mtime:
              changed.append(path)
      return changed

  
Create Index
------------

Creates a new index from documents and persists it.

::

  def create_index(input_dir, persist_dir):
      reader = SimpleDirectoryReader(
          input_dir=input_dir,
          recursive=False
      )
      documents = reader.load_data()
      st.sidebar.info(f"Creating index from {len(documents)} document(s)...")
      st.session_state.index = VectorStoreIndex.from_documents(documents)
      st.session_state.index.storage_context.persist(persist_dir=persist_dir)
      # print(f"Index created and saved successfully!")  
  
      # Save initial timestamps
      current_timestamps = get_all_file_timestamps(input_dir)
      save_timestamps(current_timestamps)


Loads an existing index and refreshes it with current documents.

::

  def load_and_refresh_index(input_dir, persist_dir):
      # print("Loading existing index...")
      try:
          storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
      
          st.session_state.index = load_index_from_storage(storage_context)
          # print("Index loaded successfully!")

          # st.info("Checking for document updates...")
          reader = SimpleDirectoryReader(
              input_dir=input_dir,
              recursive=False # Match the setting used during creation
          )
          current_documents = reader.load_data()
      
          current_timestamps = get_all_file_timestamps(note_home)
          previous_timestamps = load_previous_timestamps()
          changed_files = get_changed_files(current_timestamps, previous_timestamps)
  
          if changed_files:
              changed_docs = SimpleDirectoryReader(input_files=changed_files).load_data()
              st.session_state.index.refresh_ref_docs(changed_docs) # Pass the newly loaded docs
              st.sidebar.success(f"Refreshed {len(changed_docs)} document(s).")
              st.session_state.index.storage_context.persist(persist_dir=persist_dir)
              save_timestamps(current_timestamps)
              # print("Updated index saved.")
          else: 
              st.sidebar.info("No documents changed. Index not updated.")

      except Exception as e:
          st.sidebar.error(f"Error loading or refreshing index: {e}")

Update or create index

::

  if os.path.exists(index_folder):
      if "index" not in st.session_state:
          load_and_refresh_index(note_home, index_folder)
  
  else:
      if st.sidebar.button('Create Index', type='primary', use_container_width=True):
          # Create the index from scratch if it doesn't exist
          #st.sidebar.info("Index not found. Creating a new one...")
          create_index(note_home, index_folder)
      else:
          st.stop()

  
Query
-----

::

  if "query_engine" not in st.session_state:
      st.session_state.query_engine = st.session_state.index.as_query_engine()
  
  question = st.text_area(f"Question", height=200)
  
  if st.button('Ask', type='primary', use_container_width=True):
      response = st.session_state.query_engine.query(question)
      st.write(response.response)
  
  if st.sidebar.button('Update Index', use_container_width=True):
      del st.session_state['index']
      load_and_refresh_index(note_home, index_folder)
  # print("-------------")