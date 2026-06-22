import html
import streamlit as st
from db.repository import BaseSnippetRepository
from db.models import Snippet
from utils.helpers import truncate_desc, format_date
from ui.components.badge import render_badge
from ui.components.button import render_button


class SnippetUIRenderer:
    """Handles rendering of snippet layouts (Lists, Grids) and interactive sub-elements."""

    def __init__(self, repository: BaseSnippetRepository):
        self.repository = repository

    def _render_tags_row(self, tags: list[str]) -> None:
        """Reusable UI component for rendering the tags section."""
        if not tags:
            return
        tag_badges = "".join([render_badge(tag, "tag") for tag in tags])
        st.markdown(
            f'<div class="tag-container">{tag_badges}</div>',
            unsafe_allow_html=True,
        )

    def _render_snippet_header_html(self, snippet: Snippet) -> str:
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

    def _render_grid_header_html(self, snippet: Snippet) -> str:
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

    def render_list(self, snippets: list[Snippet], unique_cats: list[str]) -> None:
        """Renders the full details snippet list inside themed container cards."""
        for s in snippets:
            with st.container(border=True):
                # Header Row (Title, Type, Category, Options)
                header_col1, header_col2 = st.columns([8.8, 1.2])

                with header_col1:
                    header_html = self._render_snippet_header_html(s)
                    st.markdown(header_html, unsafe_allow_html=True)

                with header_col2:
                    self.render_options_popover(s, unique_cats)

                # Description
                if s.description:
                    st.markdown(s.description)

                # Code Block
                lang = s.language if s.language else "plaintext"
                st.code(s.content, language=lang)

                # Tags Row
                self._render_tags_row(s.tags)

    def render_grid(self, snippets: list[Snippet], unique_cats: list[str]) -> None:
        """Renders the compact grid snippet cards (2 columns) inside themed container cards."""
        N = 2
        cols = st.columns(N)
        for idx, s in enumerate(snippets):
            col = cols[idx % N]
            with col:
                with st.container(border=True):
                    # Title & Badges
                    header_html = self._render_grid_header_html(s)
                    st.markdown(header_html, unsafe_allow_html=True)

                    # Description (truncated)
                    desc_truncated = truncate_desc(s.description)
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
                            "View", key=f"comp_view_{s.id}", use_container_width=True
                        ):
                            from ui.dialogs import view_snippet_dialog
                            view_snippet_dialog(s)
                    with btn_col2:
                        self.render_options_popover(s, unique_cats, is_compact=True)

    def render_options_popover(
        self, snippet: Snippet, unique_cats: list[str], is_compact: bool = False
    ) -> None:
        """Renders the settings popover menu for re-categorization and deletion."""
        prefix = "comp_" if is_compact else ""
        with st.popover(
            "⋮",
            use_container_width=True,
            help="Options",
            key=f"{prefix}opt_pop_{snippet.id}",
        ):
            st.markdown("Options")

            st.markdown("**Move Category**")
            new_cat_sel = st.selectbox(
                "Destination Category",
                options=unique_cats,
                index=(
                    unique_cats.index(snippet.category)
                    if snippet.category in unique_cats
                    else 0
                ),
                key=f"{prefix}move_sel_{snippet.id}",
            )
            new_cat_txt = st.text_input(
                "Or Create New",
                placeholder="e.g. Databases, Docker",
                key=f"{prefix}move_txt_{snippet.id}",
            )
            if render_button(
                "Apply Move",
                key=f"{prefix}move_btn_{snippet.id}",
                type="primary",
                use_container_width=True,
            ):
                final_cat = new_cat_txt.strip() if new_cat_txt.strip() else new_cat_sel
                if not final_cat:
                    final_cat = "Uncategorized"
                self.repository.update_category(snippet.id, final_cat)
                st.success(f"Moved to {final_cat}!")
                st.rerun()

            st.markdown("---")
            st.markdown("**Danger Zone**")
            if render_button(
                "Delete Snippet",
                key=f"{prefix}del_{snippet.id}",
                type="secondary",
                use_container_width=True,
            ):
                self.repository.delete(snippet.id)
                st.success("Deleted!")
                st.rerun()
