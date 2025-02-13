# Google Search
# -------------
#
# ::

import streamlit as st
import requests
import yaml
from urllib.parse import urlencode

phrase = st.text_input("Phrase", placeholder="radio")
google = "https://www.google.com/search"

site = "https://docs.streamlit.io/"
params = {
    "q": f"{phrase} site:{site}"  
}
  
st.write(f"{google}?{urlencode(params)}")

if st.button("Find"):
    response = requests.get(google, params=params)
    st.write(response.url)
