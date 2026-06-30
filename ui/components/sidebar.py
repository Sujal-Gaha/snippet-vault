import streamlit as st
from ui.styles import load_themes_config
from ui.components import render_button, render_selectbox
from utils.export import (
    export_to_json,
    export_to_csv,
    export_to_sql,
    export_to_markdown,
    export_to_zip,
)


def render_sidebar(repository, settings_repository, snippets, shortcuts, db_manager):
    """Renders the settings, statistics, and preferences sidebar area."""
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
            f"- **`{shortcuts.get('toggle_chatbot', 'Alt+C')}`**: Toggle AI chatbot\n"
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
