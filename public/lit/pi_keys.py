# Rasp Hotkeys
# ------------
#
# Keyboard shortcuts can be found in ``/etc/xdg/openbox/lxde-pi-rc.xml`` file on 
# Raspberry Pi. We need to extract the list of ``keybind`` records at ``/openbox_config/keyboard`` xpath.
# Each record looks like this:
#
# .. code:: xml
#
#     <keybind key="C-S-Escape">
#       <action name="Execute">
#         <command>lxtask</command>
#       </action>
#     </keybind>
#
# Create HTML file with an output that contains HTML file with 2 columns: ``key`` and ``action name``.
#
# .. csv-table:: Useful Links
#    :header: "Name", "URL"
#    :widths: 10 30
#
#    "ElementTree XML API", https://docs.python.org/3/library/xml.etree.elementtree.html
#
# ::

import xml.etree.ElementTree as ET
import os

# Print banner.
#
# ::

print("""
888 888             d8     888 88P                         
888 888  e88 88e   d88     888 8P   ,e e,  Y8b Y888P  dP"Y 
8888888 d888 888b d88888   888 K   d88 88b  Y8b Y8P  C88b  
888 888 Y888 888P  888     888 8b  888   ,   Y8b Y    Y88D 
888 888  "88 88"   888     888 88b  "YeeP"    888    d,dP  
                                              888          
                                              888              
""")

# Parses the keybind records from the specified XML file and returns a list of tuples.
# Each tuple contains the key and the corresponding action name.
#
# Args:
#   xml_file (str): Path to the XML file to parse.
#
# Returns:
#   list: List of tuples containing key and action name.
#
# ::
    
def parse_keybinds(xml_file):
    if not os.path.exists(xml_file):
        raise FileNotFoundError(f"The file {xml_file} does not exist.")

    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Find the namespace (if any) in the XML
    namespace = ''
    if root.tag.startswith('{'):
        namespace = root.tag.split('}')[0] + '}'

    keybinds = []
    for keybind in root.findall(f".//{namespace}keybind"):
        key = keybind.attrib.get('key')
        action_el = keybind.find(f"./{namespace}action")
        action = action_el.attrib.get('name', '') if action_el is not None else ''
        command_el = action_el.find(f"./{namespace}command") if action_el is not None else None
        command = command_el.text if command_el is not None else ''
        keybinds.append((key, action, command))

    return keybinds

# Generates an HTML file with two columns: key and action name.
#
# Args:
#   keybinds (list): List of tuples containing key and action name.
#   output_file (str): Path to the HTML file to generate.      
# 
# ::      

def generate_html(keybinds, output_file):
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Raspberry Pi Hotkeys</title>
    <style>
        table {
            width: 50%;
            border-collapse: collapse;
            margin: 25px 0;
            font-size: 18px;
            text-align: left;
        }
        th, td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Raspberry Pi Hotkeys</h1>
    <table>
        <tr>
            <th>Key</th>
            <th>Action Name</th>
            <th>Command</th>
        </tr>
"""

    for key, action, command in keybinds:
        html_content += f"        <tr><td>{key}</td><td>{action}</td><td>{command}</td></tr>\n"

    html_content += """    </table>
</body>
</html>"""

    with open(output_file, 'w') as file:
        file.write(html_content)
    print(f"HTML file '{output_file}' has been created successfully.")

# Main
#
# ::

def main():
    xml_file = 'lxde-pi-rc.xml'
    output_file = 'raspberry_pi_hotkeys.html'

    # Parse keybinds from the XML file
    keybinds = parse_keybinds(xml_file)

    # Generate the HTML file
    generate_html(keybinds, output_file)

if __name__ == "__main__":
    main()