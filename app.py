import streamlit as st
from typing import Literal

# Imports from modular packages
from db.connection import DatabaseManager
from db.repository import SQLSnippetRepository, SQLSettingsRepository
from ui.styles import (
    inject_custom_styles,
    get_keyboard_shortcuts,
    inject_keyboard_shortcuts,
)
from ui.components import (
    SnippetUIRenderer,
    render_button,
    render_text_input,
    render_selectbox,
    add_snippet_dialog,
    theme_gallery_dialog,
    shortcuts_dialog,
    render_sidebar,
    render_chatbot_widget,
)

# Page Configuration
st.set_page_config(
    page_title="Snippet Vault", layout="centered", initial_sidebar_state="expanded"
)

# Initialize Database Manager & Repositories
db_manager = DatabaseManager()
db_manager.init_db()
settings_repository = SQLSettingsRepository(db_manager)
repository = SQLSnippetRepository(db_manager)

# Display any deferred toasts from session state
if "toast_message" in st.session_state:
    msg, icon = st.session_state.pop("toast_message")
    st.toast(msg, icon=icon)

# Load data and keyboard shortcuts early
snippets = repository.get_all()
shortcuts = get_keyboard_shortcuts(settings_repository)

# Inject CSS styles (using database preferences)
inject_custom_styles(settings_repository)

# Initialize UI Renderer
renderer = SnippetUIRenderer(repository)

# Application Header & Add Button
col_title, col_btn = st.columns([3, 1])
with col_title:
    st.title("Snippet Vault")
    st.markdown(
        "A minimal, self-hosted vault for organizing code snippets and terminal commands."
    )
with col_btn:
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    add_shortcut = shortcuts.get("add_snippet", "Alt+N")
    if render_button(
        f"Add Snippet ({add_shortcut})", type="primary", use_container_width=True
    ):
        # Open Dialog, injecting the dependency repository instance
        add_snippet_dialog(repository)

# Sidebar Configuration, Statistics & Settings
with st.sidebar:
    render_sidebar(repository, settings_repository, snippets, shortcuts, db_manager)

# Main Area - Search & Filtering
if not snippets:
    st.info(
        "Your Snippet Vault is empty. Use the button at the top to add your first snippet or command!"
    )
else:
    # View Layout Switcher (Main Toggle Buttons)
    view_col1, view_col2, view_spacer = st.columns([1.5, 1.5, 7])
    with view_col1:
        full_type: Literal["primary", "secondary"] = (
            "primary" if st.session_state.view_mode == "Full Details" else "secondary"
        )
        if render_button("List View", type=full_type, use_container_width=True):
            st.session_state.view_mode = "Full Details"
            st.rerun()
    with view_col2:
        grid_type: Literal["primary", "secondary"] = (
            "primary" if st.session_state.view_mode == "Compact Grid" else "secondary"
        )
        if render_button("Grid View", type=grid_type, use_container_width=True):
            st.session_state.view_mode = "Compact Grid"
            st.rerun()

    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

    # Search and Filter Bars - Two Rows for Centered Layout
    search_col, type_col = st.columns([3, 1])
    with search_col:
        search_query = render_text_input(
            "Search snippets",
            placeholder="Search in titles, descriptions, categories, tags, or content...",
        )
    with type_col:
        filter_type = render_selectbox("Type Filter", ["All", "Code", "Command"])

    cat_col, tag_col = st.columns(2)

    # Extract unique categories
    unique_cats = repository.get_existing_categories(snippets)
    with cat_col:
        filter_cat = render_selectbox("Category Filter", ["All"] + unique_cats)

    # Extract unique tags for tag filter
    all_tags = set()
    for s in snippets:
        for t in s.tags:
            all_tags.add(t)
    unique_tags = sorted(list(all_tags))
    with tag_col:
        filter_tags = st.multiselect(
            "Tag Filter", options=unique_tags, placeholder="Select tags..."
        )

    # Apply filters
    filtered_snippets = snippets

    # 1. Type Filter
    if filter_type != "All":
        filtered_snippets = [s for s in filtered_snippets if s.type == filter_type]

    # 2. Category Filter
    if filter_cat != "All":
        filtered_snippets = [s for s in filtered_snippets if s.category == filter_cat]

    # 3. Search Query Filter
    if search_query:
        q = search_query.lower()
        filtered_snippets = [
            s
            for s in filtered_snippets
            if (
                q in s.title.lower()
                or (q in s.description.lower() if s.description else False)
                or any(q in t.lower() for t in s.tags)
                or q in s.category.lower()
                or q in s.content.lower()
            )
        ]

    # 4. Tag Filter
    if filter_tags:
        # Check if the snippet contains ALL selected filter tags
        filtered_snippets = [
            s for s in filtered_snippets if set(filter_tags).issubset(set(s.tags))
        ]

    # Display results
    if not filtered_snippets:
        st.warning(
            "No snippets match your filters. Try adjusting your search query or filters."
        )
    else:
        if st.session_state.view_mode == "Compact Grid":
            renderer.render_grid(filtered_snippets, unique_cats)
        else:
            renderer.render_list(filtered_snippets, unique_cats)

# Show theme gallery dialog if requested
if st.session_state.get("show_theme_gallery", False):
    theme_gallery_dialog(settings_repository)

# Show shortcuts configuration dialog if requested
if st.session_state.get("show_shortcuts", False):
    st.session_state.show_shortcuts = False
    shortcuts_dialog(settings_repository)

# Keyboard shortcut handler using dynamic database settings
inject_keyboard_shortcuts(shortcuts)

# Floating Chatbot Widget (Coming Soon)
render_chatbot_widget()
