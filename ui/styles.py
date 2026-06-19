import json
import streamlit as st

DEFAULT_THEMES = {
    "Nordic Dark (Default)": {
        "primary": "#88c0d0",
        "background": "#2e3440",
        "secondary_background": "#3b4252",
        "text": "#eceff4",
    },
    "Rose Theme": {
        "primary": "#ebbcba",
        "background": "#191724",
        "secondary_background": "#26233a",
        "text": "#e0def4",
    },
    "Catppuccin Mocha": {
        "primary": "#cba6f7",
        "background": "#1e1e2e",
        "secondary_background": "#313244",
        "text": "#cdd6f4",
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

    st.html(f"""
    <style>
        /* Theme variables applied to root and key elements */
        :root, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], [data-testid="stSidebar"] {{
            --primary-color: {primary} !important;
            --background-color: {bg} !important;
            --secondary-background-color: {sec_bg} !important;
            --text-color: {text} !important;
            
            /* Streamlit specific variables to trigger theme colors on elements */
            --st-color-background: {bg} !important;
            --st-color-background-secondary: {sec_bg} !important;
            --st-color-text: {text} !important;
            --st-color-primary: {primary} !important;
        }}
        
        /* Core layout and app container backgrounds */
        .stApp {{
            background-color: {bg} !important;
            color: {text} !important;
        }}
        [data-testid="stAppViewContainer"] {{
            background-color: {bg} !important;
            color: {text} !important;
        }}
        [data-testid="stHeader"] {{
            background-color: {bg} !important;
        }}
        [data-testid="stSidebar"] {{
            background-color: {sec_bg} !important;
            border-right: 1px solid rgba(128, 128, 128, 0.1) !important;
        }}
        
        /* Sidebar elements overrides */
        [data-testid="stSidebar"] .stMarkdown p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] label {{
            color: {text} !important;
        }}

        /* Input fields and dropdown select components */
        div[data-baseweb="select"] > div, 
        div[data-baseweb="input"] > div,
        div[data-baseweb="base-input"] > input,
        textarea,
        input {{
            background-color: {bg} !important;
            color: {text} !important;
            border-color: rgba(128, 128, 128, 0.2) !important;
        }}
        
        div[data-baseweb="select"] > div:hover, 
        div[data-baseweb="input"] > div:hover,
        textarea:hover,
        input:hover {{
            border-color: {primary} !important;
        }}
        
        /* Streamlit primary/secondary buttons */
        button[kind="primary"] {{
            background-color: {primary} !important;
            color: {bg} !important;
            border: none !important;
            font-weight: 600 !important;
        }}
        button[kind="primary"]:hover {{
            opacity: 0.9 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        }}
        button[kind="secondary"] {{
            background-color: {sec_bg} !important;
            color: {text} !important;
            border: 1px solid rgba(128, 128, 128, 0.3) !important;
        }}
        button[kind="secondary"]:hover {{
            border-color: {primary} !important;
            color: {primary} !important;
            background-color: {bg} !important;
        }}
        
        /* Popovers background adjustment */
        div[data-testid="stPopoverBody"] {{
            background-color: {sec_bg} !important;
            border: 1px solid rgba(128, 128, 128, 0.2) !important;
        }}
        div[data-testid="stPopoverBody"] * {{
            color: {text} !important;
        }}
        
        /* BaseWeb and Streamlit virtualized selectbox dropdown list styles (rendered outside .stApp via React portals) */
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] > div,
        div[data-baseweb="menu"],
        div[data-baseweb="menu"] > div,
        ul[role="listbox"],
        ul[role="listbox"] div,
        div[data-testid="stVirtualDropdown"],
        div[data-testid="stVirtualDropdown"] > div,
        [data-testid="stVirtualDropdown"] {{
            background-color: {sec_bg} !important;
            border-color: rgba(128, 128, 128, 0.2) !important;
        }}
        div[data-baseweb="popover"] ul,
        div[data-baseweb="menu"] ul,
        div[data-testid="stVirtualDropdown"] ul {{
            background-color: {sec_bg} !important;
        }}
        div[data-baseweb="popover"] ul *,
        div[data-baseweb="menu"] *,
        div[data-testid="stVirtualDropdown"] *,
        [data-testid="stVirtualDropdown"] * {{
            background-color: transparent !important;
            color: {text} !important;
        }}
        
        /* Global Listbox & Option styling overrides (selectbox dropdown items and nested wrappers) */
        [role="listbox"],
        [role="listbox"] *,
        [role="option"],
        [role="option"] *,
        [role="option"] > div,
        [role="option"] > span,
        div[data-baseweb="popover"] li,
        div[data-baseweb="menu"] li,
        li[role="option"],
        div[role="option"],
        [data-testid="stVirtualDropdown"] div[role="option"] {{
            background-color: {sec_bg} !important;
            color: {text} !important;
            transition: background-color 0.1s ease !important;
        }}
        
        /* Highlighted/Hovered states for options and all descendants (forcing colors to Mauve and Base background) */
        [role="option"]:hover,
        [role="option"]:hover *,
        [role="option"][aria-selected="true"],
        [role="option"][aria-selected="true"] *,
        [role="option"][data-highlighted="true"],
        [role="option"][data-highlighted="true"] *,
        [data-active="true"],
        [data-active="true"] *,
        li[role="option"]:hover,
        li[role="option"]:hover *,
        div[role="option"]:hover,
        div[role="option"]:hover *,
        div[data-baseweb="popover"] li:hover,
        div[data-baseweb="popover"] li:hover *,
        div[data-baseweb="popover"] li[aria-selected="true"],
        div[data-baseweb="popover"] li[aria-selected="true"] *,
        div[data-baseweb="popover"] li[data-highlighted="true"],
        div[data-baseweb="popover"] li[data-highlighted="true"] *,
        div[data-baseweb="menu"] li:hover,
        div[data-baseweb="menu"] li:hover *,
        [data-testid="stVirtualDropdown"] div[role="option"]:hover,
        [data-testid="stVirtualDropdown"] div[role="option"]:hover *,
        [data-testid="stVirtualDropdown"] [data-active="true"],
        [data-testid="stVirtualDropdown"] [data-active="true"] * {{
            background-color: {primary} !important;
            color: {bg} !important;
        }}
        
        /* Metric widget styling */
        [data-testid="stMetricValue"] {{
            color: {primary} !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: {text} !important;
            opacity: 0.8;
        }}

        /* Global Segoe UI Font override (targeting text elements and controls while protecting icons) */
        html, body, p, li, h1, h2, h3, h4, label, input, select, textarea, button, .snippet-title, .snippet-desc {{
            font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, sans-serif !important;
        }}
        
        /* Card design */
        .snippet-card {{
            background-color: {sec_bg};
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            border: 1px solid rgba(128, 128, 128, 0.2);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.03);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }}
        .snippet-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
            border-color: {primary};
        }}
        .snippet-title {{
            color: {primary};
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 5px;
        }}
        .snippet-card p, .snippet-card li, .snippet-card h1, .snippet-card h2, .snippet-card h3, .snippet-card h4 {{
            color: {text};
            line-height: 1.6;
        }}
        /* Tags styling */
        .tag-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 15px;
        }}
        .tag-badge {{
            background-color: {bg};
            color: {text};
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 0.8rem;
            font-weight: 500;
            border: 1px solid rgba(128, 128, 128, 0.2);
        }}
        .type-badge-code {{
            background-color: {primary}dd; /* theme primary with some transparency */
            color: {bg};
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: bold;
            text-transform: uppercase;
            margin-right: 12px;
            display: inline-block;
            vertical-align: middle;
        }}
        .type-badge-command {{
            background-color: #bf616a;
            color: #eceff4;
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: bold;
            text-transform: uppercase;
            margin-right: 12px;
            display: inline-block;
            vertical-align: middle;
        }}
        .category-badge {{
            background-color: {bg};
            color: {primary};
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 500;
            border: 1px solid rgba(128, 128, 128, 0.2);
            display: inline-block;
            vertical-align: middle;
            margin-right: 12px;
        }}
    </style>
    """)
