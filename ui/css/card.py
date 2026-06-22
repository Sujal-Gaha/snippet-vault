CARD_CSS = """/* Card design for snippet blocks (including Streamlit's native st.container with border) */
.snippet-card,
div[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlockBorderWrapper"],
div.stElementContainer div[data-testid="stVerticalBlock"]:has(.snippet-title),
div.stElementContainer div[data-testid="stVerticalBlock"]:has(.snippet-card),
div.stElementContainer div[data-testid="stVerticalBlock"]:has([data-testid="stCodeBlock"]),
div.stElementContainer div[data-testid="stVerticalBlock"]:has(.tag-container) {
    background-color: var(--card) !important;
    border-radius: var(--radius-lg, var(--radius)) !important;
    padding: 24px !important;
    margin-bottom: 24px !important;
    border: var(--border-width) solid var(--border) !important;
    border-style: solid !important;
    border-width: var(--border-width) !important;
    border-color: var(--border) !important;
    box-shadow: var(--shadow) !important;
    transition: border-color 0.15s ease !important;
}

.snippet-card:hover,
div[data-testid="stVerticalBlockBorderWrapper"]:hover,
[data-testid="stVerticalBlockBorderWrapper"]:hover,
div.stElementContainer div[data-testid="stVerticalBlock"]:has(.snippet-title):hover,
div.stElementContainer div[data-testid="stVerticalBlock"]:has(.snippet-card):hover,
div.stElementContainer div[data-testid="stVerticalBlock"]:has([data-testid="stCodeBlock"]):hover,
div.stElementContainer div[data-testid="stVerticalBlock"]:has(.tag-container):hover {
    border-color: var(--primary) !important;
}

.snippet-title {
    color: var(--primary) !important;
    font-size: 1.4rem;
    font-weight: 600;
    display: inline-block;
}

/* Tags styling */
.tag-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 16px;
}
"""
