YouTube Transcript
==================

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

Get transcript from YouTube URL

::

  youtube_url = st.text_input("YouTube URL")
  lang = st.radio("Language", ["ru","en"], horizontal=True)

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
      "gemini-2.0-flash": 0.0,
      "gemini-2.5-pro-exp-03-25": 0.0,
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

GenericLLM
----------

::

  class GenericLLM:

      def __init__(self, llm_model: str) -> None:
          self.llm_model = llm_model

          self.client = OpenAI()
          self.llm_temperature = 0.1

          self.g_key = os.getenv("GEMINI_API_KEY")
          self.g_client = OpenAI(
              api_key=self.g_key,
              base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
          )

      def _call_o_model(self, prompt, text):
          messages = [
              {"role": "developer", "content": prompt},
              {"role": "user", "content": text},
          ]
          response = self.client.chat.completions.create(
              model=self.llm_model,
              messages=messages,
          )
          return response.choices[0]

      def _call_gpt(self, prompt, text):
          messages = [
              {"role": "developer", "content": prompt},
              {"role": "user", "content": text},
          ]
          response = self.client.chat.completions.create(
                  model=self.llm_model,
                  messages=messages,
                  temperature=self.llm_temperature,
              )
          return response.choices[0]

      def _call_gemini(self, prompt, text):
          messages = [
              {"role": "developer", "content": prompt},
              {"role": "user", "content": text},
          ]
          response = self.g_client.chat.completions.create(
                  model=self.llm_model,
                  messages=messages,
                  temperature=self.llm_temperature,
              )
          return response.choices[0]

      def _call_gemma(self, prompt, text):
          messages = [
              {"role": "user", "content": f"<instructions>{prompt}</instructions>\n<user_input>{text}</user_input>"},
              {"role": "user", "content": text},
          ]
          response = self.g_client.chat.completions.create(
                  model=self.llm_model,
                  messages=messages,
                  temperature=self.llm_temperature,
              )
          return response.choices[0]

      def call_llm(self, prompt, text):

          if self.llm_model.startswith("gemini"):
              response = self._call_gemini(prompt, text)

          elif self.llm_model.startswith("gemma"):
              response = self._call_gemma(prompt, text)

          elif self.llm_model.startswith("gpt"):
              response = self._call_gpt(prompt, text)

          elif self._llm_model.startswith("o"):
              response = self._call_o_model(prompt, text)

          else:
              response = None

          return response

Select LLM

::

  llm_model = st.selectbox("LLM Model", llm_models)

  def create_summary():
      with open(transcript_file, 'r', encoding='utf-8') as file:
          transcript = file.read()

      llm = GenericLLM(llm_model) 
      summary = llm.call_llm(prompt_summary, transcript)

      return summary.message.content

Summary button

::

  if st.button("Summary", use_container_width=True):
      st.session_state.summary = create_summary()

  st.write(st.session_state.get("summary"))