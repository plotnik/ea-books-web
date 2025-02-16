# Jira Stats
# ----------
#
# Process CSV file exported from JIRA filter with all columns.
#
# ::

import streamlit as st
import pandas as pd
import os

csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
csv_files.sort()
csv_file = st.sidebar.radio("Select exported JIRA filter CSV file to process:", csv_files)

df = pd.read_csv(csv_file)

def drop_columns_from_list():
    with open("drop_columns.txt", "r") as f:
        return [line.strip() for line in f]

def drop_columns_by_prefix():
    prefixes = [
        'Watchers Id',
        'Watchers',
        'Log Work',
        'Attachment',
        'Comment',
        'Components',
        'Labels',
        'Sprint',
    ]
    cols_to_drop = [col for col in df.columns if any(col.startswith(prefix) for prefix in prefixes)]
    # st.write(cols_to_drop)
    df.drop(columns=cols_to_drop, inplace=True)

drop_columns_by_prefix()
# df.drop(columns=drop_columns_from_list(), inplace=True)

st.sidebar.write("---")
num_rows = df.shape[0]
st.sidebar.write(f"Jiras: `{num_rows}`")

total_time_spent = df['Time Spent'].sum()
hours = round(total_time_spent/3600)
st.sidebar.write(f"Total time spent: `{hours}` h")

# Select row
#
# ::

num = st.number_input("Row", min_value=0, max_value=num_rows-1)

# Extract row to Series
#
# ::

dfs = df.iloc[num]
drops = dfs.dropna()
st.write(f"Num cols: `{dfs.shape[0]}`, not empty: `{drops.shape[0]}`")

# st.table(dfs)
st.table(drops)
