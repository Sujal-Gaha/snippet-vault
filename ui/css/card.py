CARD_CSS = """/* Card design for snippet blocks (including Streamlit's native st.container with border) */
.snippet-card,
div[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlockBorderWrapper"],
div.stElementContainer div[data-testid="stVerticalBlock"]:has(.snippet-title),
div.stElementContainer div[data-testid="stVerticalBlock"]:has(.snippet-card),
div.stElementContainer div[data-testid="stVerticalBlock"]:has([data-testid="stCodeBlock"]),
div.stElementContainer div[data-testid="stVerticalBlock"]:has(.tag-container) {
    background-color: $clr_sec_bg !important;
    border-radius: 12px !important;
    padding: 24px !important;
    margin-bottom: 24px !important;
    border: 1px solid $clr_border !important;
    border-style: solid !important;
    border-width: 1px !important;
    border-color: $clr_border !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.03) !important;
    transition: border-color 0.15s ease !important;
}

.snippet-card:hover,
div[data-testid="stVerticalBlockBorderWrapper"]:hover,
[data-testid="stVerticalBlockBorderWrapper"]:hover,
div.stElementContainer div[data-testid="stVerticalBlock"]:has(.snippet-title):hover,
div.stElementContainer div[data-testid="stVerticalBlock"]:has(.snippet-card):hover,
div.stElementContainer div[data-testid="stVerticalBlock"]:has([data-testid="stCodeBlock"]):hover,
div.stElementContainer div[data-testid="stVerticalBlock"]:has(.tag-container):hover {
    border-color: $clr_primary !important;
}

.snippet-title {
    color: $clr_primary !important;
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 5px;
    display: inline-block;
}

/* Tags styling */
.tag-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 15px;
}
"""
