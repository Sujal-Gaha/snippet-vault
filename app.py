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
from utils.export import (
    export_to_json,
    export_to_csv,
    export_to_sql,
    export_to_markdown,
    export_to_zip,
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

# Sidebar Configuration & Stats
with st.sidebar:
    st.header("Dashboard & Settings")

    # Calculate statistics
    total_count = len(snippets)
    code_count = sum(1 for s in snippets if s.type == "Code")
    cmd_count = sum(1 for s in snippets if s.type == "Command")

    stat_col1, stat_col2, stat_col3 = st.columns(3)
    with stat_col1:
        st.metric("Total", total_count)
    with stat_col2:
        st.metric("Code", code_count)
    with stat_col3:
        st.metric("Commands", cmd_count)

    st.markdown("---")

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

    # Section 1: Themes & Shortcuts
    with st.expander("Theme & Keyboard Shortcuts", expanded=False):
        st.markdown(f"**Active Theme:** `{selected_theme}`")
        if render_button(
            "Open Theme Gallery",
            use_container_width=True,
            key="open_theme_gallery_sidebar_btn",
        ):
            st.session_state.show_theme_gallery = True
            st.rerun()

        st.markdown("---")
        st.markdown("### Active Shortcuts")
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

    # Section 2: Import & Export
    with st.expander("Backup & Restore", expanded=False):
        st.markdown("### Export Snippets")
        if snippets:
            export_format = render_selectbox(
                "Select Format",
                options=[
                    "JSON",
                    "CSV",
                    "SQL",
                    "Markdown (Single File)",
                    "Markdown (ZIP Archive)",
                ],
                key="export_format_select",
            )

            # Prepare export files
            if export_format == "JSON":
                data = export_to_json(snippets)
                mime = "application/json"
                filename = "snippets_export.json"
            elif export_format == "CSV":
                data = export_to_csv(snippets)
                mime = "text/csv"
                filename = "snippets_export.csv"
            elif export_format == "SQL":
                data = export_to_sql(snippets)
                mime = "application/sql"
                filename = "snippets_export.sql"
            elif export_format == "Markdown (Single File)":
                data = export_to_markdown(snippets)
                mime = "text/markdown"
                filename = "snippets_export.md"
            else:  # ZIP Archive
                data = export_to_zip(snippets)
                mime = "application/zip"
                filename = "snippets_export.zip"

            st.download_button(
                label=f"Download {export_format}",
                data=data,
                file_name=filename,
                mime=mime,
                use_container_width=True,
            )
        else:
            st.info("No snippets to export.")

        st.markdown("---")
        st.markdown("### Import SQL Backup")

        if "import_message" in st.session_state:
            msg_type, msg_text = st.session_state.pop("import_message")
            if msg_type == "success":
                st.success(msg_text)
            else:
                st.error(msg_text)

        uploaded_file = st.file_uploader(
            "Upload SQL Backup (.sql)",
            type=["sql"],
            key="import_sql_uploader",
            help="Upload a previously exported .sql file to restore or merge snippets.",
        )
        if uploaded_file is not None:
            if render_button(
                "Import SQL Backup",
                type="primary",
                use_container_width=True,
                key="run_import_backup_btn",
            ):
                try:
                    import re

                    sql_content = uploaded_file.read().decode("utf-8")
                    # Rewrite INSERT INTO to INSERT OR REPLACE INTO for resolving duplicates gracefully
                    sql_content = re.sub(
                        r"(?i)\bINSERT\s+INTO\s+snippets\b",
                        "INSERT OR REPLACE INTO snippets",
                        sql_content,
                    )

                    conn = db_manager.get_connection()
                    conn.executescript(sql_content)
                    conn.commit()
                    conn.close()
                    st.session_state.import_message = (
                        "success",
                        "Snippets imported successfully!",
                    )
                    st.rerun()
                except Exception as e:
                    st.session_state.import_message = (
                        "error",
                        f"Failed to import: {e}",
                    )
                    st.rerun()

    # Section 3: Danger Zone
    with st.expander("Danger Zone", expanded=False):
        confirm_clear = st.checkbox(
            "I want to delete all snippets",
            key="confirm_clear_checkbox",
            help="Check this box to enable the clear database button.",
        )
        if confirm_clear:
            if render_button(
                "Clear All Snippets",
                type="primary",
                use_container_width=True,
                key="clear_all_snippets_btn",
            ):
                repository.delete_all()
                st.session_state.toast_message = (
                    "All snippets have been deleted.",
                    "🗑️",
                )
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
                const eventCode = e.code ? e.code.toLowerCase() : '';
                
                let codeMatch = false;
                if (keyPart.length === 1) {{
                    if (keyPart >= 'a' && keyPart <= 'z') {{
                        codeMatch = (eventCode === 'key' + keyPart);
                    }} else if (keyPart >= '0' && keyPart <= '9') {{
                        codeMatch = (eventCode === 'digit' + keyPart);
                    }}
                }}
                
                // Common punctuation/special keys mappings
                if (keyPart === '/') codeMatch = codeMatch || (eventCode === 'slash');
                if (keyPart === 'space') codeMatch = codeMatch || (eventCode === 'space');
                if (keyPart === 'enter') codeMatch = codeMatch || (eventCode === 'enter');
                if (keyPart === 'escape') codeMatch = codeMatch || (eventCode === 'escape');
                
                return eventKey === keyPart || codeMatch;
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

# Floating Chatbot Widget (Coming Soon) - CSS-only Toggle (No JS required)
st.html("""
<style>
.chatbot-widget {
    position: fixed;
    bottom: 24px;
    right: 24px;
    z-index: 999999;
}

.chatbot-head {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background-color: var(--primary);
    color: var(--primary-foreground);
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.chatbot-head:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
}

.chatbot-head:active {
    transform: scale(0.95);
}

.chatbot-head .close-icon {
    display: none;
}

.chatbot-head .chat-icon {
    display: block;
}

.chatbot-window {
    position: absolute;
    bottom: 72px;
    right: 0;
    width: 320px;
    height: 380px;
    background-color: var(--card);
    border: var(--border-width) solid var(--border);
    border-radius: var(--radius);
    box-shadow: var(--shadow-2xl);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    opacity: 0;
    transform: translateY(20px) scale(0.95);
    pointer-events: none;
    transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* Sibling toggling rules using CSS checkbox hack */
#chatbot-toggle-checkbox:checked ~ .chatbot-window {
    opacity: 1 !important;
    transform: translateY(0) scale(1) !important;
    pointer-events: auto !important;
}

#chatbot-toggle-checkbox:checked ~ .chatbot-head .chat-icon {
    display: none !important;
}

#chatbot-toggle-checkbox:checked ~ .chatbot-head .close-icon {
    display: block !important;
}

.chatbot-header {
    padding: 12px 16px;
    background-color: var(--secondary);
    border-bottom: var(--border-width) solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.chatbot-title-container {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.chatbot-title {
    font-weight: 600;
    font-size: 14px;
    color: var(--foreground);
}

.chatbot-badge {
    align-self: flex-start;
    font-size: 8px;
    font-weight: 700;
    text-transform: uppercase;
    background-color: var(--primary);
    color: var(--primary-foreground);
    padding: 1px 5px;
    border-radius: 99px;
    letter-spacing: 0.5px;
}

.chatbot-close-btn {
    background: none;
    border: none;
    font-size: 18px;
    color: var(--muted-foreground);
    cursor: pointer;
    padding: 0;
    transition: color 0.2s;
}

.chatbot-close-btn:hover {
    color: var(--foreground);
}

.chatbot-content {
    padding: 12px 16px;
    display: flex;
    flex-direction: column;
    height: calc(100% - 50px);
    overflow: hidden;
}

.chatbot-desc {
    font-size: 12px;
    line-height: 1.4;
    color: var(--muted-foreground);
    margin-bottom: 12px;
}

.chat-messages {
    flex-grow: 1;
    overflow-y: auto;
    margin-bottom: 12px;
    display: flex;
    flex-direction: column;
}

.chat-message {
    display: flex;
    gap: 8px;
    align-items: flex-start;
}

.chat-message.assistant .avatar {
    font-size: 14px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background-color: var(--secondary);
    display: flex;
    align-items: center;
    justify-content: center;
    border: var(--border-width) solid var(--border);
}

.chat-message.assistant .message-bubble {
    background-color: var(--secondary);
    color: var(--foreground);
    font-size: 12px;
    line-height: 1.4;
    padding: 8px 10px;
    border-radius: 0 var(--radius) var(--radius) var(--radius);
    border: var(--border-width) solid var(--border);
}

.chat-input-container {
    display: flex;
    gap: 6px;
    border: var(--border-width) solid var(--border);
    background-color: var(--background);
    padding: 2px 8px;
    border-radius: var(--radius);
    align-items: center;
}

.chat-input {
    flex-grow: 1;
    background: none;
    border: none;
    outline: none;
    font-size: 12px;
    color: var(--foreground);
    padding: 4px 0;
}

.chat-input::placeholder {
    color: var(--muted-foreground);
}

.chat-send-btn {
    background: none;
    border: none;
    color: var(--muted-foreground);
    cursor: not-allowed;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2px;
}
</style>

<div class="chatbot-widget">
    <!-- Hidden Checkbox for CSS-only Toggle -->
    <input type="checkbox" id="chatbot-toggle-checkbox" style="display: none;">

    <!-- Floating Chat Head -->
    <label class="chatbot-head" for="chatbot-toggle-checkbox">
        <!-- Chat Icon -->
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="chat-icon">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
        <!-- Close Icon -->
        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="close-icon">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
        </svg>
    </label>

    <!-- Chat Window -->
    <div class="chatbot-window" id="chatbot-window">
        <div class="chatbot-header">
            <div class="chatbot-title-container">
                <span class="chatbot-title">💬 AI Copilot</span>
                <span class="chatbot-badge">Coming Soon</span>
            </div>
            <label class="chatbot-close-btn" for="chatbot-toggle-checkbox">×</label>
        </div>
        <div class="chatbot-content">
            <div class="chatbot-desc">
                An intelligent AI assistant designed to help you instantly search, explain, and write snippets or commands using natural language.
            </div>
            <div class="chat-messages">
                <div class="chat-message assistant">
                    <div class="avatar">🤖</div>
                    <div class="message-bubble">
                        Hello! I am your future AI assistant. Soon you will be able to ask me to find snippets, explain code, or write commands for you!
                    </div>
                </div>
            </div>
            <div class="chat-input-container">
                <input type="text" class="chat-input" placeholder="Ask for a snippet..." disabled>
                <button class="chat-send-btn" disabled>
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                    </svg>
                </button>
            </div>
        </div>
    </div>
</div>
""")
