# exc histo
# =========
#
# Display histogram from ``yml`` file created by exc_yaml_.
#
# .. _exc_yaml: exc_yaml.py.html
#
# ::

import streamlit as st
import pandas as pd
import yaml
import argparse

parser = argparse.ArgumentParser(description="histo")
parser.add_argument("input_yaml", help="YAML file created by exc_yaml")
args = parser.parse_args()

# Bin size.
#
# ::

bin_size = "1min"

# **Step 1.** Load the YAML file
#
# ::

with open(args.input_yaml, "r") as file:
    events = yaml.safe_load(file)

# Convert the loaded data (a list of dicts) into a DataFrame
#
# ::

df = pd.DataFrame(events)

# **Step 2.** Process the time field
#
# Convert the 'time' column to datetime.
# The provided time format is "YYYY/MM/DD HH:MM:SS"
#
# ::

df["time"] = pd.to_datetime(df["time"], format="%Y/%m/%d %H:%M:%S")

# **Step 3.** Set the time column as the index
#
# ::

df.set_index("time", inplace=True)

# **Step 4.** Resample in ``bin_size`` intervals
#
# The ``.resample()`` method groups data into bins of a specified time frequency.
# The ``.size()`` function counts the number of events per bin.
#
# ::

counts = df.resample(bin_size).size()

# Reset the index to turn the time bins into a regular column (optional)
#
# ::

chart_data = counts.reset_index(name="event_count")
chart_data.set_index("time", inplace=True)

# **Step 5.** Plot with Streamlit 
#
# ::

st.write(f"Number of exceptions in {bin_size} intervals")
st.bar_chart(chart_data)