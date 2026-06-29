import streamlit as st
from db.repository import BaseSnippetRepository
from db.models import Snippet
from utils.helpers import format_date
from ui.components.badge import render_badge
from ui.components.button import render_button
from ui.components.input import render_text_input, render_text_area, render_selectbox
from ui.styles import (
    DEFAULT_THEMES,
    load_themes_config,
    save_themes_config,
)


@st.dialog("Add New Snippet / Command", width="small")
def add_snippet_dialog(repository: BaseSnippetRepository):
    # Fetch fresh list for category selectbox
    snippets = repository.get_all()
    existing_cats = repository.get_existing_categories(snippets)

    title = render_text_input(
        "Title", placeholder="e.g. Docker Clean Containers", max_chars=100
    )

    snippet_type = st.radio("Type", ["Code", "Command"], horizontal=True)

    language = render_selectbox(
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

    content = render_text_area(
        "Snippet / Command",
        placeholder="Paste code or command line here...",
        height=150,
    )
    description = render_text_area(
        "Description (supports Markdown)",
        placeholder="What does this do? Supports **bold**, *italics*, `code`, lists, tables, links...",
        height=100,
    )

    # Category selection & creation
    cat_col1, cat_col2 = st.columns(2)
    with cat_col1:
        cat_sel = render_selectbox(
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
        cat_new = render_text_input(
            "Or Create New Category",
            placeholder="e.g. Databases, Docker, Git",
            help="Type to create and assign a new category (overrides selection)",
        )

    tags = render_text_input(
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


@st.dialog("Edit Snippet / Command", width="small")
def edit_snippet_dialog(repository: BaseSnippetRepository, snippet: Snippet):
    # Fetch fresh list for category selectbox
    snippets = repository.get_all()
    existing_cats = repository.get_existing_categories(snippets)

    title = render_text_input(
        "Title",
        value=snippet.title,
        placeholder="e.g. Docker Clean Containers",
        max_chars=100,
        key=f"edit_title_{snippet.id}",
    )

    type_options = ["Code", "Command"]
    type_index = type_options.index(snippet.type) if snippet.type in type_options else 0
    snippet_type = st.radio(
        "Type",
        type_options,
        index=type_index,
        horizontal=True,
        key=f"edit_type_{snippet.id}",
    )

    lang_options = (
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
    )
    lang_index = (
        lang_options.index(snippet.language) if snippet.language in lang_options else 0
    )
    language = render_selectbox(
        "Syntax Highlighting",
        options=lang_options,
        index=lang_index,
        key=f"edit_lang_{snippet.id}",
    )

    content = render_text_area(
        "Snippet / Command",
        value=snippet.content,
        placeholder="Paste code or command line here...",
        height=150,
        key=f"edit_content_{snippet.id}",
    )
    description = render_text_area(
        "Description (supports Markdown)",
        value=snippet.description or "",
        placeholder="What does this do? Supports **bold**, *italics*, `code`, lists, tables, links...",
        height=100,
        key=f"edit_desc_{snippet.id}",
    )

    # Category selection & creation
    cat_col1, cat_col2 = st.columns(2)
    with cat_col1:
        cat_index = (
            existing_cats.index(snippet.category)
            if snippet.category in existing_cats
            else (
                existing_cats.index("Uncategorized")
                if "Uncategorized" in existing_cats
                else 0
            )
        )
        cat_sel = render_selectbox(
            "Assign Category",
            options=existing_cats,
            index=cat_index,
            help="Select an existing category from the dropdown",
            key=f"edit_cat_sel_{snippet.id}",
        )
    with cat_col2:
        cat_new = render_text_input(
            "Or Create New Category",
            placeholder="e.g. Databases, Docker, Git",
            help="Type to create and assign a new category (overrides selection)",
            key=f"edit_cat_new_{snippet.id}",
        )

    tags = render_text_input(
        "Tags (comma-separated)",
        value=snippet.tags_csv,
        placeholder="e.g. docker, devops, cleanup",
        key=f"edit_tags_{snippet.id}",
    )

    col1, col2, col3 = st.columns([1.2, 1.2, 3])
    with col1:
        if render_button(
            "Save Changes",
            type="primary",
            use_container_width=True,
            key=f"edit_save_{snippet.id}",
        ):
            if not title.strip():
                st.error("Please enter a title.")
            elif not content.strip():
                st.error("Please enter snippet/command content.")
            else:
                final_cat = cat_new.strip() if cat_new.strip() else cat_sel
                if not final_cat:
                    final_cat = "Uncategorized"

                # Update snippet properties and save
                snippet.title = title.strip()
                snippet.content = content.strip()
                snippet.description = description.strip()
                snippet.tags = [t.strip() for t in tags.split(",") if t.strip()]
                snippet.type = snippet_type
                snippet.language = language
                snippet.category = final_cat

                repository.update(snippet)
                st.success("Changes saved!")
                st.rerun()
    with col2:
        if render_button(
            "Cancel", use_container_width=True, key=f"edit_cancel_{snippet.id}"
        ):
            st.rerun()


@st.dialog("Snippet Details", width="large")
def view_snippet_dialog(snippet: Snippet):
    badge_type = "code" if snippet.type == "Code" else "command"
    badge_html = render_badge(snippet.type, badge_type)
    cat_html = render_badge(snippet.category, "category")

    st.markdown(
        f"<div>" f"{badge_html}" f"{cat_html}" f"</div>",
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
        tag_badges = "".join([render_badge(tag, "tag") for tag in snippet.tags])
        st.markdown(
            f'<div class="tag-container">{tag_badges}</div>', unsafe_allow_html=True
        )


def _get_valid_hex(color_str: str, fallback: str) -> str:
    if color_str and color_str.startswith("#"):
        val = color_str[1:]
        if len(val) in (3, 6, 4, 8) and all(c in "0123456789abcdefABCDEF" for c in val):
            if len(val) == 4:
                return "#" + val[:3]
            elif len(val) == 8:
                return "#" + val[:6]
            return color_str
    return fallback


def reset_theme_gallery():
    st.session_state.show_theme_gallery = False


@st.dialog("Theme Gallery", width="medium", on_dismiss=reset_theme_gallery)
def theme_gallery_dialog(settings_repo):
    themes_config = load_themes_config(settings_repo)
    selected_theme = themes_config.get("selected_theme", "Nordic Dark")
    custom_themes = themes_config.get("custom_themes", {})

    # Sync session state variable for active theme inside dialog
    if (
        "temp_theme" not in st.session_state
        or st.session_state.temp_theme != selected_theme
    ):
        st.session_state.temp_theme = selected_theme

    # Inject custom styles for the gallery cards and overlay buttons
    st.markdown(
        """
        <style>
        /* Make the immediate parent vertical block relative so overlay buttons align correctly */
        div:has(> div[class*="st-key-theme_select_"]),
        div:has(> div[class*="st-key-custom_select_"]) {
            position: relative !important;
            max-width: 100px !important;
            margin: 0 auto !important;
        }
        
        /* Selection overlay button wrapper */
        div[class*="st-key-theme_select_"],
        div[class*="st-key-custom_select_"] {
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            z-index: 10 !important;
        }
        
        /* Make select buttons transparent and fill the card container */
        div[class*="st-key-theme_select_"] button,
        div[class*="st-key-custom_select_"] button {
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 100% !important;
            opacity: 0 !important;
            cursor: pointer !important;
            border: none !important;
            background: transparent !important;
            padding: 0 !important;
            margin: 0 !important;
        }
        
        div[class*="st-key-theme_select_"] button:focus,
        div[class*="st-key-custom_select_"] button:focus,
        div[class*="st-key-theme_select_"] button:active,
        div[class*="st-key-custom_select_"] button:active {
            box-shadow: none !important;
            outline: none !important;
            background: transparent !important;
        }
        
        /* Floating delete button wrapper at top-right */
        div[class*="st-key-custom_delete_"] {
            position: absolute !important;
            top: 4px !important;
            right: 4px !important;
            width: 18px !important;
            height: 18px !important;
            margin: 0 !important;
            padding: 0 !important;
            z-index: 20 !important;
        }
        
        /* Style the delete button to look like a small floating circle */
        div[class*="st-key-custom_delete_"] button {
            width: 18px !important;
            height: 18px !important;
            min-height: 18px !important;
            max-height: 18px !important;
            min-width: 18px !important;
            max-width: 18px !important;
            padding: 0 !important;
            margin: 0 !important;
            font-size: 8px !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            background-color: rgba(255, 75, 75, 0.15) !important;
            color: #ff4b4b !important;
            border: 1px solid rgba(255, 75, 75, 0.25) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.15) !important;
        }
        
        div[class*="st-key-custom_delete_"] button:hover {
            background-color: #ff4b4b !important;
            color: white !important;
            border-color: #ff4b4b !important;
            transform: scale(1.1);
        }

        /* Hover animation for custom theme cards */
        .theme-card-wrapper {
            position: relative;
            transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.2s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            border-radius: 10px;
        }
        
        /* Hover animation triggered when hovering over the relative parent container */
        div:has(> div[class*="st-key-theme_select_"]):hover .theme-card-wrapper,
        div:has(> div[class*="st-key-custom_select_"]):hover .theme-card-wrapper {
            transform: translateY(-3px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    def _sanitize_key(val: str) -> str:
        return "".join(c if c.isalnum() else "_" for c in val)

    def render_theme_card(name, theme):
        is_active = name == st.session_state.temp_theme

        # Calculate dynamic borders/shadows
        text_color = theme.get("text", "#eceff4")
        bg_color = theme.get("background", "#2e3440")
        sec_bg = theme.get("secondary_background", "#3b4252")
        primary_color = theme.get("primary", "#88c0d0")

        border_color = (
            primary_color
            if is_active
            else theme.get("border", "rgba(128, 128, 128, 0.2)")
        )
        box_shadow = (
            f"0 0 15px {primary_color}50, 0 4px 6px rgba(0, 0, 0, 0.15)"
            if is_active
            else "0 2px 4px rgba(0, 0, 0, 0.1)"
        )

        st.markdown(
            f"""
            <div class="theme-card-wrapper" style="
                border: 2px solid {border_color};
                border-radius: 10px;
                padding: 6px;
                margin-bottom: 12px;
                max-width: 100px;
                background-color: {sec_bg};
                box-shadow: {box_shadow};
            ">
                <!-- Theme Demo Mockup -->
                <div style="
                    background-color: {bg_color};
                    border-radius: 6px;
                    padding: 4px;
                    height: 50px;
                    display: flex;
                    flex-direction: column;
                    gap: 3px;
                    border: 1px solid rgba(128, 128, 128, 0.15);
                    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.15);
                ">
                    <!-- Header row -->
                    <div style="
                        display: flex;
                        justify-content: space-between;
                        align-items: center;
                        background-color: {sec_bg};
                        padding: 1px 4px;
                        border-radius: 3px;
                        height: 10px;
                    ">
                        <div style="display: flex; gap: 2px;">
                            <div style="width: 3px; height: 3px; border-radius: 50%; background-color: {primary_color};"></div>
                            <div style="width: 3px; height: 3px; border-radius: 50%; background-color: {text_color}; opacity: 0.5;"></div>
                        </div>
                        <div style="width: 15px; height: 2px; border-radius: 0.5px; background-color: {text_color}; opacity: 0.3;"></div>
                    </div>
                    <!-- Body row -->
                    <div style="
                        display: flex;
                        gap: 3px;
                        flex: 1;
                    ">
                        <!-- Sidebar Panel -->
                        <div style="
                            width: 35%;
                            background-color: {sec_bg};
                            border-radius: 3px;
                            padding: 2px;
                            display: flex;
                            flex-direction: column;
                            gap: 2px;
                        ">
                            <div style="width: 100%; height: 2px; background-color: {text_color}; opacity: 0.4; border-radius: 0.5px;"></div>
                            <div style="width: 80%; height: 2px; background-color: {text_color}; opacity: 0.3; border-radius: 0.5px;"></div>
                        </div>
                        <!-- Main Content Area -->
                        <div style="
                            width: 65%;
                            background-color: {sec_bg};
                            border-radius: 3px;
                            padding: 3px;
                            border: 1px solid {primary_color};
                            display: flex;
                            flex-direction: column;
                            gap: 2px;
                        ">
                            <div style="width: 100%; height: 3px; background-color: {primary_color}; opacity: 0.8; border-radius: 0.5px;"></div>
                            <div style="display: flex; flex-direction: column; gap: 1px;">
                                <div style="width: 90%; height: 1.5px; background-color: {text_color}; opacity: 0.6; border-radius: 0.5px;"></div>
                                <div style="width: 70%; height: 1.5px; background-color: {text_color}; opacity: 0.4; border-radius: 0.5px;"></div>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Theme Name -->
                <div style="
                    text-align: center;
                    font-size: 10px;
                    font-weight: 600;
                    color: {text_color};
                    margin-top: 6px;
                    overflow: hidden;
                    text-overflow: ellipsis;
                    white-space: nowrap;
                ">
                    {name}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    tab1, tab2 = st.tabs(["Themes", "Custom Themes"])

    with tab1:
        st.markdown("### Predefined Themes")
        # Grid of default themes
        available_defaults = list(DEFAULT_THEMES.keys())
        # Display 6 themes per row
        cols = st.columns(6)
        for idx, name in enumerate(available_defaults):
            theme = DEFAULT_THEMES[name]
            col = cols[idx % 6]
            with col:
                with st.container():
                    render_theme_card(name, theme)

                    # Hidden overlay select button
                    if st.button(
                        f"Select {name}",
                        key=f"theme_select_{_sanitize_key(name)}",
                        use_container_width=True,
                    ):
                        save_themes_config(settings_repo, name, custom_themes)
                        st.session_state.temp_theme = name
                        st.toast(f"Theme '{name}' applied!")
                        st.rerun()

    with tab2:
        st.markdown("### Existing Custom Themes")
        if not custom_themes:
            st.info("No custom themes created yet. Use the creator below to build one!")
        else:
            available_custom = list(custom_themes.keys())
            cols = st.columns(6)
            for idx, name in enumerate(available_custom):
                theme = custom_themes[name]
                col = cols[idx % 6]
                with col:
                    with st.container():
                        render_theme_card(name, theme)

                        is_active = name == st.session_state.temp_theme

                        # Hidden overlay select button
                        if st.button(
                            f"Select {name}",
                            key=f"custom_select_{_sanitize_key(name)}",
                            use_container_width=True,
                        ):
                            save_themes_config(settings_repo, name, custom_themes)
                            st.session_state.temp_theme = name
                            st.toast(f"Theme '{name}' applied!")
                            st.rerun()

                        # Floating delete button
                        if st.button(
                            "🗑️",
                            key=f"custom_delete_{_sanitize_key(name)}",
                            use_container_width=True,
                            help="Delete theme",
                        ):
                            del custom_themes[name]
                            new_sel = (
                                "Nordic Dark"
                                if is_active
                                else st.session_state.temp_theme
                            )
                            save_themes_config(settings_repo, new_sel, custom_themes)
                            st.session_state.temp_theme = new_sel
                            st.toast(f"Theme '{name}' deleted!")
                            st.rerun()

        st.markdown("---")
        st.markdown("### Create Custom Theme")
        custom_name = render_text_input(
            "Theme Name",
            placeholder="e.g. Lavender Dream",
            key="custom_theme_name_input",
        ).strip()

        active_colors = (
            DEFAULT_THEMES.get(
                st.session_state.temp_theme,
                custom_themes.get(
                    st.session_state.temp_theme, DEFAULT_THEMES["Nordic Dark"]
                ),
            )
            or DEFAULT_THEMES["Nordic Dark"]
        )

        c_primary = st.color_picker(
            "Primary Color",
            _get_valid_hex(active_colors.get("primary", ""), "#88c0d0"),
            key="picker_primary",
        )
        c_bg = st.color_picker(
            "Background Color",
            _get_valid_hex(active_colors.get("background", ""), "#2e3440"),
            key="picker_bg",
        )
        c_sec = st.color_picker(
            "Card Background",
            _get_valid_hex(active_colors.get("secondary_background", ""), "#3b4252"),
            key="picker_sec",
        )
        c_txt = st.color_picker(
            "Text Color",
            _get_valid_hex(active_colors.get("text", ""), "#eceff4"),
            key="picker_txt",
        )

        if render_button(
            "Save & Apply Theme",
            type="primary",
            key="save_custom_theme_btn",
            use_container_width=True,
        ):
            if not custom_name:
                st.error("Theme name cannot be empty.")
            elif (
                custom_name in DEFAULT_THEMES or custom_name == "Create Custom Theme..."
            ):
                st.error("Cannot overwrite predefined default themes.")
            else:
                custom_themes[custom_name] = {
                    "primary": c_primary,
                    "background": c_bg,
                    "secondary_background": c_sec,
                    "text": c_txt,
                }
                save_themes_config(settings_repo, custom_name, custom_themes)
                st.session_state.temp_theme = custom_name
                st.toast(f"Theme '{custom_name}' applied and saved!")
                st.rerun()


@st.dialog("Keyboard Shortcuts", width="medium")
def shortcuts_dialog(settings_repo):
    import json
    from ui.styles import get_keyboard_shortcuts, DEFAULT_KEYBOARD_SHORTCUTS

    st.markdown(
        "Customize keyboard shortcuts. Refresh the page to apply new bindings. Keyboard combinations must be formatted like: `Alt+N`, `Ctrl+Shift+A`, `Alt+/` etc."
    )

    shortcuts = get_keyboard_shortcuts(settings_repo)

    st.write("---")

    col_labels, col_inputs = st.columns([1.8, 1.2])
    new_shortcuts = {}

    # 1. Add Snippet Shortcut
    with col_labels:
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown("**Add New Snippet**")
    with col_inputs:
        new_shortcuts["add_snippet"] = render_text_input(
            "Add Snippet Key",
            value=shortcuts.get("add_snippet", "Alt+N"),
            label_visibility="collapsed",
            key="shortcut_add_snippet",
        )

    # 2. Toggle Sidebar Shortcut
    with col_labels:
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown("**Toggle Sidebar**")
    with col_inputs:
        new_shortcuts["toggle_sidebar"] = render_text_input(
            "Toggle Sidebar Key",
            value=shortcuts.get("toggle_sidebar", "Alt+S"),
            label_visibility="collapsed",
            key="shortcut_toggle_sidebar",
        )

    # 3. Show Shortcuts Shortcut
    with col_labels:
        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        st.markdown("**Show Keyboard Shortcuts Dialog**")
    with col_inputs:
        new_shortcuts["show_shortcuts"] = render_text_input(
            "Show Shortcuts Key",
            value=shortcuts.get("show_shortcuts", "Alt+/"),
            label_visibility="collapsed",
            key="shortcut_show_shortcuts",
        )

    st.write("---")
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        if render_button(
            "Save Shortcuts",
            type="primary",
            use_container_width=True,
            key="save_shortcuts_btn",
        ):
            valid = True
            for k, v in new_shortcuts.items():
                if not v.strip():
                    st.error(f"Shortcut key combo cannot be empty.")
                    valid = False
                    break
            if valid:
                settings_repo.set(
                    "keyboard_shortcuts",
                    json.dumps({k: v.strip() for k, v in new_shortcuts.items()}),
                )
                st.success("Shortcuts saved! Rerunning...")
                st.rerun()
    with btn_col2:
        if render_button(
            "Reset to Defaults",
            type="secondary",
            use_container_width=True,
            key="reset_shortcuts_btn",
        ):
            settings_repo.set(
                "keyboard_shortcuts", json.dumps(DEFAULT_KEYBOARD_SHORTCUTS)
            )
            st.success("Shortcuts reset to defaults! Rerunning...")
            st.rerun()
