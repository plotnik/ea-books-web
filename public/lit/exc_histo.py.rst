exc histo
=========

Display histogram from ``yml`` file created by exc_yaml_.

.. _exc_yaml: exc_yaml.py.html

::

  import streamlit as st
  import pandas as pd
  import yaml
  import os

Bin size.

::

  bin_size = "1min"

Get the list of ``.yml`` files in the current directory

::

  yml_files = [f for f in os.listdir('.') if f.endswith('.yml')]
  yml_files.sort()

Create radio buttons to select a file

::

  input_yaml = st.radio("Select **yml** file to process:", yml_files)

Load the YAML file

::

  with open(input_yaml, "r") as file:
      events = yaml.safe_load(file)

Convert the loaded data (a list of dicts) into a DataFrame

::

  df = pd.DataFrame(events)

Convert the ``time`` column to datetime.

The provided time format is ``YYYY/MM/DD HH:MM:SS``

::

  df["time"] = pd.to_datetime(df["time"], format="%Y/%m/%d %H:%M:%S")

Set the time column as the index

::

  df.set_index("time", inplace=True)

Resample in ``bin_size`` intervals

The ``.resample()`` method groups data into bins of a specified time frequency.
The ``.size()`` function counts the number of events per bin.

::

  counts = df.resample(bin_size).size()

Reset the index to turn the time bins into a regular column (optional)

::

  chart_data = counts.reset_index(name="event_count")
  chart_data.set_index("time", inplace=True)

Plot with Streamlit 

::

  st.write("---")
  st.write(f"**Number of exceptions in `{bin_size}` intervals**")
  st.bar_chart(chart_data)

Export Excel

::

  if st.button("Export Excel"):
      output_excel = input_yaml + ".xlsx"
      df.to_excel(output_excel, index=True)
      st.write(f"File created `{output_excel}`")

Show table

::

  st.table(df)    
    