Compare JSON
============

Comparing two JSON documents side by side.

The app presents two text areas arranged in left and right columns. A user can paste a JSON string into each text area and click a ``Compare`` button. The script then attempts to parse, normalize, and pretty-format both JSON values, updates the displayed text areas with the formatted JSON, and reports whether the two JSON documents are equivalent.

::

  import json
  from typing import Any

  import streamlit as st


  MAX_DIFFS = 200


.. function:: load_json(raw_text: str) -> tuple[Any | None, str | None]

::

  def load_json(raw_text: str) -> tuple[Any | None, str | None]:
      if not raw_text.strip():
          return None, "JSON input is empty."

      try:
          return json.loads(raw_text), None
      except json.JSONDecodeError as exc:
          return None, f"Invalid JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"


.. function:: format_json(value: Any) -> str

::

  def format_json(value: Any) -> str:
      return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)


.. function:: preview_value(value: Any) -> str

::

  def preview_value(value: Any) -> str:
      rendered = json.dumps(value, sort_keys=True, ensure_ascii=False)
      return rendered if len(rendered) <= 140 else f"{rendered[:137]}..."


.. function:: path_join(path: str, part: str) -> str

::

  def path_join(path: str, part: str) -> str:
      return f"{path}.{part}" if path else part


.. function:: compare_json(left: Any, right: Any, path: str = "$") -> list[str]

::

  def compare_json(left: Any, right: Any, path: str = "$") -> list[str]:
      diffs: list[str] = []

      def add(message: str) -> bool:
          diffs.append(message)
          return len(diffs) >= MAX_DIFFS

      def walk(left_value: Any, right_value: Any, current_path: str) -> bool:
          if type(left_value) is not type(right_value):
              return add(
                  f"{current_path}: type differs "
                  f"({type(left_value).__name__} != {type(right_value).__name__})"
              )

          if isinstance(left_value, dict):
              left_keys = set(left_value)
              right_keys = set(right_value)

              for key in sorted(left_keys - right_keys):
                  if add(f"{path_join(current_path, key)}: only in left"):
                      return True

              for key in sorted(right_keys - left_keys):
                  if add(f"{path_join(current_path, key)}: only in right"):
                      return True

              for key in sorted(left_keys & right_keys):
                  if walk(left_value[key], right_value[key], path_join(current_path, key)):
                      return True

              return False

          if isinstance(left_value, list):
              common_length = min(len(left_value), len(right_value))

              for index in range(common_length):
                  if walk(left_value[index], right_value[index], f"{current_path}[{index}]"):
                      return True

              if len(left_value) > len(right_value):
                  for index in range(common_length, len(left_value)):
                      if add(f"{current_path}[{index}]: only in left"):
                          return True

              if len(right_value) > len(left_value):
                  for index in range(common_length, len(right_value)):
                      if add(f"{current_path}[{index}]: only in right"):
                          return True

              return False

          if left_value != right_value:
              return add(
                  f"{current_path}: value differs "
                  f"({preview_value(left_value)} != {preview_value(right_value)})"
              )

          return False

      walk(left, right, path)
      return diffs


.. function:: compare_inputs() -> None

::

  def compare_inputs() -> None:
      left_json, left_error = load_json(st.session_state.left_json)
      right_json, right_error = load_json(st.session_state.right_json)

      st.session_state.left_error = left_error
      st.session_state.right_error = right_error
      st.session_state.diffs = []
      st.session_state.are_equal = False

      if left_error or right_error:
          return

      st.session_state.left_json = format_json(left_json)
      st.session_state.right_json = format_json(right_json)
      st.session_state.diffs = compare_json(left_json, right_json)
      st.session_state.are_equal = not st.session_state.diffs


  st.set_page_config(page_title="JSON Compare", layout="wide")
  st.title("JSON Compare")

  if "left_json" not in st.session_state:
      st.session_state.left_json = ""
  if "right_json" not in st.session_state:
      st.session_state.right_json = ""
  if "left_error" not in st.session_state:
      st.session_state.left_error = None
  if "right_error" not in st.session_state:
      st.session_state.right_error = None
  if "diffs" not in st.session_state:
      st.session_state.diffs = []
  if "are_equal" not in st.session_state:
      st.session_state.are_equal = False

  left_column, right_column = st.columns(2)

  with left_column:
      st.text_area("Left JSON", key="left_json", height=520)

  with right_column:
      st.text_area("Right JSON", key="right_json", height=520)

  st.button("Compare", type="primary", on_click=compare_inputs)

  if st.session_state.left_error:
      st.error(f"Left JSON: {st.session_state.left_error}")

  if st.session_state.right_error:
      st.error(f"Right JSON: {st.session_state.right_error}")

  if not st.session_state.left_error and not st.session_state.right_error:
      if st.session_state.are_equal:
          st.success("JSON documents are equal after normalization.")
      elif st.session_state.diffs:
          st.warning(f"JSON documents differ. Showing up to {MAX_DIFFS} differences.")
          st.code("\n".join(st.session_state.diffs), language="text")
