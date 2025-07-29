YouTube Transcript
==================

.. contents::

.. csv-table:: API Links
    :header: "Name", "URL"
    :widths: 10 30
  
    "YouTube Transcript API", https://pypi.org/project/youtube-transcript-api/


::

  import streamlit as st
  import os
  from typing import Optional, Dict, Any

  from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
  from openai import OpenAI

Prints a stylized banner to the console when the application starts.

::

  st.set_page_config(
      page_title="You-T"
  )

  @st.cache_data
  def print_banner():
      print("""
               )                                                      
            ( /(                  *   )                               
            )\\())       (       ` )  /(                               
           ((_)\\  (    ))\\  ___  ( )(_))                              
          __ ((_) )\\  /((_)|___|(_(_())                               
          \\ \\ / /((_)(_))(      |_   _|                               
           \\ V // _ \\| || |       | |                                 
            |_| \\___/ \\_,_|       |_|                                 
          """)
      return 1

  print_banner()

Get transcript from YouTube URL
-------------------------------

::

  youtube_url = st.text_input("YouTube URL")

Extract video_id

::

  video_id = None
  if len(youtube_url) > 0:
      video_id = youtube_url.split("v=")[-1].split("&")[0]

  show_timecodes = True

Initialize YouTubeTranscriptApi

::

  ytt_api = YouTubeTranscriptApi()

If `transcript_file` exists, output the contents

::

  def write_transcript():
      if os.path.exists(transcript_file):
          with open(transcript_file, 'r', encoding='utf-8') as file:
              existing_transcript = file.read()
          st.write(existing_transcript)

Fetch languages

::

  lang = None

  if "transcript_list" not in st.session_state and video_id is not None:
      with st.spinner("Fetching languages...", show_time=True):
          st.session_state.transcript_list = ytt_api.list(video_id)

  if "transcript_list" in st.session_state:
      language_codes = [lang.language_code for lang in st.session_state.transcript_list]
      lang = st.sidebar.radio("Language", language_codes)
  
Output file

::

  transcript_file = st.sidebar.text_input("Output file:", value="transcript.md")
  
  def disabled_save_transcript():
      return lang is None
      #return len(youtube_url)==0
          
Save Transcript

::
    
  if st.button("Save Transcript", type="primary", use_container_width=True, disabled=disabled_save_transcript()):

      with st.spinner("Fetching transcript...", show_time=True):
          st.session_state.transcript_list = ytt_api.list(video_id)
          st.sidebar.write(st.session_state.transcript_list)
      
          fetched_transcript = ytt_api.fetch(video_id, languages=[lang])  
    
      # collect all `snippet.text` into `transcript` variable
      transcript = ""
      if show_timecodes:
          for snippet in fetched_transcript:
              # translate seconds into "HH:MM:SS" format
              m, s = divmod(int(snippet.start), 60)
              #h, m = divmod(m, 60)
              #timestamp = f"{h:02d}:{m:02d}:{s:02d}"
              timestamp = f"{m:02d}:{s:02d}"
              transcript += f"`{timestamp}` {snippet.text}  \n"        
      else:
          for snippet in fetched_transcript:
              transcript += snippet.text + " "
          transcript = transcript.strip()
    
      with open(transcript_file, 'w', encoding='utf-8') as file:
          file.write(transcript)

      st.write(f"Transcript saved: `{transcript_file}`")  
      st.rerun() 
  
  write_transcript()

Get trunscript summary
----------------------

::

  prompt_summary = """
  Тебе будет передана расшифровка видео.
  Твоя задача: подготовить ёмкое резюме.
  """

  llm_prices = {
      "gemini-2.5-flash-preview-05-20": 0.0,
      "gemini-2.0-flash": 0.0,
      "gemma-3-27b-it": 0.0,
      "gpt-4.1-mini": 0.4,
      "gpt-4.1-nano": 0.1,
      "gpt-4.1": 2.0,
      "gpt-4o-mini": 0.15,
      "o4-mini": 1.10,
      "o3-mini": 1.10,
      "gpt-4o": 2.5,
      "o1": 15.0,
  }
  llm_models = list(llm_prices.keys())

        
Class MultiModel
****************

Wrapper for multiple LLM APIs (OpenAI, Gemini, Gemma).

::

  class MultiModel:
      def __init__(self, llm_model: str, llm_temperature = 0.1) -> None:
          self.llm_model = llm_model
          self.llm_temperature = llm_temperature

          vendor = self._get_vendor(llm_model)
          if vendor == "google":
              self.client = OpenAI(
                  api_key=os.getenv("GEMINI_API_KEY"),
                  base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
              )
          else:
              self.client = OpenAI()

Determines the vendor based on the model name.

::

      @staticmethod
      def _get_vendor(llm_model: str) -> str:
          if llm_model.lower().startswith(("gemini", "gemma")):
              return "google"
          return "openai"

Calls a GPT-like model with standard message format and temperature.

::

      def _call_gpt(self, prompt: str, text: str):
          messages = [
              {"role": "system", "content": prompt},
              {"role": "user", "content": text},
          ]
          response = self.client.chat.completions.create(
              model=self.llm_model,
              messages=messages,
              temperature=self.llm_temperature,
          )
          return response.choices[0]

Calls a Gemma model with custom message format and temperature.

::

      def _call_gemma(self, prompt: str, text: str):
          messages = [
              {"role": "user", "content": f"<instructions>{prompt}</instructions>\n<user_input>{text}</user_input>"},
          ]
          response = self.client.chat.completions.create(
              model=self.llm_model,
              messages=messages,
              temperature=self.llm_temperature,
          )
          return response.choices[0]

Calls an 'o'-prefixed model with standard message format, no temperature.

::

      def _call_o_model(self, prompt: str, text: str):
          messages = [
              {"role": "system", "content": prompt},
              {"role": "user", "content": text},
          ]
          response = self.client.chat.completions.create(
              model=self.llm_model,
              messages=messages,
          )
          return response.choices[0]

Calls the appropriate LLM based on the model name.

::

      def call_llm(self, prompt: str, text: str):
          model = self.llm_model.lower()
          if model.startswith(("gemini", "gpt")):
              return self._call_gpt(prompt, text)
          elif model.startswith("gemma"):
              return self._call_gemma(prompt, text)
          elif model.startswith("o"):
              return self._call_o_model(prompt, text)
          else:
              raise ValueError(f"Unknown model prefix for: {self.llm_model}")
        
Select LLM
**********

::

  llm_model = st.sidebar.selectbox("LLM Model", llm_models)

  def create_summary():
      with open(transcript_file, 'r', encoding='utf-8') as file:
          transcript = file.read()

      llm = MultiModel(llm_model) 
      summary = llm.call_llm(prompt_summary, transcript)

      return summary.message.content

Summary button

::

  if st.sidebar.button("Summary", use_container_width=True):
      st.session_state.summary = create_summary()

  if "summary" in st.session_state:
      st.write("### Summary")
      st.write(st.session_state.get("summary"))
  
Truncate text to max len

::

  def max_len(text, k):
      if len(text) <= k:
          return text
      return text[:k] + '...'    