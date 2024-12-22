-------------------
Obsidian Web Editor
-------------------

Edit markdown source for Obsidian page in ``textarea``

By the way, jbang_ version appears to be more stable.

.. _jbang: https://github.com/a-services/jbang-catalog/blob/main/o_ed.java

::

  import streamlit as st
  import json
  import os

Print banner.

::

  @st.cache_data
  def print_banner():
      print("""                                                    
                                                 o       
                                                <|>      
                                                < \\     
        o__ __o               o__  __o     o__ __o/      
       /v     v\\   _\\__o__   /v      |>   /v     |     
      />       <\\       \\   />      //   />     / \\   
      \\         /           \\o    o/     \\      \\o/  
       o       o             v\\  /v __o   o      |      
       <\\__ __/>              <\\/> __/>   <\\__  / \\                                                                                               
      """)
      return 1

  print_banner()

Get the list of Obsidian recent vaults from JSON.

::

  home_folder = os.path.expanduser('~')
  obsidian_json_path = f"{home_folder}/Library/Application Support/obsidian/obsidian.json"
  with open(obsidian_json_path, "r") as json_file:
      obsidian_json = json.load(json_file)

  obsidian_vaults = obsidian_json.get('vaults')

  # Extract the values from the dictionary and sort them based on the 'ts' key
  sorted_vaults = sorted(obsidian_vaults.values(), key=lambda x: x['ts'], reverse=True)

  # Extract the 'path' from each sorted entry
  obsidian_folders = [vault['path'] for vault in sorted_vaults]

  obsidian_names = [os.path.basename(folder) for folder in obsidian_folders]


Select Obsidian vault as ``note_home`` from the list of recent vaults.  

::
    
  obsidian_name = st.sidebar.selectbox(
     "Obsidian",
     obsidian_names,
  )

  note_home = obsidian_folders[obsidian_names.index(obsidian_name)]

Get subfolders of Obsidian folder.

::
    
  all_dir_items = os.listdir(note_home)
  subfolders = [item for item in all_dir_items if os.path.isdir(os.path.join(note_home, item)) and item != ".obsidian"]
  subfolders.insert(0, ".")
      
  subfolder = st.sidebar.selectbox(
     "Folder",
     subfolders,
  )

  note_folder = os.path.join(note_home, subfolder)

Get ``num_files`` newest files from the provided directory.

::

  def get_newest_files(directory, num_files):
      # Check if the directory exists
      if not os.path.isdir(directory):
          raise ValueError(f"The directory {directory} does not exist.")

      # Get a list of files in the directory with their full paths and modification times
      files_with_paths = []
      for file_name in os.listdir(directory):
          file_path = os.path.join(directory, file_name)
          if os.path.isfile(file_path):
              files_with_paths.append((file_path, os.path.getmtime(file_path)))

      # Sort files by modification time in descending order (newest first)
      sorted_files = sorted(files_with_paths, key=lambda x: x[1], reverse=True)

      # Extract the num_files newest file names
      newest_files = [os.path.basename(file_with_path[0]) for file_with_path in sorted_files[:num_files]]

      return newest_files

Select ``note_name`` from 5 newest notes

::

  newest_files = get_newest_files(note_folder, 5)
  note_name = st.sidebar.selectbox(
     "Page",
     newest_files,
  )

Read the contents of Obsidian page to ``note_text``

::

  file_path = os.path.join(note_folder, note_name)
  with open(file_path, 'r', encoding='utf-8') as file:
      note_text = file.read()
 
Add Streamlit widgets for editing.

::  

  st.header(note_name, divider=True)

  note_text = st.text_area("Note", note_text, height=400)    

Save updates.

::
    
  if st.button('Save'):
      with open(file_path, 'w') as file:
          file.write(note_text)  
      
      st.write(f'Page saved: `{note_name}`')    