Persisted List   
==============    

A tiny helper that remembers a list of strings on disk.

.. admonition:: Example
   :collapsible: closed

   .. code:: python
   
        persisted = PersistedList(".persisted")
        options = [
            "Email", 
            "Home phone", 
            "Mobile phone"
        ]
        ordered = persisted.sort_by_pattern(options)
       
        import streamlit as st
       
        option = st.selectbox(
            "How would you like to be contacted?",
            ordered,
        )
       
        st.write("You selected:", option)   
        persisted.select(option)  

----

::

  from typing import List
  from pathlib import Path
 
  class PersistedList:

.. classmethod:: __init__(filename: str)

    Set ``filename``.

::
    
      def __init__(self, filename: str) -> None:
          self.filename = Path(filename)
          self.group = ""
        
.. classmethod:: sort_by_pattern(all_names: List[str], group: str = "") -> List[str]

    Sort ``all_names`` so that previously‑stored names keep their old
    ordering, and every new name is appended alphabetically.
    The internal list is updated and re‑written to disk.

::
    
      def sort_by_pattern(self, options: List[str], group: str = "") -> List[str]:
          # Read the file on disk to get the current list of names.
          # Persisted names are expected to be in the format "group|name" if group is used, 
          # otherwise just "name".
          self.names: List[str] = self._read_from_file()

          extracted = self._extract_groups(self.names, group)
        
          # Create a priority mapping for persisted names, 
          # like {"A|Home phone": 0, "A|Mobile phone": 1, "A|Email": 2}
          priority = {name: idx for idx, name in enumerate(extracted)}

          # Sort the grouped names based on the priority of persisted names
          prioritized_names = [name for name in options if name in priority]
          missing_names = [name for name in options if name not in priority]

          sorted_names = sorted(prioritized_names, key=priority.get) + missing_names
          return sorted_names

.. classmethod:: select(name: str, group: str = "")

      Move ``name`` to the top of the list (inserting it if it
      wasn’t present) and persist the change.
         
::
    
      def select(self, name: str, group: str = "") -> None:
          selected_name = self._add_group(name, group)
          # if 1st element of `self.names` equals to `selected_name` then return
          if self.names and self.names[0] == selected_name:
              return
          self.names = self._remove_strings(self.names, [selected_name])
          self.names.insert(0, selected_name)
          self._write_to_file()

----

Private helpers

::
    
      def _read_from_file(self) -> List[str]:
          """
          Return the list stored on disk (empty if the file is missing).
          """
          if self.filename.exists():
              with self.filename.open("r", encoding="utf-8") as fh:
                  return [line.strip() for line in fh if line.strip()]
          return []

      def _write_to_file(self) -> None:
          """
          Persist the current list to disk (one item per line).
          """
          intended_content = "\n".join(self.names)

          if self.filename.exists():
              current_content = self.filename.read_text(encoding="utf-8")
              if current_content == intended_content:
                  return

          self.filename.parent.mkdir(parents=True, exist_ok=True)
          with self.filename.open("w", encoding="utf-8") as fh:
              fh.write(intended_content)

      @staticmethod
      def _remove_strings(source: List[str], to_remove: List[str]) -> List[str]:
          """
          Return a copy of *source* without any element that occurs in *to_remove*.
          """
          removal_set = set(to_remove)
          return [s for s in source if s not in removal_set]

      @staticmethod
      def _add_group(name: str, group: str) -> str:
          if not group:
              return name
          if "|" in name:
              return name
          return f"{group}|{name}"

      @staticmethod
      def _extract_groups(sorted_names: List[str], group: str) -> List[str]:
          if group:
              prefix = f"{group}|"
              return [name[len(prefix):] for name in sorted_names if name.startswith(prefix)]
          return [name.split("|", 1)[1] if "|" in name else name for name in sorted_names]

Convenience

::
    
      def __iter__(self):
          return iter(self.names)

      def __repr__(self) -> str:
          return f"{self.__class__.__name__}({self.filename!s}, {self.names})"
        
.. csv-table:: History
   :header: "Date", "Comment"
   :widths: 10 30
   :width: 100%

   "2026-03-20", "Add groups"   
   "2025-11-07", "Read file in ``sort_by_pattern``"   
   "2025-07-30", "Cache in ``select``"
   "2025-06-13", "New elements come first"
   "", "Copied from: ``explain_java.py``_"

.. _explain_java.py: explain_java.py.html#persisted-list
 