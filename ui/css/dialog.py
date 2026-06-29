DIALOG_CSS = """/* Dialog modal styling overrides */
div[role="dialog"],
[data-testid="stDialog"] > div,
div[data-testid="stDialog"] {
    background-color: var(--popover) !important;
    color: var(--popover-foreground) !important;
    border: var(--border-width) solid var(--border) !important;
    border-radius: var(--radius-md, var(--radius)) !important;
    box-shadow: var(--shadow-xl) !important;
}
div[role="dialog"] h1,
div[role="dialog"] h2,
div[role="dialog"] h3,
div[role="dialog"] h4,
div[role="dialog"] h5,
div[role="dialog"] h6,
div[role="dialog"] p,
div[role="dialog"] label,
div[role="dialog"] span {
    color: var(--popover-foreground) !important;
}

/* Tab titles styling */
div[data-testid="stTabBar"] button p {
    color: var(--foreground) !important;
}
div[data-testid="stTabBar"] button[aria-selected="true"] p {
    color: var(--primary) !important;
}

/* Metric widget styling */
[data-testid="stMetricValue"] {
    color: var(--primary) !important;
}
[data-testid="stMetricLabel"] {
    color: var(--foreground) !important;
    opacity: 0.8;
}
"""
