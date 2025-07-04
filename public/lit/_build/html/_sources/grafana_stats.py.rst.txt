Grafana Stats
-------------

Process CSV file exported from Grafana

::

  import os
  import streamlit as st
  import pandas as pd
  import json
  import datetime

  st.set_page_config(
      page_title="Grafana-Stats"
  )


  csv_files = [f for f in os.listdir('.') if f.endswith('.csv') and not f.startswith("log-")]
  csv_file = st.sidebar.radio("Select CSV file to process:", csv_files)

  df = pd.read_csv(csv_file)
  df.drop(columns=["tsNs", "id", "traceID", "exporter", "instance", "service_name"], inplace=True)

  if st.sidebar.toggle("Show details"):

      num_rows = df.shape[0]
      st.sidebar.write(f"Rows: `{num_rows}`")
    
      num = st.number_input("Row", min_value=0, max_value=num_rows-1)
      series = df.iloc[num]


Parse body

::

      data = json.loads(series["Line"])
      series["Line"] = data["body"]
    
      timestamp_s = series["Time"] / 1000.0  # Convert milliseconds to seconds
      series["Time"] = datetime.datetime.fromtimestamp(timestamp_s)
    
      st.table(series)

  # Function to extract "body" from JSON string
  def extract_body(json_str):
      try:
          parsed = json.loads(json_str)
          return parsed.get("body", None) #,parsed.get("instrumentation_scope", None)
      except json.JSONDecodeError:
          return None
        
  log_file = "log-" + csv_file
    
  if st.sidebar.button("Export log"):
      df_log = df[[
          'Date',
          'Line',
      ]].copy()
      df_log['Line'] = df_log['Line'].apply(extract_body)
      df_log.to_csv(log_file, index=False)
      st.sidebar.write(f"Exported log: `{log_file}`")

  if st.sidebar.toggle("Show counts"):
      df_log = pd.read_csv(log_file)
    
      # Count distinct messages
      count_df = df_log.groupby("Line").size().reset_index(name="Count")
    
      # Reorder columns to have Count first
      count_df = count_df[["Count", "Line"]].sort_values(by='Count', ascending=False)
    
      st.table(count_df)