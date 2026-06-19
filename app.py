import streamlit as st
from typing import Literal

# Imports from modular packages
from db.connection import DatabaseManager
from db.repository import SQLSnippetRepository
from ui.styles import inject_custom_styles, load_themes_config, save_themes_config, DEFAULT_THEMES
from ui.dialogs import add_snippet_dialog
from ui.components import SnippetUIRenderer

# Page Configuration
st.set_page_config(
    page_title="Snippet Vault",
    page_icon="💾",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Inject CSS styles
inject_custom_styles()

# Initialize Database Manager & Repository
db_manager = DatabaseManager()
db_manager.init_db()
repository = SQLSnippetRepository(db_manager)

# Initialize UI Renderer
renderer = SnippetUIRenderer(repository)

# Application Header & Add Button
col_title, col_btn = st.columns([3, 1])
with col_title:
    st.title("💾 Snippet Vault")
    st.markdown("A minimal, self-hosted vault for organizing code snippets and terminal commands.")
with col_btn:
    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
    if st.button("➕ Add Snippet (Alt+N)", type="primary", use_container_width=True):
        # Open Dialog, injecting the dependency repository instance
        add_snippet_dialog(repository)

# Load Snippets Data
snippets = repository.get_all()

# Sidebar Configuration & Stats
with st.sidebar:
    st.header("⚙️ Settings")

    # View Mode toggle state (initialized here, controlled by main buttons)
    if "view_mode" not in st.session_state:
        st.session_state.view_mode = "Full Details"

    # Theme Settings configuration and management
    themes_config = load_themes_config()
    selected_theme = themes_config.get("selected_theme", "Nordic Dark (Default)")
    custom_themes = themes_config.get("custom_themes", {})
    
    st.markdown("---")
    st.header("🎨 Theme Settings")
    
    available_themes = list(DEFAULT_THEMES.keys()) + list(custom_themes.keys())
    if selected_theme not in available_themes:
        selected_theme = "Nordic Dark (Default)"
        
    theme_choice = st.selectbox(
        "Select Theme",
        options=available_themes + ["➕ Create Custom Theme..."],
        index=available_themes.index(selected_theme) if selected_theme in available_themes else 0
    )
    
    if theme_choice == "➕ Create Custom Theme...":
        st.markdown("### ➕ Custom Theme Creator")
        custom_name = st.text_input("Theme Name", placeholder="e.g. Lavender Dream").strip()
        
        # Use currently active theme colors as picker defaults
        active_colors = DEFAULT_THEMES.get(selected_theme, custom_themes.get(selected_theme, DEFAULT_THEMES["Nordic Dark (Default)"]))
        
        col_p, col_bg = st.columns(2)
        with col_p:
            c_primary = st.color_picker("Primary Color", active_colors["primary"])
        with col_bg:
            c_bg = st.color_picker("Background Color", active_colors["background"])
            
        col_sec, col_txt = st.columns(2)
        with col_sec:
            c_sec = st.color_picker("Card Background", active_colors["secondary_background"])
        with col_txt:
            c_txt = st.color_picker("Text Color", active_colors["text"])
            
        if st.button("Save & Apply Theme", type="primary", use_container_width=True):
            if not custom_name:
                st.error("Theme name cannot be empty.")
            elif custom_name in DEFAULT_THEMES or custom_name == "➕ Create Custom Theme...":
                st.error("Cannot overwrite predefined default themes.")
            else:
                custom_themes[custom_name] = {
                    "primary": c_primary,
                    "background": c_bg,
                    "secondary_background": c_sec,
                    "text": c_txt
                }
                save_themes_config(custom_name, custom_themes)
                st.success(f"Theme '{custom_name}' applied and saved!")
                st.rerun()
    else:
        if theme_choice != selected_theme:
            save_themes_config(theme_choice, custom_themes)
            st.rerun()
            
        if theme_choice in custom_themes:
            if st.button("🗑️ Delete Custom Theme", use_container_width=True):
                del custom_themes[theme_choice]
                save_themes_config("Nordic Dark (Default)", custom_themes)
                st.success(f"Theme '{theme_choice}' deleted!")
                st.rerun()

    st.markdown("---")
    st.header("📊 Vault Statistics")
    if snippets:
        st.metric("Total Items", len(snippets))
        st.metric("Code Snippets", len([s for s in snippets if s.type == "Code"]))
        st.metric("Terminal Commands", len([s for s in snippets if s.type == "Command"]))
    else:
        st.info("Your vault is empty.")

    st.markdown("---")
    st.markdown("### 💡 Formatting Guide")
    st.markdown(
        "You can use **Markdown** syntax in the description field to format text with "
        "**bold**, *italics*, `code blocks`, links, list bullets, or even tables."
    )

# Main Area - Search & Filtering
if not snippets:
    st.info("Your Snippet Vault is empty. Use the button at the top to add your first snippet or command!")
else:
    # View Layout Switcher (Main Toggle Buttons)
    view_col1, view_col2, view_spacer = st.columns([1.5, 1.5, 7])
    with view_col1:
        full_type: Literal["primary", "secondary"] = "primary" if st.session_state.view_mode == "Full Details" else "secondary"
        if st.button("📋 List View", type=full_type, use_container_width=True):
            st.session_state.view_mode = "Full Details"
            st.rerun()
    with view_col2:
        grid_type: Literal["primary", "secondary"] = "primary" if st.session_state.view_mode == "Compact Grid" else "secondary"
        if st.button("🗂️ Grid View", type=grid_type, use_container_width=True):
            st.session_state.view_mode = "Compact Grid"
            st.rerun()
            
    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

    # Search and Filter Bars - Two Rows for Centered Layout
    search_col, type_col = st.columns([3, 1])
    with search_col:
        search_query = st.text_input("🔍 Search snippets", placeholder="Search in titles, descriptions, categories, tags, or content...")
    with type_col:
        filter_type = st.selectbox("Type Filter", ["All", "Code", "Command"])
        
    cat_col, tag_col = st.columns(2)
    
    # Extract unique categories
    unique_cats = repository.get_existing_categories(snippets)
    with cat_col:
        filter_cat = st.selectbox("Category Filter", ["All"] + unique_cats)
        
    # Extract unique tags for tag filter
    all_tags = set()
    for s in snippets:
        for t in s.tags:
            all_tags.add(t)
    unique_tags = sorted(list(all_tags))
    with tag_col:
        filter_tags = st.multiselect("Tag Filter", options=unique_tags, placeholder="Select tags...")

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
            s for s in filtered_snippets if (
                q in s.title.lower() or
                (q in s.description.lower() if s.description else False) or
                any(q in t.lower() for t in s.tags) or
                q in s.category.lower() or
                q in s.content.lower()
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
        st.warning("No snippets match your filters. Try adjusting your search query or filters.")
    else:
        if st.session_state.view_mode == "Compact Grid":
            renderer.render_grid(filtered_snippets, unique_cats)
        else:
            renderer.render_list(filtered_snippets, unique_cats)

# Keyboard shortcut handler (Alt + N) to trigger the popup modal
st.iframe("""
<script>
    (function() {
        try {
            const parentWin = window.parent;
            const parentDoc = parentWin.document;
            
            if (parentWin.__shortcut_attached__) {
                return;
            }
            parentWin.__shortcut_attached__ = true;
            
            parentDoc.addEventListener('keydown', function(e) {
                try {
                    // Check if user is typing in a form input or text area
                    const active = parentDoc.activeElement;
                    if (active && (
                        active.tagName === 'INPUT' || 
                        active.tagName === 'TEXTAREA' || 
                        active.contentEditable === 'true' ||
                        active.closest('.stTextInput') ||
                        active.closest('.stTextArea')
                    )) {
                        return; 
                    }
                    
                    // Check for Alt+N keypress
                    if (e.altKey && (e.key === 'n' || e.key === 'N' || e.keyCode === 78)) {
                        e.preventDefault();
                        e.stopPropagation();
                        
                        const buttons = Array.from(parentDoc.querySelectorAll('button'));
                        const addBtn = buttons.find(btn => btn.textContent && btn.textContent.includes('Add Snippet'));
                        if (addBtn) {
                            addBtn.click();
                        }
                    }
                } catch (err) {
                    console.error("Error in shortcut keydown listener:", err);
                }
            }, true);
        } catch (e) {
            console.error("Failed to attach global keydown listener from iframe:", e);
        }
    })();
</script>
""", height=1)
