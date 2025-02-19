Grafana Stats
-------------

Process CSV file exported from Grafana

::

  import os
  import streamlit as st
  import pandas as pd
  import json
  import datetime


  csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
  csv_file = st.sidebar.radio("Select CSV file to process:", csv_files)
  df = pd.read_csv(csv_file)

  df.drop(columns=["tsNs", "id", "traceID", "exporter", "instance", "service_name"], inplace=True)

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