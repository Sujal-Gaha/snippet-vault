INPUT_CSS = """/* Input fields and dropdown select components */
div[data-baseweb="select"] > div, 
div[data-baseweb="input"] > div,
div[data-baseweb="base-input"] > input,
textarea,
input {
    background-color: $clr_bg !important;
    color: $clr_text !important;
    border-color: $clr_border !important;
}

div[data-baseweb="select"] *, 
div[data-baseweb="input"] *,
div[data-baseweb="base-input"] * {
    color: $clr_text !important;
}

input::placeholder,
textarea::placeholder {
    color: $clr_text !important;
    opacity: 0.5 !important;
}

div[data-baseweb="select"] > div:hover, 
div[data-baseweb="input"] > div:hover,
textarea:hover,
input:hover {
    border-color: $clr_primary !important;
}

/* BaseWeb and Streamlit virtualized selectbox dropdown list styles (rendered outside .stApp via React portals) */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="menu"],
div[data-baseweb="menu"] > div,
ul[role="listbox"],
ul[role="listbox"] div,
div[data-testid="stVirtualDropdown"],
div[data-testid="stVirtualDropdown"] > div,
[data-testid="stVirtualDropdown"] {
    background-color: $clr_sec_bg !important;
    border-color: $clr_border !important;
}
div[data-baseweb="popover"] ul,
div[data-baseweb="menu"] ul,
div[data-testid="stVirtualDropdown"] ul {
    background-color: $clr_sec_bg !important;
}
div[data-baseweb="popover"] ul *,
div[data-baseweb="menu"] *,
div[data-testid="stVirtualDropdown"] *,
[data-testid="stVirtualDropdown"] * {
    background-color: transparent !important;
    color: $clr_text !important;
}

/* Global Listbox & Option styling overrides (selectbox dropdown items and nested wrappers) */
[role="listbox"],
[role="listbox"] *,
[role="option"],
[role="option"] *,
[role="option"] > div,
[role="option"] > span,
div[data-baseweb="popover"] li,
div[data-baseweb="menu"] li,
li[role="option"],
div[role="option"],
[data-testid="stVirtualDropdown"] div[role="option"] {
    background-color: $clr_sec_bg !important;
    color: $clr_text !important;
    transition: background-color 0.1s ease !important;
}

/* Highlighted/Hovered states for options and all descendants (forcing colors to Mauve and Base background) */
[role="option"]:hover,
[role="option"]:hover *,
[role="option"][aria-selected="true"],
[role="option"][aria-selected="true"] *,
[role="option"][data-highlighted="true"],
[role="option"][data-highlighted="true"] *,
[data-active="true"],
[data-active="true"] *,
li[role="option"]:hover,
li[role="option"]:hover *,
div[role="option"]:hover,
div[role="option"]:hover *,
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li:hover *,
div[data-baseweb="popover"] li[aria-selected="true"],
div[data-baseweb="popover"] li[aria-selected="true"] *,
div[data-baseweb="popover"] li[data-highlighted="true"],
div[data-baseweb="popover"] li[data-highlighted="true"] *,
div[data-baseweb="menu"] li:hover,
div[data-baseweb="menu"] li:hover *,
[data-testid="stVirtualDropdown"] div[role="option"]:hover,
[data-testid="stVirtualDropdown"] div[role="option"]:hover *,
[data-testid="stVirtualDropdown"] [data-active="true"],
[data-testid="stVirtualDropdown"] [data-active="true"] * {
    background-color: $clr_primary !important;
    color: $clr_bg !important;
}
"""
