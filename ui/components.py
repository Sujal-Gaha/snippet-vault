import html
import streamlit as st
from db.repository import BaseSnippetRepository
from db.models import Snippet
from ui.dialogs import view_snippet_dialog
from utils.helpers import truncate_desc, format_date

class SnippetUIRenderer:
    """Handles rendering of snippet layouts (Lists, Grids) and interactive sub-elements."""
    
    def __init__(self, repository: BaseSnippetRepository):
        self.repository = repository

    def render_list(self, snippets, unique_cats):
        """Renders the full details snippet list."""
        for s in snippets:
            st.markdown(f'<div class="snippet-card">', unsafe_allow_html=True)
            
            # Header Row (Title, Type, Category, Options)
            header_col1, header_col2 = st.columns([8.8, 1.2])
            
            with header_col1:
                badge_class = "type-badge-code" if s.type == "Code" else "type-badge-command"
                date_str = format_date(s.created_at)
                escaped_type = html.escape(s.type)
                escaped_category = html.escape(s.category)
                escaped_title = html.escape(s.title)
                st.markdown(
                    f'<div>'
                    f'<span class="{badge_class}">{escaped_type}</span>'
                    f'<span class="category-badge">📁 {escaped_category}</span>'
                    f'<span class="snippet-title">{escaped_title}</span>'
                    f'</div>'
                    f'<div style="color: var(--text-color); opacity: 0.65; font-size: 0.85rem; margin-top: 6px; margin-bottom: 12px;">'
                    f'Added on {date_str}</div>',
                    unsafe_allow_html=True
                )
            
            with header_col2:
                self.render_options_popover(s, unique_cats)
            
            # Description
            if s.description:
                st.markdown(s.description)
                
            # Code Block
            lang = s.language if s.language else "plaintext"
            st.code(s.content, language=lang)
            
            # Tags Row
            if s.tags:
                tag_badges = "".join([f'<span class="tag-badge">#{html.escape(tag)}</span>' for tag in s.tags])
                st.markdown(f'<div class="tag-container">{tag_badges}</div>', unsafe_allow_html=True)
                
            st.markdown('</div>', unsafe_allow_html=True)

    def render_grid(self, snippets, unique_cats):
        """Renders the compact grid snippet cards (2 columns)."""
        N = 2
        cols = st.columns(N)
        for idx, s in enumerate(snippets):
            col = cols[idx % N]
            with col:
                st.markdown(f'<div class="snippet-card">', unsafe_allow_html=True)
                
                # Title & Badges
                badge_class = "type-badge-code" if s.type == "Code" else "type-badge-command"
                escaped_type = html.escape(s.type)
                escaped_category = html.escape(s.category)
                escaped_title = html.escape(s.title)
                st.markdown(
                    f'<div style="min-height: 80px;">'
                    f'<span class="{badge_class}" style="font-size: 0.7rem; padding: 2px 6px;">{escaped_type}</span>'
                    f'<span class="category-badge" style="font-size: 0.7rem; padding: 2px 6px;">📁 {escaped_category}</span>'
                    f'<div class="snippet-title" style="font-size: 1.1rem; margin-top: 6px;">{escaped_title}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
                # Description (truncated)
                desc_truncated = truncate_desc(s.description)
                if desc_truncated:
                    escaped_desc = html.escape(desc_truncated)
                    st.markdown(f'<div style="font-size: 0.9rem; min-height: 60px; color: var(--text-color); opacity: 0.85; line-height: 1.4; margin-bottom: 12px;">{escaped_desc}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div style="min-height: 60px; font-style: italic; color: gray; font-size: 0.9rem; margin-bottom: 12px;">No description provided.</div>', unsafe_allow_html=True)
                    
                # Footer: buttons row
                btn_col1, btn_col2 = st.columns([4, 1])
                with btn_col1:
                    if st.button("👁️ View", key=f"comp_view_{s.id}", use_container_width=True):
                        view_snippet_dialog(s)
                with btn_col2:
                    self.render_options_popover(s, unique_cats, is_compact=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

    def render_options_popover(self, snippet: Snippet, unique_cats, is_compact=False):
        """Renders the settings popover menu for re-categorization and deletion."""
        prefix = "comp_" if is_compact else ""
        with st.popover("⚙️", use_container_width=True, help="Options", key=f"{prefix}opt_pop_{snippet.id}"):
            st.markdown("### ⚙️ Options")
            
            st.markdown("**📁 Move Category**")
            new_cat_sel = st.selectbox(
                "Destination Category",
                options=unique_cats,
                index=unique_cats.index(snippet.category) if snippet.category in unique_cats else 0,
                key=f"{prefix}move_sel_{snippet.id}"
            )
            new_cat_txt = st.text_input(
                "Or Create New",
                placeholder="e.g. Databases, Docker",
                key=f"{prefix}move_txt_{snippet.id}"
            )
            if st.button("Apply Move", key=f"{prefix}move_btn_{snippet.id}", type="primary", use_container_width=True):
                final_cat = new_cat_txt.strip() if new_cat_txt.strip() else new_cat_sel
                if not final_cat:
                    final_cat = "Uncategorized"
                self.repository.update_category(snippet.id, final_cat)
                st.success(f"Moved to {final_cat}!")
                st.rerun()
                
            st.markdown("---")
            st.markdown("**⚠️ Danger Zone**")
            if st.button("🗑️ Delete Snippet", key=f"{prefix}del_{snippet.id}", type="secondary", use_container_width=True):
                self.repository.delete(snippet.id)
                st.success("Deleted!")
                st.rerun()
