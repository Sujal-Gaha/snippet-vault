import streamlit as st
from db.repository import BaseSnippetRepository
from db.models import Snippet
from ui.components.input import render_selectbox, render_text_input
from ui.components.button import render_button
from ui.components.card import render_list_card, render_grid_card


class SnippetUIRenderer:
    """Handles rendering of snippet layouts (Lists, Grids) and interactive sub-elements."""

    def __init__(self, repository: BaseSnippetRepository):
        self.repository = repository

    def render_list(self, snippets: list[Snippet], unique_cats: list[str]) -> None:
        """Renders the full details snippet list inside themed container cards."""
        for s in snippets:
            render_list_card(s, unique_cats, self.render_options_popover)

    def render_grid(self, snippets: list[Snippet], unique_cats: list[str]) -> None:
        """Renders the compact grid snippet cards (2 columns) inside themed container cards."""
        N = 2
        cols = st.columns(N)
        for idx, s in enumerate(snippets):
            col = cols[idx % N]
            with col:
                render_grid_card(s, unique_cats, self.render_options_popover)

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
            new_cat_sel = render_selectbox(
                "Destination Category",
                options=unique_cats,
                index=(
                    unique_cats.index(snippet.category)
                    if snippet.category in unique_cats
                    else 0
                ),
                key=f"{prefix}move_sel_{snippet.id}",
            )
            new_cat_txt = render_text_input(
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
