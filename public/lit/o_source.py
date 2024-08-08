# --------------------
# Obsidian Page Source
# --------------------
#
# Provide markdown source for Obsidian page in ``textarea``
#
# ::

import streamlit as st
import json
import os

# Select Obsidian folder from recent vaults.
#
# ::

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

obsidian_name = st.selectbox(
   "Obsidian folder",
   obsidian_names,
)

note_home = obsidian_folders[obsidian_names.index(obsidian_name)]

# Get ``num_files`` newest files from the provided directory.
#
# ::

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

# Select ``note_name`` from 5 newest notes
#
# ::

newest_files = get_newest_files(note_home, 5)
note_name = st.selectbox(
   "Note",
   newest_files,
)

# Read the contents of Obsidian page to ``note_text``
#
# ::

file_path = os.path.join(note_home, note_name)
with open(file_path, 'r', encoding='utf-8') as file:
    note_text = file.read()

st.code(note_name)

st.code(note_text)