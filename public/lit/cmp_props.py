# Compare Properties
# ------------------
#
# ::

import streamlit as st
import argparse

# Two file names as arguments.
#
# ::
    
parser = argparse.ArgumentParser(description="Compare properties")

parser.add_argument("file1", help="1st file")
parser.add_argument("file2", help="2nd file")

args = parser.parse_args()

st.write(f"1st file: `{args.file1}`")
st.write(f"2nd file: `{args.file2}`")

# Read properties
#
# ::
    
def read_properties(file_path):
    properties = {}
    with open(file_path, 'r') as file:
        current_key = None
        current_value = []
      
        for line in file:
            line = line.strip()
            # Ignore comments and empty lines
            if not line or line.startswith('#'):
                continue

            if '=' in line:
                # If we were reading a multi-line value, save the previous key-value pair
                if current_key is not None:
                    properties[current_key] = ' '.join(current_value).replace("\\", "").strip()
              
                # Start a new key-value pair
                current_key, value = line.split('=', 1)
                current_key = current_key.strip()
                current_value = [value.strip()]
            else:
                # Continue with a multi-line value
                current_value.append(line.strip())
      
        # Save the last key-value pair
        if current_key is not None:
            properties[current_key] = ' '.join(current_value).replace("\\", "").strip()
  
    return properties

# Compare properties
#
# ::
    
def compare_properties(file1, file2):
    # Read the properties from both files
    props1 = read_properties(file1)
    props2 = read_properties(file2)

    # Convert keys to sets for comparison
    keys1 = set(props1.keys())
    keys2 = set(props2.keys())

    # Determine added, deleted, and changed properties
    added = keys2 - keys1
    deleted = keys1 - keys2
    changed = {key for key in keys1 & keys2 if props1[key] != props2[key]}

    # Output results
    st.write(f"### Added Properties `({len(added)})`:")
    for key in added:
        st.write(f"  **{key}** = `{props2[key]}`")
  
    st.write(f"### Deleted Properties `({len(deleted)})`:")
    for key in deleted:
        st.write(f"  **{key}** = `{props1[key]}`")

    st.write(f"### Changed Properties `({len(changed)})`:")
    for key in changed:
        st.write(f"""
            **{key}**:
            ```
            `{props1[key]}`
            `{props2[key]}`
            ```
            """)

# Main
#
# ::
    
compare_properties(args.file1, args.file2)
