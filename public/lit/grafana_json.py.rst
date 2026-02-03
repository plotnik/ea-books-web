Grafana Record
--------------

Decode Grafana JSON record from clipboard

::

  import streamlit as st
  import pyperclip
  import json

  st.set_page_config(
      page_title="g-rec",
      layout="wide",
  )

  @st.cache_data
  def print_banner():
      print("""
       ,ccc,        =,,[[==,cc[[[cc. ,cc[[[cc.                    
      $$$cc$$$ cccc `$$$\"``$$$___--' $$$                          
      888   888      888   88b    ,o,88b    ,o,                   
       \"YUM\" MP      \"MM,   \"YUMMMMP\" \"YUMMMMP\"                   
            MMM                                                   
      ,c.   ###                                                   
      \\M###MMU   
      """)
      return 1

  print_banner()

  if "clipboard_content" not in st.session_state:
      st.session_state.clipboard_content = ""

  if st.button("Paste", type="primary", use_container_width=True):
      st.session_state.clipboard_content = pyperclip.paste()
    
  st.text_area("Grafana JSON", value=st.session_state.clipboard_content, height=300)
    
  if st.session_state.clipboard_content.startswith("{"):    
      data = json.loads(st.session_state.clipboard_content)    
      st.write(data)