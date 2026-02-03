Grafana Panels
==============

Extract the list of panel titles from a Grafana dashboard JSON. 
Each panel title is located at ``spec.elements.panel-N.spec.title``, 
where ``panel-N`` uses a numeric suffix 
(for example, ``panel-1`` or ``panel-3``).

::

  import json
  import re
  from typing import Dict, List, Optional
  import sys

Command-line argument: path to Grafana dashboard JSON file

::

  if len(sys.argv) != 2:
      print("Usage: python grafana_panels.py <dashboard_json_file>")
      sys.exit(1)

  grafana_json_path = sys.argv[1]


The OutputFile class opens a file whose name is provided to its constructor. 
Its ``print`` method behaves like the built-in ``print`` but also writes the output to that file. 
The class includes a ``close`` method that closes the file.

::

  class OutputFile:
      def __init__(self, filename: str):
          self.file = open(filename, "w", encoding="utf-8")
  
      def print(self, *args, **kwargs):
          # Print to stdout
          print(*args, **kwargs)
          # Print to file
          print(*args, **kwargs, file=self.file)
  
      def close(self):
          self.file.close()
        
  out = OutputFile(grafana_json_path + ".md")

Extracts panel titles located at ``spec -> elements -> "panel-N" -> spec -> title``.

::

  def process_spec(spec: Dict):
      title: Optional[str] = spec.get("title")
      if not isinstance(title, str):
          return
    
      if len(title) == 0:
          title = "."
      out.print(f"### {title}\n")
      data = spec.get("data", {})
      data_spec = data.get("spec", {})
      queries = data_spec.get("queries", [])
      for q in queries:
          query = q.get("spec", {}).get("query", {})
          expr = query.get("spec", {}).get("expr")
          if expr != None:
              out.print(f"```\n{expr}\n```\n")
               
  def process_json(dashboard: Dict):
      elements = dashboard.get("spec", {}).get("elements", {})
      if not isinstance(elements, dict):
          return 

      for key, panel_obj in elements.items():
          if re.match(r"^panel-\d+$", key) and isinstance(panel_obj, dict):
              process_spec(panel_obj.get("spec", {}))
    
Load a dashboard JSON file and print the titles

::

  with open(grafana_json_path, "r", encoding="utf-8") as f:
      dashboard_json = json.load(f)

  titles = process_json(dashboard_json)

  out.close()
  print("----------------------------")
