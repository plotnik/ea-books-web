# exc UI
# ------
#
# Processing log files in current directory with exc_ and exc_yaml_.
#
# .. _exc: https://github.com/a-services/jbang-catalog/blob/main/exc.java
# .. _exc_yaml: exc_yaml.py.html
#
# ::

import os
import streamlit as st
import subprocess

# Step 1: Get the list of .log files in the current directory
#
# ::
    
log_files = [f for f in os.listdir('.') if f.endswith('.log')]

# Step 2: Sort the log files alphabetically
#
# ::
    
log_files_sorted = sorted(log_files)

# Step 3: Create radio buttons to select a file
#
# ::
    
selected_file = st.radio("Select a log file to process:", log_files_sorted)

# Step 4: Button to process the selected file
#
# ::
    
if st.button("Process"):
    subprocess.run(["exc", selected_file, '--html', '--skip=20', '--tformat=yyyy/MM/dd HH:mm:ss', '--restart=wrapper.tanukisoftware.org'], check=True)
    subprocess.run(["exc_yaml", selected_file], check=True)
  
    st.write(f"Processed: `{selected_file}`")
