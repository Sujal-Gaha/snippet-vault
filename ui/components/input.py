from typing import Any, Callable, List, Optional, Union
import streamlit as st

def render_text_input(
    label: str,
    value: str = "",
    placeholder: Optional[str] = None,
    max_chars: Optional[int] = None,
    key: Optional[str] = None,
    help: Optional[str] = None,
    type: str = "default",
    disabled: bool = False,
    label_visibility: str = "visible",
) -> str:
    """Reusable text input component wrapping Streamlit's native text_input."""
    return st.text_input(
        label=label,
        value=value,
        placeholder=placeholder,
        max_chars=max_chars,
        key=key,
        help=help,
        type=type,
        disabled=disabled,
        label_visibility=label_visibility,
    )

def render_text_area(
    label: str,
    value: str = "",
    placeholder: Optional[str] = None,
    height: Optional[int] = None,
    max_chars: Optional[int] = None,
    key: Optional[str] = None,
    help: Optional[str] = None,
    disabled: bool = False,
    label_visibility: str = "visible",
) -> str:
    """Reusable text area component wrapping Streamlit's native text_area."""
    return st.text_area(
        label=label,
        value=value,
        placeholder=placeholder,
        height=height,
        max_chars=max_chars,
        key=key,
        help=help,
        disabled=disabled,
        label_visibility=label_visibility,
    )

def render_selectbox(
    label: str,
    options: Union[List[Any], tuple],
    index: int = 0,
    format_func: Optional[Callable[[Any], str]] = None,
    key: Optional[str] = None,
    help: Optional[str] = None,
    disabled: bool = False,
    label_visibility: str = "visible",
) -> Any:
    """Reusable selectbox component wrapping Streamlit's native selectbox."""
    return st.selectbox(
        label=label,
        options=options,
        index=index,
        format_func=format_func if format_func is not None else str,
        key=key,
        help=help,
        disabled=disabled,
        label_visibility=label_visibility,
    )
