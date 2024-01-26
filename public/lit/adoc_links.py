import yaml
import argparse

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
    
# Remove newlines from the note.
#
# ::

def format_note(note):
    lines = note.strip().split("\n")
    note = " - ".join(lines)
    return note

# Process YAML records:
#
# ::

text = """
[cols="1,1,1"]
|===
"""

for d in data:
    icon = d['icon']
    link = d['link']
    name = d['name']
    note = d['note']
    note = format_note(note)

    text += f"""
a|    
====
icon:{icon}[2x,role={{c}}flag] &nbsp;
link:{link}[
*{name}*] +
&nbsp;&nbsp;&nbsp;
_{note}_
====
"""    

text += """
|===
"""

# Write output file:
#
# ::

with open(args.output_adoc, 'w') as file:
    file.write(text)

print(f"AsciiDoc links created: {args.output_adoc}")    