INPUT_CSS = """/* Input fields and dropdown select components */
div[data-baseweb="select"] > div, 
div[data-baseweb="input"] > div,
div[data-baseweb="base-input"] > input,
textarea,
input {
    background-color: var(--background) !important;
    color: var(--foreground) !important;
    border: var(--border-width) solid var(--border) !important;
    border-radius: var(--radius-md, var(--radius)) !important;
    font-size: 0.85rem !important;
}

div[data-baseweb="select"] *, 
div[data-baseweb="input"] *,
div[data-baseweb="base-input"] * {
    color: var(--foreground) !important;
}

input::placeholder,
textarea::placeholder {
    color: var(--foreground) !important;
    opacity: 0.5 !important;
}

div[data-baseweb="select"] > div:hover, 
div[data-baseweb="input"] > div:hover,
textarea:hover,
input:hover {
    border-color: var(--primary) !important;
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
    background-color: var(--popover) !important;
    border: var(--border-width) solid var(--border) !important;
    border-radius: var(--radius-md, var(--radius)) !important;
}
div[data-baseweb="popover"] ul,
div[data-baseweb="menu"] ul,
div[data-testid="stVirtualDropdown"] ul {
    background-color: var(--popover) !important;
}
div[data-baseweb="popover"] ul *,
div[data-baseweb="menu"] *,
div[data-testid="stVirtualDropdown"] *,
[data-testid="stVirtualDropdown"] * {
    background-color: transparent !important;
    color: var(--popover-foreground) !important;
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
    background-color: var(--popover) !important;
    color: var(--popover-foreground) !important;
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
    background-color: var(--primary) !important;
    color: var(--primary-foreground) !important;
}
"""
