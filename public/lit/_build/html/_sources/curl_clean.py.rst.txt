curl clean
==========

Clean up curl command by removing unnecessary headers while keeping only the essential ones 
(``Content-Type``, ``Origin``, and ``Referer``).

::

  import streamlit as st
  import pyperclip
  import json
  st.set_page_config(
      page_title="Curl-Clean"
  )

  @st.cache_data
  def print_banner():
      print("""
                    _        _                                    
        __ _  _ _ _| |___ __| |___ __ _ _ _                       
       / _| || | '_| |___/ _| / -_) _` | ' \\                      
       \\__|\\_,_|_| |_|   \\__|_\\___\\__,_|_||_|                                                                     
      """)
      return 1

  print_banner()

Process Curl command

::

  def process_curl_command(text):
      # Split into lines
      lines = text.split('\n')
  
      # Keep only essential headers
      result = []
      in_headers = False
      found_data_raw = False
  
      for line in lines:
          line = line.strip()
      
          # Skip empty lines
          if not line:
              continue
      
          # Keep the curl command line
          if line.startswith('curl'):
              result.append(line + ' \\')
              in_headers = True
              continue
      
          # Keep only essential headers
          if in_headers and line.startswith('-H'):
              if any(header in line for header in ['Content-Type:', 'Origin:', 'Referer:']):
                  result.append('  ' + line + ' \\')
      
          # Keep the data-raw section
          if line.startswith('--data-raw'):
              found_data_raw = True
              result.append('  ' + line)
              break
  
      # If we found data-raw, extract and append the data separately
      data_raw_content = None
      if found_data_raw:
          data_raw_index = text.find('--data-raw')
          if data_raw_index != -1:
              data_raw_content = text[data_raw_index:]
  
      return '\n'.join(result), data_raw_content

Get clipboard content

::
    
  text = pyperclip.paste()

Create Streamlit UI

::

  st.title('Curl-Clean')
  st.write('This tool cleans up curl commands by keeping only essential headers (`Content-Type`, `Origin`, and `Referer`) and the `data-raw` section.')

Input text area

::

  input_text = st.text_area("Input curl command", value=text, height=200)

Process button

::

  if st.button('Clean Curl Command'):
      if input_text:
          cleaned_command, data_raw_content = process_curl_command(input_text)
          st.text_area("Cleaned curl command", value=cleaned_command, height=200)
      
          # Add copy button
          if st.button('Copy to Clipboard'):
              pyperclip.copy(cleaned_command)
              st.success('Copied to clipboard!')

          if data_raw_content:
              # Extract JSON from data-raw content by finding content between single quotes
              json_start = data_raw_content.find("'") + 1
              json_end = data_raw_content.rfind("'")
              json_content = data_raw_content[json_start:json_end]
              json_data = json.loads(json_content)
              st.write("JSON Data:")
              st.write(json_data)
      
      else:
          st.warning('Please paste a curl command first.')