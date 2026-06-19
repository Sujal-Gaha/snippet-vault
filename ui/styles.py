import streamlit as st

def inject_custom_styles():
    st.html("""
    <style>
        /* Global Font override (targeting text elements only to protect icon fonts) */
        html, body, p, li, h1, h2, h3, h4, span.snippet-title, .snippet-desc {
            font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, sans-serif !important;
        }
        
        /* Card design */
        .snippet-card {
            background-color: var(--secondary-background-color);
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 24px;
            border: 1px solid rgba(128, 128, 128, 0.2);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.03);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
        }
        .snippet-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
            border-color: var(--primary-color);
        }
        .snippet-title {
            color: var(--primary-color);
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 5px;
        }
        .snippet-card p, .snippet-card li, .snippet-card h1, .snippet-card h2, .snippet-card h3, .snippet-card h4 {
            color: var(--text-color);
            line-height: 1.6;
        }
        /* Tags styling */
        .tag-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 15px;
        }
        .tag-badge {
            background-color: var(--background-color);
            color: var(--text-color);
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 0.8rem;
            font-weight: 500;
            border: 1px solid rgba(128, 128, 128, 0.2);
        }
        .type-badge-code {
            background-color: #5e81ac;
            color: #eceff4;
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: bold;
            text-transform: uppercase;
            margin-right: 12px;
            display: inline-block;
            vertical-align: middle;
        }
        .type-badge-command {
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
        }
        .category-badge {
            background-color: var(--background-color);
            color: var(--primary-color);
            padding: 3px 10px;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 500;
            border: 1px solid rgba(128, 128, 128, 0.2);
            display: inline-block;
            vertical-align: middle;
            margin-right: 12px;
        }
    </style>
    """)
