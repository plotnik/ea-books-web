YouTube Transcript
==================

.. contents::

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

::

  youtube_url = st.text_input("YouTube URL")
  lang = st.radio("Language", ["ru","en","by"], horizontal=True)

  transcript_file = "transcript.txt"

  def transcript_as_text(url: str, lang: str = 'en') -> str:
      """
      Returns one plain‑text string containing the caption lines.
      Falls back to auto‑generated captions if no manual track exists.
      """
      video_id = url.split("v=")[-1].split("&")[0]

      try:
          # This tries manual captions first, then auto‑generated.
          transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[lang])
          return " ".join(chunk['text'] for chunk in transcript)
      except TranscriptsDisabled:
          return "[Captions are disabled on this video.]"
      except NoTranscriptFound:
          return "[No transcript available in the requested language.]"
  
  # Truncate text to max len
  def max_len(text, k):
      if len(text) <= k:
          return text
      return text[:k] + '...'
  
  if st.button("Save Transcript", use_container_width=True):
      transcript = transcript_as_text(youtube_url, lang)    
      st.text_area("Transcript", transcript, height=300)

      with open(transcript_file, 'w', encoding='utf-8') as file:
          file.write(transcript)

      st.write(f"Transcript saved: `{transcript_file}`")  

Get trunscript summary

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

            
MultiModel
----------

::

  class MultiModel:
      """
      Wrapper for multiple LLM APIs (OpenAI, Gemini, Gemma).
      """

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

      @staticmethod
      def _get_vendor(llm_model: str) -> str:
          """
          Determines the vendor based on the model name.
          """
          if llm_model.lower().startswith(("gemini", "gemma")):
              return "google"
          return "openai"

      def _call_gpt(self, prompt: str, text: str):
          """
          Calls a GPT-like model with standard message format and temperature.
          """
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

      def _call_gemma(self, prompt: str, text: str):
          """
          Calls a Gemma model with custom message format and temperature.
          """
          messages = [
              {"role": "user", "content": f"<instructions>{prompt}</instructions>\n<user_input>{text}</user_input>"},
          ]
          response = self.client.chat.completions.create(
              model=self.llm_model,
              messages=messages,
              temperature=self.llm_temperature,
          )
          return response.choices[0]

      def _call_o_model(self, prompt: str, text: str):
          """
          Calls an 'o'-prefixed model with standard message format, no temperature.
          """
          messages = [
              {"role": "system", "content": prompt},
              {"role": "user", "content": text},
          ]
          response = self.client.chat.completions.create(
              model=self.llm_model,
              messages=messages,
          )
          return response.choices[0]

      def call_llm(self, prompt: str, text: str):
          """
          Calls the appropriate LLM based on the model name.
          """
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

::

  llm_model = st.selectbox("LLM Model", llm_models)

  def create_summary():
      with open(transcript_file, 'r', encoding='utf-8') as file:
          transcript = file.read()

      llm = MultiModel(llm_model) 
      summary = llm.call_llm(prompt_summary, transcript)

      return summary.message.content

Summary button

::

  if st.button("Summary", use_container_width=True):
      st.session_state.summary = create_summary()

  st.write(st.session_state.get("summary"))