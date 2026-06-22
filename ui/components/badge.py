import html

def render_badge(label: str, badge_type: str, custom_style: str = "") -> str:
    """Reusable HTML component for rendering badges."""
    escaped_label = html.escape(label)
    if badge_type == "code":
        return f'<span class="type-badge-code" style="{custom_style}">{escaped_label}</span>'
    elif badge_type == "command":
        return f'<span class="type-badge-command" style="{custom_style}">{escaped_label}</span>'
    elif badge_type == "category":
        return f'<span class="category-badge" style="{custom_style}">{escaped_label}</span>'
    elif badge_type == "tag":
        return f'<span class="tag-badge" style="{custom_style}">#{escaped_label}</span>'
    return escaped_label
