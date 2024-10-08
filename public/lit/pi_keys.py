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
# Create HTML file with an output that contains HTML file with 3 columns: 
# ``key``, ``action name`` and ``command``.
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
import html

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

# .. function:: parse_keybinds(xml_file)
#
#     Parses the keybind records from the specified XML file and returns a list of tuples.
#     Each tuple contains the key and the corresponding action name.
#    
#     :param xml_file: Path to the XML file to parse.
#     :type xml_file: str
#
#     :return: List of tuples containing key and action name.
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
        action_els = keybind.findall(f"./{namespace}action")
        actions = []
        if len(action_els) > 0:
            for action_el in action_els:
                action = action_el.attrib.get('name', '')
                command_el = action_el.find(f"./{namespace}command")
                command = command_el.text if command_el is not None else ''
                actions.append((action, command))
            keybinds.append((key, actions))

    return keybinds
    
# .. function:: generate_html(keybinds, output_file)
#
#     Generates an HTML file with two columns: key and action name.
#    
#     :param keybinds: List of tuples containing key and action name.
#     :type keybinds: list
#    
#     :param output_file: Path to the HTML file to generate. 
#     :type output_file: str
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
            <th>Actions</th>
        </tr>
"""

    # Populate the table with keybinds
    for key, actions in keybinds:
        key = html.escape(key)  
        
        actions_content = ""
        for action, command in actions:         
            action = html.escape(action) 
            command = html.escape(command) 
            actions_content += f"<li>{action} <code>{command}</code></li>"
            
        html_content += f"""
            <tr>
                <td>{key}</td>
                <td><ul>{actions_content}</ul></td>
            </tr>
        """    

    html_content += """    </table>
</body>
</html>"""

    with open(output_file, 'w') as file:
        file.write(html_content)
    print(f"HTML file '{output_file}' has been created successfully.")

    
# .. function:: main()
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