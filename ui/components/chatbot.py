import streamlit as st


def render_chatbot_widget():
    """Renders a floating AI Copilot chatbot head on the bottom-right corner of the application."""
    st.html("""
    <style>
    .chatbot-widget {
        position: fixed;
        bottom: 24px;
        right: 24px;
        z-index: 999999;
    }

    .chatbot-head {
        width: 56px;
        height: 56px;
        border-radius: 50%;
        background-color: var(--primary);
        color: var(--primary-foreground);
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .chatbot-head:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    }

    .chatbot-head:active {
        transform: scale(0.95);
    }

    .chatbot-head .close-icon {
        display: none;
    }

    .chatbot-head .chat-icon {
        display: block;
    }

    .chatbot-window {
        position: absolute;
        bottom: 72px;
        right: 0;
        width: 320px;
        height: 380px;
        background-color: var(--card);
        border: var(--border-width) solid var(--border);
        border-radius: var(--radius);
        box-shadow: var(--shadow-2xl);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        opacity: 0;
        transform: translateY(20px) scale(0.95);
        pointer-events: none;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    /* Sibling toggling rules using CSS checkbox hack */
    #chatbot-toggle-checkbox:checked ~ .chatbot-window {
        opacity: 1 !important;
        transform: translateY(0) scale(1) !important;
        pointer-events: auto !important;
    }

    #chatbot-toggle-checkbox:checked ~ .chatbot-head .chat-icon {
        display: none !important;
    }

    #chatbot-toggle-checkbox:checked ~ .chatbot-head .close-icon {
        display: block !important;
    }

    .chatbot-header {
        padding: 12px 16px;
        background-color: var(--secondary);
        border-bottom: var(--border-width) solid var(--border);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .chatbot-title-container {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }

    .chatbot-title {
        font-weight: 600;
        font-size: 14px;
        color: var(--foreground);
    }

    .chatbot-badge {
        align-self: flex-start;
        font-size: 8px;
        font-weight: 700;
        text-transform: uppercase;
        background-color: var(--primary);
        color: var(--primary-foreground);
        padding: 1px 5px;
        border-radius: 99px;
        letter-spacing: 0.5px;
    }

    .chatbot-close-btn {
        background: none;
        border: none;
        font-size: 18px;
        color: var(--muted-foreground);
        cursor: pointer;
        padding: 0;
        transition: color 0.2s;
    }

    .chatbot-close-btn:hover {
        color: var(--foreground);
    }

    .chatbot-content {
        padding: 12px 16px;
        display: flex;
        flex-direction: column;
        height: calc(100% - 50px);
        overflow: hidden;
    }

    .chatbot-desc {
        font-size: 12px;
        line-height: 1.4;
        color: var(--muted-foreground);
        margin-bottom: 12px;
    }

    .chat-messages {
        flex-grow: 1;
        overflow-y: auto;
        margin-bottom: 12px;
        display: flex;
        flex-direction: column;
    }

    .chat-message {
        display: flex;
        gap: 8px;
        align-items: flex-start;
    }

    .chat-message.assistant .avatar {
        font-size: 14px;
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background-color: var(--secondary);
        display: flex;
        align-items: center;
        justify-content: center;
        border: var(--border-width) solid var(--border);
    }

    .chat-message.assistant .message-bubble {
        background-color: var(--secondary);
        color: var(--foreground);
        font-size: 12px;
        line-height: 1.4;
        padding: 8px 10px;
        border-radius: 0 var(--radius) var(--radius) var(--radius);
        border: var(--border-width) solid var(--border);
    }

    .chat-input-container {
        display: flex;
        gap: 6px;
        border: var(--border-width) solid var(--border);
        background-color: var(--background);
        padding: 2px 8px;
        border-radius: var(--radius);
        align-items: center;
    }

    .chat-input {
        flex-grow: 1;
        background: none;
        border: none;
        outline: none;
        font-size: 12px;
        color: var(--foreground);
        padding: 4px 0;
    }

    .chat-input::placeholder {
        color: var(--muted-foreground);
    }

    .chat-send-btn {
        background: none;
        border: none;
        color: var(--muted-foreground);
        cursor: not-allowed;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2px;
    }
    </style>

    <div class="chatbot-widget">
        <!-- Hidden Checkbox for CSS-only Toggle -->
        <input type="checkbox" id="chatbot-toggle-checkbox" style="display: none;">

        <!-- Floating Chat Head -->
        <label class="chatbot-head" for="chatbot-toggle-checkbox">
            <!-- Chat Icon -->
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="chat-icon">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
            <!-- Close Icon -->
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="close-icon">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        </label>

        <!-- Chat Window -->
        <div class="chatbot-window" id="chatbot-window">
            <div class="chatbot-header">
                <div class="chatbot-title-container">
                    <span class="chatbot-title">💬 AI Copilot</span>
                    <span class="chatbot-badge">Coming Soon</span>
                </div>
                <label class="chatbot-close-btn" for="chatbot-toggle-checkbox">×</label>
            </div>
            <div class="chatbot-content">
                <div class="chatbot-desc">
                    An intelligent AI assistant designed to help you instantly search, explain, and write snippets or commands using natural language.
                </div>
                <div class="chat-messages">
                    <div class="chat-message assistant">
                        <div class="avatar">🤖</div>
                        <div class="message-bubble">
                            Hello! I am your future AI assistant. Soon you will be able to ask me to find snippets, explain code, or write commands for you!
                        </div>
                    </div>
                </div>
                <div class="chat-input-container">
                    <input type="text" class="chat-input" placeholder="Ask for a snippet..." disabled>
                    <button class="chat-send-btn" disabled>
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="22" y1="2" x2="11" y2="13"></line>
                            <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                        </svg>
                    </button>
                </div>
            </div>
        </div>
    </div>
    """)
