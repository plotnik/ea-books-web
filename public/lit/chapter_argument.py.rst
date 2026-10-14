Chapter Argument
================

For Pratchett-like material, this prompt aims for an old-fashioned, mock-solemn chapter argument 
rather than asking the model to imitate Pratchett’s prose style. 
That contrast—grand bibliographical dignity applied to absurd events—is exactly what makes the device work.

::

  import streamlit as st
  import os
  from dataclasses import dataclass

Page banner

::

  st.set_page_config(
      page_title="Chapter Argument",
  )

  @st.cache_data
  def print_banner():
      print("### Chapter Argument")
      return 1

  print_banner()
  st.write("### Chapter Argument")

----

.. |moneybag| unicode:: 0x1F4B0

|moneybag| **OpenAI Model Pricing** 
   https://platform.openai.com/docs/pricing#latest-models

|moneybag| **Gemini Model Pricing** 
   https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing

----

Select LLM.

Prices are USD per 1 million input/output tokens.

::

  llm_prices = {
      "gemini-3.8-flash": (0.75, 3.75),
      "gpt-6-luna": (0.10, 0.50),
      "gpt-6.1-sol": (2.00, 10.00),
      # "gpt-5.6-sol": (5.00, 30.00),
      # "gpt-6-astra": (10.00, 50.00),
  }

  llm_models = list(llm_prices.keys())

  llm_model =  st.radio("Model", llm_models, horizontal=True, label_visibility="collapsed")
  # model_name = st.radio("Model", ["luna", "terra"], horizontal=True, label_visibility="collapsed")
  # llm_model = llm_models[2 if model_name == "terra" else 1]

  st.write(f"`{llm_model}`")

EN prompt

::

  chapter_argument_prompt = """
  You are given the full text of a chapter from a comic fantasy novel.

  Write a **traditional descriptive chapter argument** for the chapter: 
  an old-fashioned miniature synopsis of the kind historically printed 
  beneath or in place of a chapter title.

  The argument must begin:

  **“In which…”**

  ### Style

  Write as though an excessively dignified old editor is cataloguing 
  the contents of the chapter for the reader.

  The tone should be:
  - formal, dry, concise, and mock-solemn;
  - slightly archaic, but immediately readable;
  - amused without explaining the joke;
  - disproportionately serious about trivial, ridiculous, or mundane events.

  The humour should arise primarily from **contrast**: treat a minor inconvenience, 
  foolish remark, unfortunate meal, bureaucratic procedure, peculiar object, 
  or embarrassing misunderstanding with the same narrative importance as a murder, 
  magical catastrophe, political crisis, or threat to civilization.

  Prefer understatement to punchlines.

  Do **not** imitate the prose style or characteristic phrasing of the novel's author. 
  The voice should instead resemble an old-fashioned eighteenth- or nineteenth-century 
  chapter heading applied to comic fantasy.

  ### Content

  Identify roughly **3–6 of the chapter's most characteristic events, discoveries, reversals, conversations, or absurdities**.

  Do not merely summarize the plot. Select details that make an amusing sequence when juxtaposed.

  Whenever possible:
  - begin with something apparently important;
  - include at least one wonderfully trivial or mundane detail;
  - mention a character by name where useful;
  - hint at consequences rather than explaining them;
  - preserve surprises that the argument does not need to reveal;
  - finish on an intriguing, ominous, or absurdly understated note.

  ### Form

  Produce **one sentence only**.

  Begin with **“In which…”**

  Separate the miniature topics with semicolons, commas, or constructions such as **“and in which…”**.

  Aim for **35–70 words**.

  Do not add a title, explanation, quotation marks, bullet points, or commentary.

  ### Examples of the desired mechanism

  “In which a matter of considerable importance is entrusted to entirely the wrong person; 
  a wizard discovers that theoretical knowledge has certain practical disadvantages; 
  supper is delayed by circumstances beyond supper’s control; 
  and a perfectly ordinary door proves regrettably less ordinary upon inspection.”

  “In which the Watch investigates a disturbance; several citizens demonstrate 
  the flexible nature of the word ‘innocent’; a question of municipal procedure 
  assumes unexpected urgency; and a cheese becomes relevant.”

  These examples demonstrate the **form and comic mechanism only**. 
  Do not reuse their wording or events.
  """

RU prompt

::

  chapter_argument_prompt_ru = """
  Вам дан полный текст главы из юмористического фэнтезийного романа.

  Напишите для этой главы **традиционное описательное краткое содержание** — 
  старомодную миниатюрную аннотацию в духе тех, что исторически печатались 
  под заголовком главы или вместо него.

  Текст должен начинаться словами:

  **«В которой…»**

  ### Стиль

  Пишите так, словно чрезмерно степенный старинный редактор обстоятельно 
  перечисляет читателю содержание главы.

  Тон должен быть:
  - формальным, сухим, лаконичным и шутливо-торжественным;
  - слегка архаичным, но сразу понятным современному читателю;
  - насмешливым, но без объяснения шуток;
  - несоразмерно серьёзным по отношению к пустяковым, нелепым или обыденным событиям.

  Юмор должен возникать прежде всего из **контраста**: мелкое неудобство, глупое замечание, 
  неудачную трапезу, бюрократическую процедуру, странный предмет или неловкое недоразумение 
  следует описывать с той же повествовательной значительностью, что и 
  убийство, магическую катастрофу, политический кризис или угрозу цивилизации.

  Предпочитайте сдержанность явным остротам и панчлайнам.

  **Не** подражайте стилю прозы или характерным оборотам автора романа. Голос должен 
  скорее напоминать старомодный заголовок главы XVIII или XIX века, 
  применённый к юмористическому фэнтези.

  ### Содержание

  Выберите примерно **3–6 наиболее характерных событий, открытий, поворотов, разговоров или нелепостей главы**.

  Не пересказывайте сюжет целиком. Отбирайте такие детали, которые при сопоставлении 
  образуют забавную последовательность.

  По возможности:
  - начинайте с чего-либо, кажущегося важным;
  - включайте хотя бы одну восхитительно мелкую или бытовую подробность;
  - при необходимости называйте персонажа по имени;
  - намекайте на последствия, а не объясняйте их;
  - сохраняйте те сюрпризы, раскрывать которые для этой аннотации необязательно;
  - заканчивайте интригующей, зловещей или нелепо сдержанной нотой.

  ### Форма

  Напишите **ровно одно предложение**.

  Начните со слов **«В которой…»**

  Разделяйте миниатюрные темы точками с запятой, запятыми или конструкциями вроде **«и в которой…»**.

  Ориентируйтесь на объём **35–70 слов**.

  Не добавляйте заголовок, пояснения, кавычки, маркированные списки или комментарии.

  ### Примеры требуемого приёма

  «В которой дело чрезвычайной важности доверяется совершенно неподходящему человеку; 
  волшебник обнаруживает, что теоретические познания имеют некоторые практические недостатки; 
  ужин задерживается по обстоятельствам, от ужина не зависящим; а самая обыкновенная дверь 
  при ближайшем рассмотрении оказывается прискорбно менее обыкновенной».

  «В которой Стража расследует происшествие; несколько горожан демонстрируют весьма гибкое 
  понимание слова „невиновен“; вопрос муниципальной процедуры неожиданно приобретает неотложность; 
  а сыр оказывается небезразличен к происходящему».

  Эти примеры демонстрируют **только форму и комический механизм**. 
  Не повторяйте их формулировки или события.
  """

  #ru = st.toggle("en : ru")
  lang = st.radio("Language", ["en", "ru"], horizontal=True, label_visibility="collapsed")

  prompt = chapter_argument_prompt_ru if lang == "ru" else chapter_argument_prompt


Find Obsidian folder

::

  def find_obsidian_folder():
      current_folder = os.getcwd()
      home_folders = os.listdir(current_folder)
      book_folders = [item for item in home_folders if os.path.isdir(os.path.join(current_folder, item)) and item.endswith(" Book")]

      if (len(book_folders)==0):
          raise ValueError('The folder should contain a subfolder with a name that ends with " Book".')

      return book_folders[0]  

Process the supplied text with OpenAI or Gemini client.   

There should be ``OPENAI_API_KEY`` and ``GEMINI_API_KEY`` environment variables defined.

::

  @dataclass(frozen=True)
  class LLMResult:
      text: str
      input_tokens: int
      output_tokens: int

.. function:: count_tokens(value: str) -> int

::

  def count_tokens(value: str) -> int:
      import tiktoken

      try:
          encoding = tiktoken.encoding_for_model(llm_model)
      except KeyError:
          # Use the current general-purpose OpenAI encoding for new or non-OpenAI
          # model names. For Gemini this count is an estimate only.
          encoding = tiktoken.get_encoding("o200k_base")
      return len(encoding.encode(value))


.. function:: process_with_openai(text: str, prompt: str) -> LLMResult

::

  def process_with_openai(text: str, prompt: str) -> LLMResult:
      from openai import OpenAI

      client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
      response = client.responses.create(
          model=llm_model,
          instructions=prompt.strip(),
          input=text,
      )
      return LLMResult(
          text=response.output_text,
          input_tokens=response.usage.input_tokens,
          output_tokens=response.usage.output_tokens,
      )


.. function:: process_with_gemini(text: str, prompt: str) -> LLMResult

::

  def process_with_gemini(text: str, prompt: str) -> LLMResult:
      from google import genai
      from google.genai import types

      client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
      response = client.models.generate_content(
          model=llm_model,
          contents=text,
          config=types.GenerateContentConfig(system_instruction=prompt.strip()),
      )
      usage = response.usage_metadata
      # Gemini bills response and reasoning tokens at the output-token rate.
      output_tokens = (usage.candidates_token_count or 0) + (
          usage.thoughts_token_count or 0
      )
      return LLMResult(
          text=response.text or "",
          input_tokens=usage.prompt_token_count or 0,
          output_tokens=output_tokens,
      )


.. function:: process_text(text: str, prompt: str) -> LLMResult

::

  def process_text(text: str, prompt: str) -> LLMResult:
      if llm_model.startswith("gpt-"):
          return process_with_openai(text, prompt)
      if llm_model.startswith("gemini-"):
          return process_with_gemini(text, prompt)
      raise ValueError(f"Unsupported model: {llm_model}")


.. function:: calculate_cost(result: LLMResult) -> float

::

  def calculate_cost(result: LLMResult) -> float:
      input_price, output_price = llm_prices[llm_model]
      return (
          result.input_tokens * input_price + result.output_tokens * output_price
      ) / 1_000_000


.. function:: get_newest_files(directory, num_files)

   Get ``num_files`` newest files from the provided directory.

::

  def get_newest_files(directory, num_files):
      # Check if the directory exists
      if not os.path.isdir(directory):
          raise ValueError(f"The directory {directory} does not exist.")

      # Get a list of files in the directory with their full paths and modification times
      files_with_paths = []
      for file_name in os.listdir(directory):
          file_path = os.path.join(directory, file_name)
          if os.path.isfile(file_path) and file_path.endswith(".md"):
              files_with_paths.append((file_path, os.path.getmtime(file_path)))

      # Sort files by modification time in descending order (newest first)
      sorted_files = sorted(files_with_paths, key=lambda x: x[1], reverse=True)

      # Extract the num_files newest file names
      newest_files = [os.path.basename(file_with_path[0]) for file_with_path in sorted_files[:num_files]]

      return newest_files

Select ``note_name`` from 5 newest notes.

::

  note_home = find_obsidian_folder()

  newest_files = get_newest_files(note_home, 5)
  note_name = st.selectbox(
     "Note",
     newest_files,
  )

Load Obsidian note

::

  file_path = os.path.join(note_home, note_name)
  with open(file_path, 'r', encoding='utf-8') as file:
      text = file.read()

Write truncated input text in container

::

  c_input = st.container(border=True)

  def max_len(text, k):
      if len(text) <= k:
          return text
      return text[:k] + '...'

  c_input.write(f"""

  {max_len(text, 250)}

  """)

  st.write(f"Prompt: `{count_tokens(prompt)}` tokens, Text: `{count_tokens(text)}` tokens")

Process button

::

  if st.button("Process"):
      if not text.strip():
          st.warning("Enter some text to process.")
      else:
          try:
              with st.spinner("Processing..."):
                  result = process_text(text, prompt)
              st.write(result.text)
              st.write(
                  f"Cost: ${calculate_cost(result):.8f} "
                  f"({result.input_tokens:,} input tokens, "
                  f"{result.output_tokens:,} output tokens)"
              )
          except KeyError as error:
              st.error(f"Missing environment variable: {error.args[0]}")
          except Exception as error:
              st.error(f"Processing failed: {error}")
