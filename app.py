import json
import streamlit as st
from typing import Literal

# Imports from modular packages
from db.connection import DatabaseManager
from db.repository import SQLSnippetRepository, SQLSettingsRepository
from ui.styles import (
    inject_custom_styles,
    load_themes_config,
    get_keyboard_shortcuts,
)
from ui.components import (
    SnippetUIRenderer,
    render_button,
    render_text_input,
    render_selectbox,
    add_snippet_dialog,
    theme_gallery_dialog,
    shortcuts_dialog,
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

# Sidebar Configuration & Stats
with st.sidebar:
    st.header("Settings")

    # View Mode toggle state (initialized here, controlled by main buttons)
    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "Full Details"

    if "show_theme_gallery" not in st.session_state:
        st.session_state.show_theme_gallery = False

    if "show_shortcuts" not in st.session_state:
        st.session_state.show_shortcuts = False

    # Theme Settings configuration and management
    themes_config = load_themes_config(settings_repository)
    selected_theme = themes_config.get("selected_theme", "Nordic Dark")

    st.markdown("---")
    st.header("Theme Settings")
    st.markdown(f"**Active Theme:** `{selected_theme}`")
    if render_button("Open Theme Gallery", use_container_width=True):
        st.session_state.show_theme_gallery = True
        st.rerun()

    st.markdown("---")
    st.markdown("### Keyboard Shortcuts")
    st.markdown(
        f"- **`{shortcuts.get('add_snippet', 'Alt+N')}`**: Add new snippet\n"
        f"- **`{shortcuts.get('toggle_sidebar', 'Alt+S')}`**: Toggle sidebar\n"
        f"- **`{shortcuts.get('show_shortcuts', 'Alt+/')}`**: Shortcuts guide & settings"
    )
    if render_button(
        "Configure Shortcuts",
        use_container_width=True,
        key="config_shortcuts_sidebar_btn",
    ):
        st.session_state.show_shortcuts = True
        st.rerun()

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
st.iframe(
    f"""
<script>
    (function() {{
        try {{
            const parentWin = window.parent;
            const parentDoc = parentWin.document;
            
            // Always update shortcuts config in the parent window namespace
            parentWin.__shortcuts_config__ = {json.dumps(shortcuts)};
            
            if (parentWin.__shortcut_attached__) {{
                return;
            }}
            parentWin.__shortcut_attached__ = true;
            
            function matchShortcut(e, shortcutStr) {{
                if (!shortcutStr) return false;
                const parts = shortcutStr.split('+').map(p => p.trim().toLowerCase());
                const hasAlt = parts.includes('alt');
                const hasCtrl = parts.includes('ctrl');
                const hasShift = parts.includes('shift');
                
                const keyPart = parts.find(p => p !== 'alt' && p !== 'ctrl' && p !== 'shift');
                if (!keyPart) return false;
                
                if (e.altKey !== hasAlt) return false;
                if (e.ctrlKey !== hasCtrl) return false;
                if (e.shiftKey !== hasShift) return false;
                
                const eventKey = e.key ? e.key.toLowerCase() : '';
                return eventKey === keyPart;
            }}
            
            parentDoc.addEventListener('keydown', function(e) {{
                try {{
                    // Check if user is typing in a form input or text area
                    const active = parentDoc.activeElement;
                    if (active && (
                        active.tagName === 'INPUT' || 
                        active.tagName === 'TEXTAREA' || 
                        active.contentEditable === 'true' ||
                        active.closest('.stTextInput') ||
                        active.closest('.stTextArea')
                    )) {{
                        return; 
                    }}
                    
                    const currentShortcuts = parentWin.__shortcuts_config__ || {{}};
                    
                    // 1. Add Snippet Shortcut
                    if (matchShortcut(e, currentShortcuts.add_snippet)) {{
                        e.preventDefault();
                        e.stopPropagation();
                        
                        const buttons = Array.from(parentDoc.querySelectorAll('button'));
                        const addBtn = buttons.find(btn => btn.textContent && btn.textContent.includes('Add Snippet'));
                        if (addBtn) {{
                            addBtn.click();
                        }}
                    }}
                    
                    // 2. Toggle Sidebar Shortcut
                    if (matchShortcut(e, currentShortcuts.toggle_sidebar)) {{
                        e.preventDefault();
                        e.stopPropagation();
                        
                        const expandBtn = parentDoc.querySelector('[data-testid="collapsedControl"]') || 
                                          parentDoc.querySelector('button[aria-label="Expand sidebar"]');
                        if (expandBtn) {{
                            expandBtn.click();
                        }} else {{
                            const collapseBtn = parentDoc.querySelector('[data-testid="stSidebarCollapseButton"]') || 
                                                parentDoc.querySelector('button[aria-label="Collapse sidebar"]');
                            if (collapseBtn) {{
                                const actualBtn = collapseBtn.tagName === 'BUTTON' ? collapseBtn : collapseBtn.querySelector('button');
                                if (actualBtn) {{
                                    actualBtn.click();
                                }} else {{
                                    collapseBtn.click();
                                }}
                            }}
                        }}
                    }}
                    
                    // 3. Show Shortcuts Shortcut
                    if (matchShortcut(e, currentShortcuts.show_shortcuts)) {{
                        e.preventDefault();
                        e.stopPropagation();
                        
                        const buttons = Array.from(parentDoc.querySelectorAll('button'));
                        const configBtn = buttons.find(btn => btn.textContent && btn.textContent.includes('Configure Shortcuts'));
                        if (configBtn) {{
                            configBtn.click();
                        }}
                    }}
                }} catch (err) {{
                    console.error("Error in shortcut keydown listener:", err);
                }}
            }}, true);
        }} catch (e) {{
            console.error("Failed to attach global keydown listener from iframe:", e);
        }}
    }})();
</script>
""",
    height=1,
)
