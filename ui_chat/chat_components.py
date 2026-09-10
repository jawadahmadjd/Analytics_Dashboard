"""
Exact Replica Components for National Bonds AI (V2)
"""

import streamlit as st

def render_empty_state():
    """
    Renders the centered 'Where should we begin?' title and the marker
    that centers st.chat_input via CSS.
    """
    st.markdown("""
    <div id="empty-chat-marker"></div>
    <div class="empty-chat-hero">
        <div class="empty-chat-title">Where should we begin?</div>
    </div>
    """, unsafe_allow_html=True)

def render_citation_accordion(citation_meta):
    """Renders clean citation metadata in assistant responses."""
    if not citation_meta:
        return
    doc_ref = citation_meta.get("document_ref", "Official Circular")
    sec = citation_meta.get("section", "Ground Truth")
    fatwa = citation_meta.get("fatwa_ref", "Approved")
    
    st.markdown(f"""
    <div style="margin-top: 8px; padding: 6px 10px; background: #F9FAFB; border-left: 2px solid #2563EB; border-radius: 4px; font-size: 11px; color: #4B5563;">
        <strong>Source:</strong> {doc_ref} &middot; <strong>Section:</strong> {sec} &middot; <span style="color: #059669; font-weight: 600;">Fatwa {fatwa} Verified</span>
    </div>
    """, unsafe_allow_html=True)
