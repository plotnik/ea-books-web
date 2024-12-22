Markdown Viewer
---------------

::

  import os
  import streamlit as st

Print banner.

::

  @st.cache_data
  def print_banner():
    print("""                                                    
                   .___              .__                        
        _____    __| _/        ___  _|__| ______  _  __         
       /     \\  / __ |  ______ \\  \\/ /  |/ __ \\ \\/ \\/ /   
      |  Y Y  \\/ /_/ | /_____/  \\   /|  \\  ___/\\     /      
      |__|_|  /\\____ |           \\_/ |__|\\___  >\\/\\_/      
            \\/      \\/                       \\/              
                                                                                          
    """)
    return 1

  print_banner()

Get the list of `.md` files in the current directory

::

  md_files = [f for f in os.listdir('.') if f.endswith('.md')]

Sort files based on their modification time

::

  md_files.sort(key=os.path.getmtime, reverse=True)

Create radio buttons to select a file

::

  selected_file = st.sidebar.radio("Select markdown file:", md_files)

Read the contents of selected file

::

  with open(selected_file, 'r', encoding='utf-8') as file:
      md_text = file.read()
  
  st.write(md_text)    