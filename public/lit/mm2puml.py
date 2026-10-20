# Mermaid to PlantUML
# ===================
#
# When working with LangGraph_, paste the result of ``graph.get_graph().draw_mermaid()`` into the input, select
# PlantUML or GraphML, and copy or download the result. 
#
# Conversion runs locally;
# it requires neither LangGraph nor Java nor a diagram rendering service.
# For GraphML, open the download in yEd_ and choose **Layout → Hierarchical**.
#
# .. _LangGraph: https://www.langchain.com/langgraph
# .. _yEd: https://www.yworks.com/products/yed
#
# Scope and representation
# ------------------------
#
# We accept the flowchart subset emitted by LangGraph: graph/flowchart headers,
# optional Markdown fences and YAML front matter, five node shape syntaxes,
# solid and dotted arrows, inline nodes, chains, edge labels, and class styles.
# Each statement occupies its own line. Unsupported syntax raises an error so
# graph structure is never silently discarded.
#
# Both exports retain topology, labels, conditional edges, and six-digit hex
# fill colors. They do not reproduce Mermaid CSS or layout coordinates.
# PlantUML approximates shapes; GraphML retains shapes with an initial grid.
# The conversion functions remain importable without starting the interface.
#
# A small graph model
# -------------------
#
# Ordered dictionaries preserve the input's node order, giving both exporters
# stable aliases. Each edge records its source, target, label, and whether it
# is dotted. Class definitions are stored separately so declarations may follow
# the nodes that use them. All conversion dependencies are in Python's standard
# library; Streamlit is imported only when the interface starts.
#
# ::

from dataclasses import dataclass, field
import html
import re
import xml.etree.ElementTree as ET


@dataclass
class Node:
    label: str
    shape: str = 'rectangle'
    classes: list[str] = field(default_factory=list)


@dataclass
class Graph:
    nodes: dict[str, Node] = field(default_factory=dict)
    edges: list[tuple[str, str, str, bool]] = field(default_factory=list)
    styles: dict[str, dict[str, str]] = field(default_factory=dict)
    direction: str = 'TD'


# Recognizing and cleaning Mermaid
# -------------------------------
#
# Node patterns put nested stadium brackets before simpler shapes. Arrow
# alternatives capture conditional labels and ordinary pipe-delimited labels.
# HTML formatting is stripped and entities decoded to obtain plain-text labels.
#
# ::

ID = r'[A-Za-z_][\w-]*'
# Explicit alternatives keep the nested stadium syntax used for start/end intact.
NODE = re.compile(rf'({ID})(?:\(\[(.*?)\]\)|\(\((.*?)\)\)|\((.*?)\)|\[(.*?)\]|\{{(.*?)\}})?(?::::(\w+(?:,\w+)*))?')
ARROW = re.compile(r'(?:-\.\s*(.*?)\s*\.->|(-\.->)|-->|--\s+(.+?)\s+-->)\s*(?:\|([^|]*)\|\s*)?')


def clean(value: str) -> str:
    value = value.strip().strip('"')
    value = re.sub(r'<br\s*/?>', '\n', value, flags=re.I)
    return html.unescape(re.sub(r'<[^>]*>', '', value)).replace('\xa0', ' ').strip()


# Parsing one statement at a time
# -------------------------------
#
# Remove presentation wrappers first, then accumulate nodes, edges, and styles.
# A reference may introduce a node before its declaration supplies a label.
# The inner parser consumes one node and returns the unconsumed suffix, allowing
# chains to be processed without a separate tokenization pass. Every statement
# error carries its source line number and original text for the interface.
#
# ::

def parse_mermaid(source: str) -> Graph:
    source = source.strip()
    if source.startswith('```'):
        source = re.sub(r'^```(?:mermaid)?\s*\n', '', source)
        source = re.sub(r'\n```\s*$', '', source)
    if source.startswith('---'):
        parts = source.split('---', 2)
        if len(parts) != 3:
            raise ValueError('Unclosed YAML front matter.')
        source = parts[2]
    graph = Graph()
    header = False

    def node_at(text: str):
        match = NODE.match(text.strip())
        if not match:
            raise ValueError('Expected a node identifier.')
        groups = match.groups()
        name = groups[0]
        labels = groups[1:6]
        explicit = next((x for x in labels if x is not None), None)
        shape = 'roundrectangle' if labels[0] is not None or labels[2] is not None else 'ellipse' if labels[1] is not None else 'diamond' if labels[4] is not None else 'rectangle'
        classes = groups[6].split(',') if groups[6] else []
        if name not in graph.nodes or explicit is not None:
            graph.nodes[name] = Node(clean(explicit) if explicit is not None else name, shape, classes)
        elif classes:
            graph.nodes[name].classes = classes
        return name, text.strip()[match.end():].strip()

    for number, original in enumerate(source.splitlines(), 1):
        line = original.strip().rstrip(';').strip()
        if not line or line.startswith('%%'):
            continue
        try:
            match = re.fullmatch(r'(?:graph|flowchart)\s+(TD|TB|BT|LR|RL)', line)
            if match:
                graph.direction = match[1]
                header = True
                continue
            if line.startswith('classDef '):
                match = re.fullmatch(r'classDef\s+([\w,]+)\s+(.+)', line)
                if not match:
                    raise ValueError('Invalid classDef.')
                style = dict(x.split(':', 1) for x in match[2].split(',') if ':' in x)
                for name in match[1].split(','):
                    graph.styles[name] = style
                continue
            if line.startswith('class '):
                match = re.fullmatch(r'class\s+([\w,-]+)\s+([\w,]+)', line)
                if not match:
                    raise ValueError('Invalid class assignment.')
                for name in match[1].split(','):
                    graph.nodes.setdefault(name, Node(name)).classes = match[2].split(',')
                continue
            if not header:
                raise ValueError('Expected graph TD (or flowchart LR, etc.).')
            start, rest = node_at(line)
            while rest:
                arrow = ARROW.match(rest)
                if not arrow:
                    raise ValueError('Unsupported syntax after node; use one statement per line.')
                end, rest = node_at(rest[arrow.end():])
                label = clean(arrow[1] or arrow[3] or arrow[4] or '')
                graph.edges.append((start, end, label, arrow[1] is not None or arrow[2] is not None))
                start = end
        except ValueError as error:
            raise ValueError(f'Line {number}: {error}\n{original}') from error
    if not header or not graph.nodes:
        raise ValueError('Paste a Mermaid flowchart containing at least one node.')
    return graph


# Resolving colors and writing PlantUML
# ------------------------------------
#
# Start with the default class and apply explicit classes in order. Only hex
# colors are emitted; unsupported CSS values fall back to a readable lavender.
# Generated aliases isolate diagram identifiers from user labels, while escaping
# keeps quotes, backslashes, and multiline labels inside PlantUML strings.
# Horizontal graphs select left-to-right layout; reverse directions use explicit
# left/up arrows. Circles become use cases and other shapes become rectangles.
#
# ::

def color(graph: Graph, node: Node) -> str:
    style = dict(graph.styles.get('default', {}))
    for cls in node.classes:
        style.update(graph.styles.get(cls, {}))
    fill = style.get('fill', '#F2F0FF').strip()
    return fill if re.fullmatch(r'#[0-9a-fA-F]{6}', fill) else '#F2F0FF'


def puml_text(value: str) -> str:
    return value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', r'\n')


def to_plantuml(graph: Graph) -> str:
    aliases = {name: f'n{i}' for i, name in enumerate(graph.nodes)}
    lines = ['@startuml', 'skinparam shadowing false']
    if graph.direction in ('LR', 'RL'):
        lines.append('left to right direction')
    for name, node in graph.nodes.items():
        kind = 'usecase' if node.shape == 'ellipse' else 'rectangle'
        lines.append(f'{kind} "{puml_text(node.label)}" as {aliases[name]} {color(graph, node)}')
    for start, end, label, dotted in graph.edges:
        arrow = '..>' if dotted else '-->'
        if graph.direction in ('BT', 'RL'):
            arrow = '-[dotted]up->' if dotted and graph.direction == 'BT' else '-up->' if graph.direction == 'BT' else '-[dotted]left->' if dotted else '-left->'
        lines.append(f'{aliases[start]} {arrow} {aliases[end]}' + (f' : {puml_text(label)}' if label else ''))
    return '\n'.join(lines + ['@enduml', ''])


# Writing a yEd-compatible GraphML document
# ----------------------------------------
#
# GraphML contains topology; yWorks extension elements describe the appearance.
# ElementTree escapes labels for XML. Nodes receive label-sized boxes and grid
# coordinates so the initial document is visible before yEd arranges it. Edges
# carry directed arrowheads, optional labels, and dashed conditional styling.
#
# ::

G = 'http://graphml.graphdrawing.org/xmlns'
Y = 'http://www.yworks.com/xml/graphml'
ET.register_namespace('', G)
ET.register_namespace('y', Y)


def to_graphml(graph: Graph) -> str:
    root = ET.Element(f'{{{G}}}graphml')
    for key, scope, kind in [('d0', 'node', 'nodegraphics'), ('d1', 'edge', 'edgegraphics')]:
        ET.SubElement(root, f'{{{G}}}key', {'id': key, 'for': scope, 'yfiles.type': kind})
    body = ET.SubElement(root, f'{{{G}}}graph', id='G', edgedefault='directed')
    aliases = {name: f'n{i}' for i, name in enumerate(graph.nodes)}
    for i, (name, node) in enumerate(graph.nodes.items()):
        item = ET.SubElement(body, f'{{{G}}}node', id=aliases[name])
        data = ET.SubElement(item, f'{{{G}}}data', key='d0')
        shape = ET.SubElement(data, f'{{{Y}}}ShapeNode')
        # A grid gives immediately visible nodes; yEd can apply a hierarchical layout.
        x, y = (i % 4) * 240, (i // 4) * 110
        if graph.direction in ('BT', 'RL'):
            x, y = -x, -y
        ET.SubElement(shape, f'{{{Y}}}Geometry', x=str(x), y=str(y), width=str(max(170, max(map(len, node.label.splitlines() or [''])) * 8 + 24)), height=str(max(44, len(node.label.splitlines()) * 18 + 20)))
        ET.SubElement(shape, f'{{{Y}}}Fill', color=color(graph, node), transparent='false')
        ET.SubElement(shape, f'{{{Y}}}BorderStyle', color='#333333', type='line', width='1.0')
        ET.SubElement(shape, f'{{{Y}}}NodeLabel').text = node.label
        ET.SubElement(shape, f'{{{Y}}}Shape', type=node.shape)
    for i, (start, end, label, dotted) in enumerate(graph.edges):
        edge = ET.SubElement(body, f'{{{G}}}edge', id=f'e{i}', source=aliases[start], target=aliases[end])
        data = ET.SubElement(edge, f'{{{G}}}data', key='d1')
        poly = ET.SubElement(data, f'{{{Y}}}PolyLineEdge')
        ET.SubElement(poly, f'{{{Y}}}LineStyle', color='#333333', type='dashed' if dotted else 'line', width='1.0')
        ET.SubElement(poly, f'{{{Y}}}Arrows', source='none', target='standard')
        if label:
            ET.SubElement(poly, f'{{{Y}}}EdgeLabel').text = label
        ET.SubElement(poly, f'{{{Y}}}BendStyle', smoothed='false')
    ET.indent(root)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding='unicode') + '\n'


# The interactive application
# ---------------------------
#
# Streamlit reruns this function when the input or format changes. Conversion
# errors are shown next to the input; successful output includes counts, a copy
# button, and a download. UTF-8 text is base64-encoded before insertion into the
# copy button's script, preserving Unicode and keeping diagram text out of HTML
# and JavaScript syntax. Clipboard access first uses the browser API and then
# a temporary textarea; if both fail, the user can copy the output manually.
#
#
#
# ::

def main() -> None:
    """Present the converter in Streamlit."""
    import base64
    import streamlit as st
    import streamlit.components.v1 as components
  
    @st.cache_data
    def print_banner():
        print("""
                       #####                              
        #    # #    # #     # #####  #    # #    # #      
        ##  ## ##  ##       # #    # #    # ##  ## #      
        # ## # # ## #  #####  #    # #    # # ## # #      
        #    # #    # #       #####  #    # #    # #      
        #    # #    # #       #      #    # #    # #      
        #    # #    # ####### #       ####  #    # ######             
        """)
        return 1
  
    st.set_page_config(page_title='Mermaid converter', layout='wide')
    st.title('Mermaid → PlantUML / GraphML')
    st.caption('Paste a LangGraph draw_mermaid() flowchart. Labels and conditional edges are preserved.')
  
    print_banner()
  
    source = st.text_area('Mermaid input', height=340, placeholder='graph TD;\n    __start__ --> prepare_turn;\n    prepare_turn -. done .-> __end__;')
    format_name = st.radio('Output format', ['PlantUML', 'GraphML (yEd)'], horizontal=True)
    output = ''
    if source.strip():
        try:
            graph = parse_mermaid(source)
            output = to_plantuml(graph) if format_name == 'PlantUML' else to_graphml(graph)
            st.caption(f'{len(graph.nodes)} nodes · {len(graph.edges)} edges')
        except ValueError as error:
            st.error(str(error))
    st.text_area('Converted output', value=output, height=340, disabled=True)
    if output:
        payload = base64.b64encode(output.encode('utf-8')).decode('ascii')
        components.html('''
        <button id="copy" style="padding:8px 18px;cursor:pointer;border:1px solid #aaa;border-radius:6px;background:white">Copy</button>
        <span id="status" role="status" style="font:14px sans-serif;margin-left:10px"></span>
        <script>
        const text = new TextDecoder().decode(Uint8Array.from(atob("''' + payload + '''"), c => c.charCodeAt(0)));
        document.getElementById('copy').onclick = async () => {
          let copied = false;
          try { await navigator.clipboard.writeText(text); copied = true; } catch (_) {
            const area = document.createElement('textarea');
            area.value = text; area.style.position = 'fixed'; area.style.opacity = '0';
            document.body.appendChild(area); area.select();
            try { copied = document.execCommand('copy'); } finally { area.remove(); }
          }
          document.getElementById('status').textContent = copied ? 'Copied!' : 'Select the output and press Ctrl+C / Cmd+C.';
        };
        </script>
        ''', height=55)
        is_puml = format_name == 'PlantUML'
        st.download_button('Download', output, file_name='graph.puml' if is_puml else 'graph.graphml', mime='text/plain' if is_puml else 'application/xml')
        if not is_puml:
            st.caption('Open the .graphml file in yEd, then choose Layout → Hierarchical to arrange the graph.')


# Streamlit executes this file as a script. The guard also makes importing the
# graph model and converters safe for tests or use in other Python programs.
#
# ::

if __name__ == '__main__':
    main()
