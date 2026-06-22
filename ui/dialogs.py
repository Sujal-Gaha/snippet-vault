import streamlit as st
from db.repository import BaseSnippetRepository
from db.models import Snippet
from utils.helpers import format_date
from ui.components.badge import render_badge
from ui.components.button import render_button


@st.dialog("Add New Snippet / Command", width="large")
def add_snippet_dialog(repository: BaseSnippetRepository):
    # Fetch fresh list for category selectbox
    snippets = repository.get_all()
    existing_cats = repository.get_existing_categories(snippets)

    title = st.text_input(
        "Title", placeholder="e.g. Docker Clean Containers", max_chars=100
    )

    snippet_type = st.radio("Type", ["Code", "Command"], horizontal=True)

    language = st.selectbox(
        "Syntax Highlighting",
        (
            [
                "bash",
                "python",
                "javascript",
                "sql",
                "html",
                "css",
                "json",
                "yaml",
                "plaintext",
            ]
            if snippet_type == "Code"
            else ["bash", "plaintext"]
        ),
    )

    content = st.text_area(
        "Snippet / Command",
        placeholder="Paste code or command line here...",
        height=150,
    )
    description = st.text_area(
        "Description (supports Markdown)",
        placeholder="What does this do? Supports **bold**, *italics*, `code`, lists, tables, links...",
        height=100,
    )

    # Category selection & creation
    cat_col1, cat_col2 = st.columns(2)
    with cat_col1:
        cat_sel = st.selectbox(
            "Assign Category",
            options=existing_cats,
            index=(
                existing_cats.index("Uncategorized")
                if "Uncategorized" in existing_cats
                else 0
            ),
            help="Select an existing category from the dropdown",
        )
    with cat_col2:
        cat_new = st.text_input(
            "Or Create New Category",
            placeholder="e.g. Databases, Docker, Git",
            help="Type to create and assign a new category (overrides selection)",
        )

    tags = st.text_input(
        "Tags (comma-separated)", placeholder="e.g. docker, devops, cleanup"
    )

    col1, col2, col3 = st.columns([1.2, 1.2, 3])
    with col1:
        if render_button("Save", type="primary", use_container_width=True):
            if not title.strip():
                st.error("Please enter a title.")
            elif not content.strip():
                st.error("Please enter snippet/command content.")
            else:
                final_cat = cat_new.strip() if cat_new.strip() else cat_sel
                if not final_cat:
                    final_cat = "Uncategorized"

                # Instantiate Snippet model
                new_snippet = Snippet(
                    id_val=None,
                    title=title.strip(),
                    content=content.strip(),
                    description=description.strip(),
                    tags=tags.strip(),
                    snippet_type=snippet_type,
                    language=language,
                    category=final_cat,
                )
                repository.add(new_snippet)
                st.success("Saved!")
                st.rerun()
    with col2:
        if render_button("Cancel", use_container_width=True):
            st.rerun()


@st.dialog("Snippet Details", width="large")
def view_snippet_dialog(snippet: Snippet):
    badge_type = "code" if snippet.type == "Code" else "command"
    badge_html = render_badge(snippet.type, badge_type)
    cat_html = render_badge(snippet.category, "category")

    st.markdown(
        f"<div>"
        f"{badge_html}"
        f"{cat_html}"
        f"</div>",
        unsafe_allow_html=True,
    )

    st.title(snippet.title)
    st.markdown(f"**Added on:** {format_date(snippet.created_at)}")
    st.markdown("---")

    if snippet.description:
        st.markdown("##### Description")
        st.markdown(snippet.description)

    st.markdown("##### Code / Command")
    lang = snippet.language if snippet.language else "plaintext"
    st.code(snippet.content, language=lang)

    if snippet.tags:
        tag_badges = "".join(
            [render_badge(tag, "tag") for tag in snippet.tags]
        )
        st.markdown(
            f'<div class="tag-container">{tag_badges}</div>', unsafe_allow_html=True
        )
