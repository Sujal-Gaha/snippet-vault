import json
import streamlit as st

from ui.themes import DEFAULT_THEMES


def load_themes_config(settings_repo):
    """Loads custom themes and the selected theme from the database settings."""
    try:
        selected_theme = settings_repo.get("selected_theme", "Nordic Dark")
        custom_themes_json = settings_repo.get("custom_themes", "{}")
        custom_themes = json.loads(custom_themes_json)
        return {"selected_theme": selected_theme, "custom_themes": custom_themes}
    except Exception as e:
        print(f"Error loading themes from database: {e}")
        return {"selected_theme": "Nordic Dark", "custom_themes": {}}


def save_themes_config(settings_repo, selected_theme, custom_themes):
    """Saves custom themes and the selected theme to the database settings."""
    try:
        settings_repo.set("selected_theme", selected_theme)
        settings_repo.set("custom_themes", json.dumps(custom_themes))
    except Exception as e:
        print(f"Error saving themes to database: {e}")


def format_font_family_string(font_str):
    """Formats a font family list string ensuring multi-word fonts without quotes are properly quoted."""
    if not font_str:
        return font_str
    parts = []
    for p in font_str.split(','):
        p = p.strip()
        if not p:
            continue
        # Check if already quoted
        if (p.startswith('"') and p.endswith('"')) or (p.startswith("'") and p.endswith("'")):
            parts.append(p)
        elif ' ' in p:
            # Multi-word family name not quoted, wrap in double quotes
            parts.append(f'"{p}"')
        else:
            parts.append(p)
    return ", ".join(parts)


def get_font_imports(theme_colors):
    """Generates the Google Fonts import URL based on the font properties of the active theme."""
    font_sans = theme_colors.get("font_sans", "")
    font_serif = theme_colors.get("font_serif", "")
    font_mono = theme_colors.get("font_mono", "")
    
    font_values = [font_sans, font_serif, font_mono]
    detected_families = []
    
    system_fonts = {
        "sans-serif", "serif", "monospace", "system-ui", "ui-sans-serif", "ui-serif", 
        "ui-monospace", "segoe ui", "apple-system", "blinkmacsystemfont", "roboto", 
        "helvetica neue", "arial", "noto sans", "apple color emoji", "segoe ui emoji", 
        "segoe ui symbol", "noto color emoji", "georgia", "cambria", "times new roman", 
        "times", "courier new", "courier", "menlo", "monaco", "consolas", "liberation mono",
        "sfmono-regular", "helvetica"
    }
    
    google_fonts_mapping = {
        "architects daughter": "Architects+Daughter",
        "montserrat": "Montserrat:ital,wght@0,100..900;1,100..900",
        "fira code": "Fira+Code:wght@300..700",
        "dm sans": "DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000",
        "space mono": "Space+Mono:ital,wght@0,400;0,700;1,400;1,700",
        "dm serif text": "DM+Serif+Text:ital@0;1",
        "dm mono": "DM+Mono:ital,wght@0,300;0,400;0,500;1,300;1,400;1,500",
    }
    
    for val in font_values:
        if not val:
            continue
        # Split by comma to extract font families
        parts = [p.strip().strip('"\'') for p in val.split(',')]
        for part in parts:
            if not part:
                continue
            part_lower = part.lower()
            if part_lower in system_fonts:
                continue
            
            # Match mapped ones
            if part_lower in google_fonts_mapping:
                param = google_fonts_mapping[part_lower]
                if param not in detected_families:
                    detected_families.append(param)
            else:
                # Dynamically format query parameter for non-mapped fonts (if they are Google Fonts)
                cleaned_name = "+".join([w.capitalize() for w in part.split()])
                param = cleaned_name
                # Keep parameter unique
                if param not in detected_families:
                    detected_families.append(param)
                    
    if not detected_families:
        return ""
        
    # Construct Google Fonts URL
    families_query = "&".join([f"family={fam}" for fam in detected_families])
    return f"@import url('https://fonts.googleapis.com/css2?{families_query}&display=swap');\n"


def inject_custom_styles(settings_repo):
    config = load_themes_config(settings_repo)
    selected_name = config.get("selected_theme", "Nordic Dark")
    custom_themes = config.get("custom_themes", {})

    if selected_name in DEFAULT_THEMES:
        theme_colors = DEFAULT_THEMES[selected_name]
    elif selected_name in custom_themes:
        theme_colors = custom_themes[selected_name]
    else:
        theme_colors = DEFAULT_THEMES["Nordic Dark"]

    primary = theme_colors.get("primary", "#88c0d0")
    bg = theme_colors.get("background", "#2e3440")
    sec_bg = theme_colors.get("secondary_background", "#3b4252")
    text = theme_colors.get("text", "#eceff4")
    border = theme_colors.get("border", f"color-mix(in srgb, {text} 18%, transparent)")

    # Extended variables
    foreground = theme_colors.get("foreground", text)
    card = theme_colors.get("card", sec_bg)
    card_foreground = theme_colors.get("card_foreground", text)
    popover = theme_colors.get("popover", sec_bg)
    popover_foreground = theme_colors.get("popover_foreground", text)
    primary_foreground = theme_colors.get("primary_foreground", bg)
    secondary = theme_colors.get("secondary", sec_bg)
    secondary_foreground = theme_colors.get("secondary_foreground", text)
    muted = theme_colors.get("muted", sec_bg)
    muted_foreground = theme_colors.get("muted_foreground", f"color-mix(in srgb, {text} 60%, transparent)")
    accent = theme_colors.get("accent", sec_bg)
    accent_foreground = theme_colors.get("accent_foreground", primary)
    destructive = theme_colors.get("destructive", "oklch(0.704 0.191 22.216)")
    destructive_foreground = theme_colors.get("destructive_foreground", "#ffffff")
    input_color = theme_colors.get("input", border)
    ring = theme_colors.get("ring", primary)

    chart_1 = theme_colors.get("chart_1", primary)
    chart_2 = theme_colors.get("chart_2", secondary)
    chart_3 = theme_colors.get("chart_3", accent)
    chart_4 = theme_colors.get("chart_4", "oklch(0.7323 0.2492 142.4953)")
    chart_5 = theme_colors.get("chart_5", "oklch(0.5931 0.2726 328.3634)")

    sidebar = theme_colors.get("sidebar", sec_bg)
    sidebar_foreground = theme_colors.get("sidebar_foreground", text)
    sidebar_primary = theme_colors.get("sidebar_primary", primary)
    sidebar_primary_foreground = theme_colors.get("sidebar_primary_foreground", bg)
    sidebar_accent = theme_colors.get("sidebar_accent", sec_bg)
    sidebar_accent_foreground = theme_colors.get("sidebar_accent_foreground", primary)
    sidebar_border = theme_colors.get("sidebar_border", border)
    sidebar_ring = theme_colors.get("sidebar_ring", primary)

    font_sans = format_font_family_string(theme_colors.get("font_sans", '"Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, sans-serif'))
    font_serif = format_font_family_string(theme_colors.get("font_serif", 'ui-serif, Georgia, Cambria, "Times New Roman", Times, serif'))
    font_mono = format_font_family_string(theme_colors.get("font_mono", 'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace'))

    radius = theme_colors.get("radius", "12px")
    border_width = theme_colors.get("border_width", "1px")

    shadow_2xs = theme_colors.get("shadow_2xs", "0 1px 2px rgba(0, 0, 0, 0.05)")
    shadow_xs = theme_colors.get("shadow_xs", "0 1px 2px rgba(0, 0, 0, 0.05)")
    shadow_sm = theme_colors.get("shadow_sm", "0 1px 2px 0 rgba(0, 0, 0, 0.05)")
    shadow = theme_colors.get("shadow", "0 4px 6px rgba(0, 0, 0, 0.03)")
    shadow_md = theme_colors.get("shadow_md", "0 4px 12px rgba(0, 0, 0, 0.15)")
    shadow_lg = theme_colors.get("shadow_lg", "0 10px 15px -3px rgba(0, 0, 0, 0.1)")
    shadow_xl = theme_colors.get("shadow_xl", "0 20px 25px -5px rgba(0, 0, 0, 0.1)")
    shadow_2xl = theme_colors.get("shadow_2xl", "0 25px 50px -12px rgba(0, 0, 0, 0.25)")

    from string import Template
    from ui.css import (
        BASE_CSS,
        CARD_CSS,
        BADGE_CSS,
        BUTTON_CSS,
        INPUT_CSS,
        DIALOG_CSS,
        SVG_CSS,
        IFRAME_CSS,
    )

    # Modular CSS templates
    css_templates = [
        BASE_CSS,
        CARD_CSS,
        BADGE_CSS,
        BUTTON_CSS,
        INPUT_CSS,
        DIALOG_CSS,
        SVG_CSS,
        IFRAME_CSS,
    ]

    compiled_css = []
    mapping = {
        "clr_primary": primary,
        "clr_bg": bg,
        "clr_sec_bg": sec_bg,
        "clr_text": text,
        "clr_border": border,
        
        "background": bg,
        "foreground": foreground,
        "card": card,
        "card_foreground": card_foreground,
        "popover": popover,
        "popover_foreground": popover_foreground,
        "primary_foreground": primary_foreground,
        "secondary": secondary,
        "secondary_foreground": secondary_foreground,
        "muted": muted,
        "muted_foreground": muted_foreground,
        "accent": accent,
        "accent_foreground": accent_foreground,
        "destructive": destructive,
        "destructive_foreground": destructive_foreground,
        "input": input_color,
        "ring": ring,
        "chart_1": chart_1,
        "chart_2": chart_2,
        "chart_3": chart_3,
        "chart_4": chart_4,
        "chart_5": chart_5,
        "sidebar": sidebar,
        "sidebar_foreground": sidebar_foreground,
        "sidebar_primary": sidebar_primary,
        "sidebar_primary_foreground": sidebar_primary_foreground,
        "sidebar_accent": sidebar_accent,
        "sidebar_accent_foreground": sidebar_accent_foreground,
        "sidebar_border": sidebar_border,
        "sidebar_ring": sidebar_ring,
        "font_sans": font_sans,
        "font_serif": font_serif,
        "font_mono": font_mono,
        "radius": radius,
        "border_width": border_width,
        "shadow_2xs": shadow_2xs,
        "shadow_xs": shadow_xs,
        "shadow_sm": shadow_sm,
        "shadow": shadow,
        "shadow_md": shadow_md,
        "shadow_lg": shadow_lg,
        "shadow_xl": shadow_xl,
        "shadow_2xl": shadow_2xl,
    }

    for template_str in css_templates:
        t = Template(template_str)
        compiled_css.append(t.substitute(mapping))

    font_import = get_font_imports(theme_colors)
    joined_css = font_import + "\n".join(compiled_css)

    st.html(f"""
    <style>
{joined_css}
    </style>
    """)
