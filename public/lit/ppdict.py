# Pretty-print dict
# =================
#
# Parse and pretty-print a string that looks like a Python dictionary.
#
# This is useful when copying structured output from logs, especially when the
# output contains Python-style objects such as ``HumanMessage(...)`` or
# ``AIMessage(...)``. These values are not valid JSON, so they cannot be formatted
# directly with ``json.dumps()``.
#
# **Example input:**
#
# ``{'messages': [HumanMessage(content='I was charged twice for my subscription', additional_kwargs={}, response_metadata={}, id='eb138f10-e9bb-4f8e-ac4e-dbee024e4cdd'), AIMessage(content='[Triage] Transferring to billing: The customer is inquiring about a payment issue related to being charged twice for their subscription.', additional_kwargs={}, response_metadata={}, id='dc0148ac-c103-4c24-8901-f7a2d9450118', tool_calls=[], invalid_tool_calls=[])], 'current_agent': 'billing', 'handoff_reason': 'The customer is inquiring about a payment issue related to being charged twice for their subscription.', 'context_summary': 'Customer was charged twice for their subscription.'}``
#
# **Example output:**
#
# .. code:: python
#
#    {
#      'messages': [
#        {
#          'type': 'HumanMessage',
#          'content': 'I was charged twice for my subscription',
#          'additional_kwargs': {},
#          'response_metadata': {},
#          'id': 'eb138f10-e9bb-4f8e-ac4e-dbee024e4cdd'
#        },
#        {
#          'type': 'AIMessage',
#          'content': '[Triage] Transferring to billing: The customer is inquiring about a payment issue related to being charged twice for their subscription.',
#          'additional_kwargs': {},
#          'response_metadata': {},
#          'id': 'dc0148ac-c103-4c24-8901-f7a2d9450118',
#          'tool_calls': [],
#          'invalid_tool_calls': []
#        }
#      ],
#      'current_agent': 'billing',
#      'handoff_reason': 'The customer is inquiring about a payment issue related to being charged twice for their subscription.',
#      'context_summary': 'Customer was charged twice for their subscription.'
#    }
#
# **Notes:**
#
# The input is Python-like, not JSON. For that reason, the script should avoid
# ``eval()`` and use a safer parsing approach such as ``ast.parse()`` together
# with ``ast.literal_eval()`` after transforming unsupported object calls.
#
# ----
#
# ::

import ast
import streamlit as st

# Print banner
#
# ::

st.set_page_config(
    page_title="ppdict",
)

@st.cache_data
def print_banner():
    print("""
                              d8b   d8,                         
                              88P  `8P           d8P            
                             d88              d888888P          
    ?88,.d88b,?88,.d88b, d888888    88b d8888b  ?88'            
    `?88'  ?88`?88'  ?88d8P' ?88    88Pd8P' `P  88P             
      88b  d8P  88b  d8P88b  ,88b  d88 88b      88b             
      888888P'  888888P'`?88P'`88bd88' `?888P'  `?8b            
      88P'      88P'                                            
     d88       d88                                              
     ?8P       ?8P                                              
    """)
    return 1

print_banner()

# Input text
#
# ::

dict_str = st.text_area("dict:", height=300)

# Parse input
#
# ::

class SafeTransformer(ast.NodeTransformer):
    def visit_Call(self, node):
        # Convert something like HumanMessage(...) into a dict
        return ast.Dict(
            keys=[ast.Constant("type")] + [kw.arg and ast.Constant(kw.arg) for kw in node.keywords],
            values=[ast.Constant(node.func.id)] + [kw.value for kw in node.keywords],
        )

def parse_log_dict(log_str: str):
    tree = ast.parse(log_str, mode="eval")
    tree = SafeTransformer().visit(tree)
    ast.fix_missing_locations(tree)
    return ast.literal_eval(tree)

if st.button("parse", type="primary", width="stretch"):
    try:
        parsed = parse_log_dict(dict_str)
        st.write(parsed)
    except Exception as e:
        st.error(e)
