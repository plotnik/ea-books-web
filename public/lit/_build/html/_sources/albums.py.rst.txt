Albums
------

Scans the current folder for subfolders, finds the first image in each subfolder, 
and displays all these images along with the names of the folders. 

::

  import streamlit as st
  import os

Print banner.

::

  @st.cache_data
  def print_banner():
      print("""
             .__ ___.                                      
      _____  |  |\\_ |__  __ __  _____   ______            
      \\__  \\ |  | | __ \\|  |  \\/     \\ /  ___/        
       / __ \\|  |_| \\_\\ \\  |  /  Y Y  \\\\___ \\       
      (____  /____/___  /____/|__|_|  /____  >             
           \\/         \\/            \\/     \\/          
                                                
      """)
      return 1

  print_banner()

Get the current folder name

::

  current_folder = os.getcwd()
  folder_name = os.path.basename(current_folder)

Set the title of the app

::

  st.title(folder_name)

Get the list of folders in the current directory

::

  folders = [f for f in os.listdir(current_folder) if os.path.isdir(os.path.join(current_folder, f))]

Iterate through each folder and find the first image

::

  image_paths = []
  captions = []

  for folder in folders:
      folder_path = os.path.join(current_folder, folder)
      images = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

      if images:
          # Get the first image
          first_image_path = os.path.join(folder_path, images[0])

          caption = folder
        
          # Define the path for the 'lyrics' folder
          lyrics_folder_path = os.path.join(folder_path, 'lyrics')
          if os.path.isdir(lyrics_folder_path):
              caption += " (lyrics)"
        
          # Append image path and caption to lists 
          image_paths.append(first_image_path)
          captions.append(caption)

  st.image(image_paths, captions, use_container_width=True) # width=300)