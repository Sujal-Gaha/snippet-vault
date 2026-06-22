DIALOG_CSS = """/* Dialog modal styling overrides */
div[role="dialog"],
[data-testid="stDialog"] > div,
div[data-testid="stDialog"] {
    background-color: $clr_sec_bg !important;
    color: $clr_text !important;
    border: 1px solid $clr_border !important;
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
    color: $clr_text !important;
}

/* Tab titles styling */
div[data-testid="stTabBar"] button p {
    color: $clr_text !important;
}
div[data-testid="stTabBar"] button[aria-selected="true"] p {
    color: $clr_primary !important;
}

/* Metric widget styling */
[data-testid="stMetricValue"] {
    color: $clr_primary !important;
}
[data-testid="stMetricLabel"] {
    color: $clr_text !important;
    opacity: 0.8;
}
"""
