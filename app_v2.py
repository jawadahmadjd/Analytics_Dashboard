"""
National Bonds Corporation - AI Product Management Transformation
Initiative: National Bonds AI Interface (Exact Screenshot Replica)
Author: Jawad Ahmad | Product AI Solutions
"""

import streamlit as st
import os
import sys
import importlib

# Ensure backend and UI modules are in Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import backend.jd_engine
importlib.reload(backend.jd_engine)
from backend.jd_engine import JDAgent

import ui_chat.chat_store
importlib.reload(ui_chat.chat_store)
from ui_chat.chat_store import (
    load_all_chats,
    save_chat,
    create_chat,
    generate_title_from_prompt
)

import ui_chat.chat_sidebar
importlib.reload(ui_chat.chat_sidebar)
from ui_chat.chat_sidebar import render_sidebar

import ui_chat.chat_components
importlib.reload(ui_chat.chat_components)
from ui_chat.chat_components import (
    render_empty_state,
    render_citation_accordion
)

# Page Configuration
st.set_page_config(
    page_title="National Bonds AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Clean Replica Theme
css_path = os.path.join(current_dir, "ui_chat", "chat_styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Cache Cognitive AI Agent
@st.cache_resource(show_spinner="Initializing National Bonds Intelligence Engine...")
def load_jd_agent():
    return JDAgent()

agent = load_jd_agent()

# Manage Active Chat ID in Session State
if "active_chat_id" not in st.session_state:
    st.session_state.active_chat_id = None

# Render Sidebar with 'National Bonds AI' header and 'Recents'
selected_chat_id, trigger_new_chat = render_sidebar(active_chat_id=st.session_state.active_chat_id)

if trigger_new_chat:
    st.session_state.active_chat_id = None
    st.rerun()

if selected_chat_id != st.session_state.active_chat_id:
    st.session_state.active_chat_id = selected_chat_id
    st.rerun()

# Load Current Conversation Data
all_chats = load_all_chats()
active_id = st.session_state.active_chat_id

current_messages = []
current_title = "New chat"
if active_id and active_id in all_chats:
    current_messages = all_chats[active_id].get("messages", [])
    current_title = all_chats[active_id].get("title", "New chat")

def process_and_save_message(user_prompt):
    """Processes user message through JDAgent and saves to persistent store."""
    global active_id, current_messages, current_title
    
    # If starting fresh, create a new chat session with smart title
    if not active_id or active_id not in all_chats:
        active_id = create_chat(initial_title=generate_title_from_prompt(user_prompt))
        st.session_state.active_chat_id = active_id
        current_messages = []
        current_title = generate_title_from_prompt(user_prompt)

    # 1. Append User Message
    current_messages.append({"role": "user", "content": user_prompt})

    # 2. Query JDAgent
    api_key = st.session_state.get("llm_api_key", None)
    policy_keywords = ['notice', 'withdrawal', 'sharia', 'fatwa', 'circular', 'penalty', 'terms', 'surrender']
    is_policy = any(k in user_prompt.lower() for k in policy_keywords)

    citation_meta = None
    if is_policy:
        kb_res = agent.query_knowledge_assistant(user_prompt)
        reply_text = kb_res.get('answer', '')
        citation_meta = {
            'document_ref': kb_res.get('document_ref', 'Official Circular'),
            'section': kb_res.get('section', 'Rules & Terms'),
            'fatwa_ref': kb_res.get('fatwa_ref', 'Approved')
        }
    else:
        reply_text = agent.answer(user_prompt, api_key=api_key)

    # 3. Append Assistant Message
    current_messages.append({
        "role": "assistant",
        "content": reply_text,
        "citation": citation_meta
    })

    # 4. Save to Store
    save_chat(active_id, current_title, current_messages)
    st.rerun()

# --------------------------------------------------------------------------
# TWO-STATE RENDERING:
# 1. Empty Chat: 'Where should we begin?' in center + centered input 'Ask anything'
# 2. Active Chat: Top-down messages stream + bottom input 'Ask anything'
# --------------------------------------------------------------------------

if len(current_messages) == 0:
    render_empty_state()
else:
    for msg in current_messages:
        role = msg["role"]
        with st.chat_message(role):
            st.markdown(msg["content"])
            if "citation" in msg and msg["citation"]:
                render_citation_accordion(msg["citation"])

# Universal Chat Input with 'Ask anything' placeholder
user_input = st.chat_input("Ask anything")

if user_input and user_input.strip():
    process_and_save_message(user_input.strip())
