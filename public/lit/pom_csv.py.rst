=======
POM CSV
=======

Export the dependencies from the POM file to a CSV file.

Open a Streamlit window that contains a text area where you can paste the contents of the `pom.xml` file.

After pasting, you can click the **"Parse"** button to process the data, and then click the **"Save CSV"** button to download the CSV file.

::

  import streamlit as st
  import xmltodict
  import pandas as pd

Print banner.

::

  @st.cache_data
  def print_banner():
      print("""
       _______  _______  __   __         _______  _______  __   __ 
      |       ||       ||  |_|  |       |       ||       ||  | |  |
      |    _  ||   _   ||       | ____  |       ||  _____||  |_|  |
      |   |_| ||  | |  ||       ||____| |       || |_____ |       |
      |    ___||  |_|  ||       |       |      _||_____  ||       |
      |   |    |       || ||_|| |       |     |_  _____| | |     | 
      |___|    |_______||_|   |_|       |_______||_______|  |___|  
      """)
      return 1

  print_banner()

  pom_text = st.text_area("POM")

Parse dependencies in "pom.xml" and store them to dataframe.

Dataframe is stored in ``session_state``.

::
    
  if st.button("Parse"):
      tree = xmltodict.parse(pom_text)
      dependencies = tree['project']['dependencies']['dependency']

      st.session_state.df = pd.DataFrame(dependencies)
  
      st.write(f"### `{len(dependencies)}` dependencies")
      st.table(st.session_state.df)

Save dataframe to csv file.

::
    
  if "df" in st.session_state and st.button("Save CSV"):
      csv_name = 'pom.csv'
      st.session_state.df.to_csv(csv_name, index=False)
      st.write(f"`{csv_name}` created")    