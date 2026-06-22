import html
import streamlit as st
from db.models import Snippet
from utils.helpers import truncate_desc, format_date
from ui.components.badge import render_badge
from ui.components.button import render_button

def _render_tags_row(tags: list[str]) -> None:
    """Reusable UI component for rendering the tags section."""
    if not tags:
        return
    tag_badges = "".join([render_badge(tag, "tag") for tag in tags])
    st.markdown(
        f'<div class="tag-container">{tag_badges}</div>',
        unsafe_allow_html=True,
    )

def _render_snippet_header_html(snippet: Snippet) -> str:
    """Reusable HTML component for snippet metadata header in List View."""
    badge_type = "code" if snippet.type == "Code" else "command"
    badge_html = render_badge(snippet.type, badge_type)
    cat_html = render_badge(snippet.category, "category")
    escaped_title = html.escape(snippet.title)
    date_str = format_date(snippet.created_at)

    return (
        f"<div>"
        f'<span class="snippet-title">{escaped_title}</span>'
        f"<br />"
        f"{badge_html}"
        f"{cat_html}"
        f"</div>"
        f'<div style="color: var(--text-color); opacity: 0.65; font-size: 0.85rem; margin-top: 6px; margin-bottom: 12px;">'
        f"Added on {date_str}</div>"
    )

def _render_grid_header_html(snippet: Snippet) -> str:
    """Reusable HTML component for snippet metadata header in Grid View."""
    badge_type = "code" if snippet.type == "Code" else "command"
    badge_html = render_badge(
        snippet.type, badge_type, "font-size: 0.7rem; padding: 2px 6px;"
    )
    cat_html = render_badge(
        snippet.category, "category", "font-size: 0.7rem; padding: 2px 6px;"
    )
    escaped_title = html.escape(snippet.title)

    return (
        f'<div style="min-height: 80px;">'
        f"{badge_html}"
        f"{cat_html}"
        f'<div class="snippet-title" style="font-size: 1.1rem; margin-top: 6px;">{escaped_title}</div>'
        f"</div>"
    )

def render_list_card(snippet: Snippet, unique_cats: list[str], render_options_popover_fn) -> None:
    """Renders a single detailed list card container."""
    with st.container(border=True):
        # Header Row (Title, Type, Category, Options)
        header_col1, header_col2 = st.columns([8.8, 1.2])

        with header_col1:
            header_html = _render_snippet_header_html(snippet)
            st.markdown(header_html, unsafe_allow_html=True)

        with header_col2:
            render_options_popover_fn(snippet, unique_cats)

        # Description
        if snippet.description:
            st.markdown(snippet.description)

        # Code Block
        lang = snippet.language if snippet.language else "plaintext"
        st.code(snippet.content, language=lang)

        # Tags Row
        _render_tags_row(snippet.tags)

def render_grid_card(snippet: Snippet, unique_cats: list[str], render_options_popover_fn) -> None:
    """Renders a single compact grid card container."""
    with st.container(border=True):
        # Title & Badges
        header_html = _render_grid_header_html(snippet)
        st.markdown(header_html, unsafe_allow_html=True)

        # Description (truncated)
        desc_truncated = truncate_desc(snippet.description)
        if desc_truncated:
            escaped_desc = html.escape(desc_truncated)
            st.markdown(
                f'<div style="font-size: 0.9rem; min-height: 60px; color: var(--text-color); opacity: 0.85; line-height: 1.4; margin-bottom: 12px;">{escaped_desc}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div style="min-height: 60px; font-style: italic; color: gray; font-size: 0.9rem; margin-bottom: 12px;">No description provided.</div>',
                unsafe_allow_html=True,
            )

        # Footer: buttons row
        btn_col1, btn_col2 = st.columns([4, 1])
        with btn_col1:
            if render_button(
                "View", key=f"comp_view_{snippet.id}", use_container_width=True
            ):
                from ui.components.dialogs import view_snippet_dialog
                view_snippet_dialog(snippet)
        with btn_col2:
            render_options_popover_fn(snippet, unique_cats, is_compact=True)
