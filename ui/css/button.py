BUTTON_CSS = """/* Streamlit primary/secondary buttons */
button[kind="primary"],
[data-testid="stPopoverBody"] button[kind="primary"] {
    background-color: var(--primary) !important;
    border: var(--border-width) solid var(--border) !important;
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-sm) !important;
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
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-2xs) !important;
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
    border-radius: var(--radius) !important;
    box-shadow: var(--shadow-md) !important;
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

/* Style the st.popover trigger buttons to look like a clean, borderless menu icon */
div[data-testid="stPopover"] button {
    background-color: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 6px 12px !important;
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
