Compare Text
============

::

  import streamlit as st
  import subprocess
  import os

  st.set_page_config(
      page_title="Cmp Text",
      layout="wide",
  )

  col1, col2 = st.columns(2)

  with col1: 
      t1 = st.text_area("1", height=500)

  with col2: 
      t2 = st.text_area("2", height=500)  

  fname1 = "cmp_text_1.txt"
  fname2 = "cmp_text_2.txt"
  output_name = "cmp_text.diff"

  if st.button("Compare", type="primary", width="stretch"):   
      with open(fname1, 'w') as f:
          f.write(t1)
      with open(fname2, 'w') as f:
          f.write(t2) 

      with open(output_name, "w") as output_file:    
          try:
              subprocess.run(
                  ["diff", fname1, fname2], 
                  check=True,
                  stdout=output_file,
                  stderr=output_file,
                  cwd=os.getcwd()
              )
              st.success(f"Same text")
            
          except subprocess.CalledProcessError as e:
              with open(output_name, 'r') as f:
                  diff = f.read()   

              st.write(f"```diff\n{diff}\n```")  
          