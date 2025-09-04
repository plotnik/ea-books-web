Bilingua
========

::

  import streamlit as st
  import os
  import pickle
  import yaml
  from pathlib import Path
  import re
  from datetime import datetime

Print banner

::

  st.set_page_config(
      page_title="Bilingua", 
      layout="wide"
  )

  @st.cache_data
  def print_banner():
      print("""
       _     _ _ _                                                
      | |__ (_) (_)_ __   __ _ _   _  __ _                        
      | '_ \\| | | | '_ \\ / _` | | | |/ _` |                       
      | |_) | | | | | | | (_| | |_| | (_| |                       
      |_.__/|_|_|_|_| |_|\\__, |\\__,_|\\__,_|                       
                         |___/                                    
      """)
      return 1

  print_banner()

Init state

::

  DEFAULTS = {
      "page": 0, 
      "ptr": 0,
  }

  state_file = "bi.state"
  config_file = "bi.yml"
  page_len = 5

Serialize selected Streamlit session state variables to a pickle file.

::

  def save_session_state(file_path: str = state_file) -> None:
      data = {k: st.session_state.get(k, DEFAULTS[k]) for k in DEFAULTS}
      with open(file_path, "wb") as f:
          pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)


Load session state variables from a pickle file if it exists.
If not found or on error, assign default values.

::

  def load_session_state(file_path: str = state_file) -> None:
      loaded = {}
      if os.path.exists(file_path):
          try:
              with open(file_path, "rb") as f:
                  obj = pickle.load(f)
              if isinstance(obj, dict):
                  loaded = obj
          except Exception:
              loaded = {}

      for key, default in DEFAULTS.items():
          st.session_state[key] = loaded.get(key, default)
        
Load YML file with configurations

::

  def load_yaml_config(yaml_path: Path) -> dict:
      with yaml_path.open("r", encoding="utf-8") as f:
          return yaml.safe_load(f)
        
Normalize newlines and split on blank lines

::

  def split_paragraphs(text: str) -> list[str]:
      text = text.replace("\r\n", "\n").replace("\r", "\n").strip()
      if not text:
          return []
      parts = re.split(r"\n\s*\n+", text)
      return [p.strip() for p in parts]  
    
  def read_text(path: Path) -> str:
      # Print current time in hh:mm:ss format
      current_time = datetime.now().strftime("%H:%M:%S")
      # print(f"[{current_time}] Reading {path}")
      return path.read_text(encoding="utf-8")
    
Main

::

  load_session_state()
  cfg = load_yaml_config(Path(config_file))   
  obsidian_path = Path(cfg["book"])
  left_name = cfg["left"]
  right_name = cfg["right"]
  left_path = obsidian_path / left_name
  right_path = obsidian_path / right_name

Check if paths to original Obsidian files exist

::

  if not left_path.exists():
      st.error(f"Left file not found: {left_path}")
      st.stop()
  if not right_path.exists():
      st.error(f"Right file not found: {right_path}")
      st.stop()   

Check if there are markdown files with the same names in current folder.
If yes, then use them

::

  if os.path.exists(left_name):
      left_path = Path(left_name)
  if os.path.exists(right_name):
      right_path = Path(right_name)    
    
Load markdown files

::

  left_text = read_text(left_path)
  right_text = read_text(right_path)

  left_pars = split_paragraphs(left_text)
  right_pars = split_paragraphs(right_text)        
  ptr = st.session_state.ptr
  max_page = max(len(left_pars), len(right_pars)) // page_len

Page transitions

::

  def prev_page():
      if st.session_state.page > 0:
          st.session_state.page -= 1
          st.session_state.ptr = page_len - 1
          save_session_state()
          st.rerun() 

  def next_page():
      if st.session_state.page < max_page-1:
          st.session_state.page += 1
          st.session_state.ptr = 0
          save_session_state()
          st.rerun() 
        
  def prev_par():
      if st.session_state.ptr > 0:
          st.session_state.ptr -= 1
          save_session_state()
          st.rerun() 
      else:
          prev_page()
        
  def next_par():
      if st.session_state.ptr < page_len-1:
          st.session_state.ptr += 1
          save_session_state()
          st.rerun() 
      else:
          next_page()
        
Top row of buttons
            
::

  col_1, col_2, col_3 = st.columns(3)
  with col_1:
      if st.button("Prev", width="stretch", icon=":material/step_out:"):
          prev_par()
            
  with col_2:
      if st.button("Next", width="stretch", icon=":material/step_into:"):
          next_par()
           
  with col_3:
      style = "text-align: right; font-weight: bold; font-size: small; text-decoration: underline; margin-right: 20px;"
      st.html(f"<div style='{style}'>Page {st.session_state.page+1}</div>")

Show 2 columns of bilingua text

::

  page_start = st.session_state.page * page_len
  for i in range(page_start, page_start + page_len):
      col_left, col_right = st.columns(2)
      lp = left_pars[i] if i < len(left_pars) else ""
      rp = right_pars[i] if i < len(right_pars) else ""
      with col_left:
          if i==ptr+page_start:
              st.session_state.left_text = st.text_area("lp", lp, height="content", label_visibility="hidden")
          else:
              st.markdown(lp)
      with col_right:
          if i==ptr+page_start:
              st.session_state.right_text = st.text_area("rp", rp, height="content", label_visibility="hidden")
          else:
              st.markdown("> " + rp)  
                
Bottom row of buttons              

::

  st.divider()

  col_1, col_2, col_3 = st.columns(3)
            
  with col_1:    
      if st.button("Prev Page", width="stretch", icon=":material/step_out:"):
          prev_page()
    
  with col_2:    
      if st.button("Next Page", width="stretch", icon=":material/step_into:"): 
          next_page()
    
  with col_3:
      if st.button("Save", type="primary", width="stretch"):
          # Save left_pars to left_name file
          left_pars[ptr+page_start] = st.session_state.left_text
          with open(left_name, "w", encoding="utf-8") as f:
              f.write("\n\n".join(left_pars))            
          # Save right_pars to right_name file
          right_pars[ptr+page_start] = st.session_state.right_text
          with open(right_name, "w", encoding="utf-8") as f:
              f.write("\n\n".join(right_pars))
          st.rerun()     