import pandas as pd


def truncate_desc(desc, limit=90):
    if not desc:
        return ""
    text = desc.replace("**", "").replace("*", "").replace("`", "").strip()
    if len(text) > limit:
        return text[:limit] + "..."
    return text


def format_date(date_str):
    return pd.to_datetime(date_str).strftime("%b %d, %Y")
