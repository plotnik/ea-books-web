Grafana Panels
==============

Extract the list of panel titles from a Grafana dashboard JSON. 
Each panel title is located at spec.elements.panel-N.spec.title, where "panel-N" uses a numeric suffix 
(for example, "panel-1" or "panel-3").

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

Extracts panel titles located at spec -> elements -> "panel-N" -> spec -> title.
Returns a list of titles (in no particular order). Skips panels without titles.

::

  def extract_panel_titles(dashboard: Dict) -> List[str]:
      titles: List[str] = []
      elements = dashboard.get("spec", {}).get("elements", {})
      if not isinstance(elements, dict):
          return titles

      for key, panel_obj in elements.items():
          if re.match(r"^panel-\d+$", key) and isinstance(panel_obj, dict):
              title: Optional[str] = panel_obj.get("spec", {}).get("title")
              if isinstance(title, str):
                  titles.append(title)
      return titles

Load a dashboard JSON file and print the titles

::

  if __name__ == "__main__":
      with open(grafana_json_path, "r", encoding="utf-8") as f:
          dashboard_json = json.load(f)

      titles = extract_panel_titles(dashboard_json)
      print("=== Panel titles")
      for t in titles:
          print("1. ", t)

      print("----------------------------")
