# Persisted List   
# ==============    
#
# A tiny helper that remembers a list of strings on disk.
#
# .. admonition:: Example
#    :collapsible: closed
#
#    .. code:: python
#    
#         persisted = PersistedList(".persisted")
#         options = [
#             "Email", 
#             "Home phone", 
#             "Mobile phone"
#         ]
#         ordered = persisted.sort_by_pattern(options)
#        
#         import streamlit as st
#        
#         option = st.selectbox(
#             "How would you like to be contacted?",
#             ordered,
#         )
#        
#         st.write("You selected:", option)   
#         persisted.select(option)  
#
# ----
#
# ::

from typing import List
from pathlib import Path
 
class PersistedList:

# .. classmethod:: __init__(filename: str)
#
#     Set ``filename``.
#
# ::
    
    def __init__(self, filename: str) -> None:
        self.filename = Path(filename)
        
# .. classmethod:: sort_by_pattern(all_names: List[str]) -> List[str]
#
#     Sort ``all_names`` so that previously‑stored names keep their old
#     ordering, and every new name is appended alphabetically.
#     The internal list is updated and re‑written to disk.
#
# ::
    
    def sort_by_pattern(self, all_names: List[str]) -> List[str]:
        self.names: List[str] = self._read_from_file()
        
        priority = {name: idx for idx, name in enumerate(self.names)}

        sorted_names = sorted(
            all_names,
            key=lambda n: (1, priority[n]) if n in priority else (0, n)
        )

        self.names = sorted_names
        self._write_to_file()
        return sorted_names

# .. classmethod:: select(selected_name: str)
#
#       Move ``selected_name`` to the top of the list (inserting it if it
#       wasn’t present) and persist the change.
#          
# ::
    
    def select(self, selected_name: str) -> None:
        # if 1st element of `self.names` equals to `selected_name` then return
        if self.names and self.names[0] == selected_name:
            return
        self.names = self._remove_strings(self.names, [selected_name])
        self.names.insert(0, selected_name)
        self._write_to_file()

# ----
#
# Private helpers
#
# ::
    
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
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        with self.filename.open("w", encoding="utf-8") as fh:
            fh.write("\n".join(self.names))

    @staticmethod
    def _remove_strings(source: List[str], to_remove: List[str]) -> List[str]:
        """
        Return a copy of *source* without any element that occurs in *to_remove*.
        """
        removal_set = set(to_remove)
        return [s for s in source if s not in removal_set]

# Convenience
#
# ::
    
    def __iter__(self):
        return iter(self.names)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.filename!s}, {self.names})"
        
# .. csv-table:: History
#    :header: "Date", "Comment"
#    :widths: 10 30
#    :width: 100%
#
#    "2025-11-07", "Read file in `sort_by_pattern`"   
#    "2025-07-30", "Cache in `select`"
#    "2025-06-13", "New elements come first"
#    "", "Copied from: `explain_java.py`_"
#
# .. _explain_java.py: explain_java.py.html#persisted-list
#  