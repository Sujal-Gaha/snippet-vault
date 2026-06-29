BUTTON_CSS = """/* Streamlit primary/secondary buttons */
button[kind="primary"],
[data-testid="stPopoverBody"] button[kind="primary"] {
    background-color: var(--primary) !important;
    border: var(--border-width) solid var(--border) !important;
    border-radius: var(--radius-md, var(--radius)) !important;
    box-shadow: var(--shadow-sm) !important;
    padding: 4px 10px !important;
    font-size: 0.85rem !important;
    min-height: 28px !important;
}
button[kind="primary"],
button[kind="primary"] *,
[data-testid="stPopoverBody"] button[kind="primary"],
[data-testid="stPopoverBody"] button[kind="primary"] * {
    color: var(--primary-foreground) !important;
}
button[kind="primary"]:hover {
    opacity: 0.9 !important;
    box-shadow: var(--shadow-md) !important;
}
button[kind="primary"]:hover * {
    opacity: 0.9 !important;
}

button[kind="secondary"] {
    background-color: var(--secondary) !important;
    border: var(--border-width) solid var(--border) !important;
    border-radius: var(--radius-md, var(--radius)) !important;
    box-shadow: var(--shadow-2xs) !important;
    padding: 4px 10px !important;
    font-size: 0.85rem !important;
    min-height: 28px !important;
}
button[kind="secondary"],
button[kind="secondary"] * {
    color: var(--secondary-foreground) !important;
}
button[kind="secondary"]:hover {
    border-color: var(--primary) !important;
    background-color: var(--primary) !important;
    box-shadow: var(--shadow-sm) !important;
}
button[kind="secondary"]:hover * {
    color: var(--primary-foreground) !important;
}

/* Popovers background adjustment */
div[data-testid="stPopoverBody"] {
    background-color: var(--popover) !important;
    border: var(--border-width) solid var(--border) !important;
    border-radius: var(--radius-md, var(--radius)) !important;
    box-shadow: var(--shadow-md) !important;
    padding: 8px 12px !important;
    min-width: 320px !important;
}
div[data-testid="stPopoverBody"] * {
    color: var(--popover-foreground) !important;
}
/* Reset all inner div borders, background-colors, and shadows inside popovers (except select and input components) */
[data-testid="stPopoverBody"] div:not([data-baseweb="select"]):not([data-baseweb="select"] div):not([data-baseweb="input"]):not([data-baseweb="input"] div):not([data-baseweb="base-input"]):not([data-baseweb="base-input"] div),
div[class*="stPopoverBody"] div:not([data-baseweb="select"]):not([data-baseweb="select"] div):not([data-baseweb="input"]):not([data-baseweb="input"] div):not([data-baseweb="base-input"]):not([data-baseweb="base-input"] div) {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

[data-testid="stPopoverBody"] [data-testid="stVerticalBlockBorderWrapper"],
div[class*="stPopoverBody"] [data-testid="stVerticalBlockBorderWrapper"] {
    padding: 0 !important;
    margin: 0 !important;
}

/* Reduce spacing inside popovers */
[data-testid="stPopoverBody"] [data-testid="stVerticalBlock"],
div[class*="stPopoverBody"] [data-testid="stVerticalBlock"] {
    gap: 6px !important;
}

[data-testid="stPopoverBody"] hr,
div[class*="stPopoverBody"] hr {
    margin: 6px 0 !important;
}

[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] p,
[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] h1,
[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] h2,
[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] h3,
[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] h4,
[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] h5,
[data-testid="stPopoverBody"] [data-testid="stMarkdownContainer"] h6,
div[class*="stPopoverBody"] [data-testid="stMarkdownContainer"] p {
    margin-top: 0 !important;
    margin-bottom: 2px !important;
}

[data-testid="stPopoverBody"] [data-testid="element-container"],
div[class*="stPopoverBody"] [data-testid="element-container"] {
    margin-bottom: 2px !important;
}

/* Style the st.popover trigger buttons to look like a clean, borderless menu icon */
div[data-testid="stPopover"] button {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 4px 8px !important;
    margin: 0 !important;
    width: auto !important;
    min-width: 0 !important;
    min-height: 0 !important;
    color: var(--foreground) !important;
    cursor: pointer !important;
    transition: color 0.15s ease, background-color 0.15s ease !important;
}

div[data-testid="stPopover"] button:hover,
div[data-testid="stPopover"] button:active,
div[data-testid="stPopover"] button:focus {
    color: var(--primary) !important;
    background-color: rgba(128, 128, 128, 0.15) !important;
    border-radius: 50% !important;
    outline: none !important;
}

/* Hide the chevron arrow inside the st.popover trigger button */
div[data-testid="stPopover"] button svg,
div[data-testid="stPopover"] button span[data-testid="stIcon"],
div[data-testid="stPopover"] button div[class*="chevron"],
div[data-testid="stPopover"] button svg[class*="chevron"],
div[data-testid="stPopover"] button > *:not(:first-child),
div[data-testid="stPopover"] button * > *:not(:first-child) {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}

/* Disable pseudo-elements representing icons */
div[data-testid="stPopover"] button::after,
div[data-testid="stPopover"] button::before,
div[data-testid="stPopover"] button *::after,
div[data-testid="stPopover"] button *::before {
    content: none !important;
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}
"""
