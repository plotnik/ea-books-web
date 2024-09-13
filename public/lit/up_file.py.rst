Upload File
-----------

::

  import streamlit as st
  import os

Path for the folder to save the uploaded files

::
    
  SAVE_PATH = os.path.expanduser('~') + "/Downloads"
  st.write(f"### Upload File to `{SAVE_PATH}`")

Print banner.

::
    
  @st.cache_data
  def print_banner():
      print("""
                               _____.__.__               
       __ ________           _/ ____\\__|  |   ____      
      |  |  \\____ \\   ______ \\   __\\|  |  | _/ __ \\ 
      |  |  /  |_> > /_____/  |  |  |  |  |_\\  ___/     
      |____/|   __/           |__|  |__|____/\\___  >    
            |__|  
      """)
      return 1

  print_banner()

Save the uploaded zip file in the specified directory.

::
    
  def save_uploadedfile(uploadedfile):
      with open(os.path.join(SAVE_PATH, uploadedfile.name), "wb") as f:
          f.write(uploadedfile.getbuffer())
      st.write(f"Saved file: `{uploadedfile.name}` to `{SAVE_PATH}`")

  up_type = st.radio("Upload type:", ["jpg", "zip", "md"])

  uploaded_file = st.file_uploader(f"Choose {up_type} file", type=up_type)
  if uploaded_file is not None:
      save_uploadedfile(uploaded_file)