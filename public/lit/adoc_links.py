import yaml
import argparse
import textwrap

# AsciiDoc links
# ==============
#
# *Create list of AsciiDoc links from YAML*
#
#
# Structure of YAML file:
#
# .. code-block::
#
#    - name: 
#      note: 
#      history:
#        - date: 
#          file: 
#
# Usage:
#
# .. code-block::
#
#     usage: adoc_links.py [-h] input_yaml output_adoc
#
#     Create AsciiDoc links from YAML.
#
#     positional arguments:
#       input_yaml   Input YAML file
#       output_adoc  Output AsciiDoc file
#
#     options:
#       -h, --help   show this help message and exit
#
# Parse arguments:
#
# ::

parser = argparse.ArgumentParser(description="Create AsciiDoc links from YAML.")

parser.add_argument("input_yaml", help="Input YAML file")

parser.add_argument("output_adoc", help="Output AsciiDoc file")

args = parser.parse_args()


# Read YAML file:
#
# ::

with open(args.input_yaml, 'r') as file:
    data = yaml.safe_load(file)

def format_note(note):
    lines = note.strip().split("\n")
    note = " - ".join(lines)
    return note

# Output YAML records as a table with ``n_cols`` columns.
#
# ::

n_cols = 3

# Specify ``n_cols`` headers of ``1`` width.
#
# ::

def repeat_string_n_times(s, n):
    return ",".join(s for _ in range(n))

text = f"""
[cols="{repeat_string_n_times('1',n_cols)}"]
|===
"""

for d in data:
    icon = d['icon']
    link = d['link']
    name = d['name']
    note = d['note']
    note = format_note(note)

    text += textwrap.dedent(f"""
        a|    
        ====
        icon:{icon}[2x,role={{c}}flag] &nbsp;
        link:{link}[*{name}*] +
        &nbsp;&nbsp;&nbsp;
        """)
    text += f"_{note}_\n====\n"  

# Fill the remaining columns with blanks:
#
# ::

def calculate_empty_elements(len_data, n_col):
    # Calculate the number of elements in the last row
    elements_in_last_row = len_data % n_col

    # If the last row is completely filled, there are no empty elements
    if elements_in_last_row == 0:
        return 0

    # Return the number of empty elements in the last row
    return n_col - elements_in_last_row
    
for _ in range(calculate_empty_elements(len(data), n_cols)):
    text += f"a|\n" 
    
# Close the table:
#
# ::

text += """
|===
"""

# Write output file:
#
# ::

with open(args.output_adoc, 'w') as file:
    file.write(text)

print(f"AsciiDoc links created: {args.output_adoc}")    