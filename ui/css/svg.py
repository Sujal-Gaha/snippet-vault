SVG_CSS = """/* Force SVG icons inside select inputs, text inputs, sidebars, dialog close triggers, and popovers to match the text color */
div[data-baseweb="select"] svg,
div[data-baseweb="input"] svg,
div[data-baseweb="base-input"] svg,
[data-testid="stPopover"] svg,
[data-testid="stVirtualDropdown"] svg,
button[aria-label="Collapse sidebar"] svg,
button[aria-label="Expand sidebar"] svg,
[data-testid="stSidebarCollapseButton"] svg,
div[role="dialog"] button svg,
div[data-testid="stDialog"] button svg,
[role="option"] svg,
li[role="option"] svg {
    fill: $clr_text !important;
    stroke: $clr_text !important;
    color: $clr_text !important;
}

/* Ensure hovered option SVGs receive background/inverse color */
[role="option"]:hover svg,
[role="option"][aria-selected="true"] svg,
[role="option"][data-highlighted="true"] svg,
[data-active="true"] svg {
    fill: $clr_bg !important;
    stroke: $clr_bg !important;
    color: $clr_bg !important;
}
"""
