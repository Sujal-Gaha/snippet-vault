import json
import streamlit as st

DEFAULT_THEMES = {
    "Nordic Dark (Default)": {
        "primary": "#88c0d0",
        "background": "#2e3440",
        "secondary_background": "#3b4252",
        "text": "#eceff4",
        "border": "rgba(255, 255, 255, 0.15)",
    },
    "Nordic Light": {
        "primary": "#5e81ac",
        "background": "#eceff4",
        "secondary_background": "#e5e9f0",
        "text": "#2e3440",
        "border": "#4c566a",
    },
    "Rose Dark": {
        "primary": "oklch(0.637 0.237 25.331)",
        "background": "oklch(0.141 0.005 285.823)",
        "secondary_background": "oklch(0.21 0.006 285.885)",
        "text": "oklch(0.985 0 0)",
        "border": "rgba(255, 255, 255, 0.12)",
    },
    "Rose Light": {
        "primary": "oklch(0.637 0.237 25.331)",
        "background": "oklch(1 0 0)",
        "secondary_background": "oklch(0.967 0.001 286.375)",
        "text": "oklch(0.141 0.005 285.823)",
        "border": "#6e6578",
    },
    "Catppuccin Mocha": {
        "primary": "#cba6f7",
        "background": "#1e1e2e",
        "secondary_background": "#313244",
        "text": "#cdd6f4",
        "border": "rgba(255, 255, 255, 0.1)",
    },
    "Shadcn": {
        "primary": "#ffffff",
        "background": "#09090b",
        "secondary_background": "#18181b",
        "text": "#fafafa",
        "border": "rgba(255, 255, 255, 0.15)",
    },
}


def load_themes_config(settings_repo):
    """Loads custom themes and the selected theme from the database settings."""
    try:
        selected_theme = settings_repo.get("selected_theme", "Nordic Dark (Default)")
        custom_themes_json = settings_repo.get("custom_themes", "{}")
        custom_themes = json.loads(custom_themes_json)
        return {"selected_theme": selected_theme, "custom_themes": custom_themes}
    except Exception as e:
        print(f"Error loading themes from database: {e}")
        return {"selected_theme": "Nordic Dark (Default)", "custom_themes": {}}


def save_themes_config(settings_repo, selected_theme, custom_themes):
    """Saves custom themes and the selected theme to the database settings."""
    try:
        settings_repo.set("selected_theme", selected_theme)
        settings_repo.set("custom_themes", json.dumps(custom_themes))
    except Exception as e:
        print(f"Error saving themes to database: {e}")


def inject_custom_styles(settings_repo):
    config = load_themes_config(settings_repo)
    selected_name = config.get("selected_theme", "Nordic Dark (Default)")
    custom_themes = config.get("custom_themes", {})

    if selected_name in DEFAULT_THEMES:
        theme_colors = DEFAULT_THEMES[selected_name]
    elif selected_name in custom_themes:
        theme_colors = custom_themes[selected_name]
    else:
        theme_colors = DEFAULT_THEMES["Nordic Dark (Default)"]

    primary = theme_colors.get("primary", "#88c0d0")
    bg = theme_colors.get("background", "#2e3440")
    sec_bg = theme_colors.get("secondary_background", "#3b4252")
    text = theme_colors.get("text", "#eceff4")
    border = theme_colors.get("border", f"color-mix(in srgb, {text} 18%, transparent)")

    import os
    from string import Template

    # Load and render modular CSS templates
    css_files = [
        "base.css",
        "card.css",
        "button.css",
        "input.css",
        "dialog.css",
        "svg.css",
        "iframe.css",
    ]
    current_dir = os.path.dirname(os.path.abspath(__file__))
    css_dir = os.path.join(current_dir, "css")

    compiled_css = []
    mapping = {
        "primary": primary,
        "bg": bg,
        "sec_bg": sec_bg,
        "text": text,
        "border": border,
    }

    for filename in css_files:
        filepath = os.path.join(css_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                template_str = f.read()
                # Use Template class to safely replace placeholder tags like $primary, $bg
                t = Template(template_str)
                compiled_css.append(t.substitute(mapping))
        except Exception as e:
            print(f"Error loading CSS file {filename}: {e}")

    joined_css = "\n".join(compiled_css)

    st.html(f"""
    <style>
{joined_css}
    </style>
    """)
