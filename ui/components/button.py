import streamlit as st

def render_button(label: str, key: str = None, type: str = "secondary", use_container_width: bool = True, disabled: bool = False) -> bool:
    """Reusable button component wrapping Streamlit's native button."""
    return st.button(
        label,
        key=key,
        type=type,
        use_container_width=use_container_width,
        disabled=disabled,
    )
