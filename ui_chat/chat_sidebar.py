"""
Exact Replica Sidebar for National Bonds AI (V2)
"""

import streamlit as st
from ui_chat.chat_store import load_all_chats

def render_sidebar(active_chat_id=None):
    selected_chat_id = active_chat_id
    trigger_new_chat = False

    with st.sidebar:
        # 1. Top Brand Header: "National Bonds AI" + Search & Toggle Icons
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: flex-start; padding: 2px 2px 14px 2px;">
            <div style="font-size: 15px; font-weight: 700; color: #000000; line-height: 1.15; letter-spacing: -0.01em;">
                National Bonds<br><span style="font-weight: 800;">AI</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; color: #6B7280; font-size: 15px; padding-top: 2px;">
                <span title="Search" style="cursor: pointer;">🔍</span>
                <span title="Toggle sidebar" style="cursor: pointer;">◫</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. 'New chat' Button
        if st.button("📝  New chat", key="btn_new_chat_top", use_container_width=True):
            trigger_new_chat = True

        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)

        # 3. 'Recents' Section Heading
        st.markdown("""
        <div style="font-size: 11px; font-weight: 500; color: #9CA3AF; letter-spacing: 0.02em; padding: 8px 4px 4px 4px;">
            Recents
        </div>
        """, unsafe_allow_html=True)

        chats = load_all_chats()

        # 4. Clean List of Recents
        for cid, cdata in chats.items():
            title = cdata.get("title", "New chat")
            is_active = (cid == active_chat_id)
            btn_type = "primary" if is_active else "secondary"
            
            if st.button(title, key=f"chat_nav_{cid}", use_container_width=True, type=btn_type):
                selected_chat_id = cid
                st.rerun()

    return selected_chat_id, trigger_new_chat
