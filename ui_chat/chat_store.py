"""
Persistent Chat Session Storage for National Bonds AI (V2)
Persists chats to data/chat_sessions.json so history is maintained across reloads.
"""

import os
import json
import uuid
from datetime import datetime

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SESSIONS_FILE = os.path.join(current_dir, "data", "chat_sessions.json")

SEED_CHATS = [
    ("Dashboard Redesign Prompt", "How should we structure the executive dashboard redesign?"),
    ("Create Quotation Memo", "Generate an official professional quotation memo for AI transformation."),
    ("AI Data Processing Costs", "What are the token and infrastructure costs for 154K customer cohort processing?"),
    ("AI BI Implementation Plan", "Outline the 6-phase roadmap for AI BI platform rollout."),
    ("AI monitoring overview", "Provide an overview of early warning anomaly detection metrics."),
    ("Explain CT Report", "Explain the Central Bank compliance and Sharia fatwa audit trail report."),
    ("Books for Agency Operations", "Recommended best practices for agency sales distribution channels."),
    ("Reformat Anatomy Script", "Reformat the anatomical decomposition of Saving Bonds portfolio drop."),
    ("Cheapest Lip Sync Options", "Cost comparison for automated video briefing avatars."),
    ("Greeting exchange", "Hello, I am JD, your National Bonds intelligence copilot.")
]

def _ensure_dir():
    d = os.path.dirname(SESSIONS_FILE)
    if not os.path.exists(d):
        os.makedirs(d, exist_ok=True)

def load_all_chats():
    """Load all saved chats from JSON file, ordered by updated_at descending."""
    _ensure_dir()
    if not os.path.exists(SESSIONS_FILE):
        _seed_default_chats()
    try:
        with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if not data:
                _seed_default_chats()
                with open(SESSIONS_FILE, "r", encoding="utf-8") as f2:
                    data = json.load(f2)
            sorted_items = sorted(
                data.items(),
                key=lambda x: x[1].get("updated_at", ""),
                reverse=True
            )
            return dict(sorted_items)
    except Exception as e:
        print(f"Error loading chat sessions: {e}")
        return {}

def _seed_default_chats():
    """Seed initial chats matching the screenshot."""
    chats = {}
    now = datetime.now()
    for idx, (title, prompt) in enumerate(SEED_CHATS):
        cid = f"seed_{idx+1}"
        chats[cid] = {
            "id": cid,
            "title": title,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            "messages": [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": f"Here is the detailed intelligence overview for **{title}** based on National Bonds Corporation audited ground truth."}
            ]
        }
    with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(chats, f, indent=2, ensure_ascii=False)

def save_chat(chat_id, title, messages):
    """Save or update a chat session."""
    _ensure_dir()
    chats = load_all_chats()
    now_str = datetime.now().isoformat()
    
    if chat_id not in chats:
        chats[chat_id] = {
            "id": chat_id,
            "title": title or "New chat",
            "created_at": now_str,
            "updated_at": now_str,
            "messages": messages
        }
    else:
        chats[chat_id]["title"] = title or chats[chat_id].get("title", "New chat")
        chats[chat_id]["updated_at"] = now_str
        chats[chat_id]["messages"] = messages

    try:
        with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(chats, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving chat sessions: {e}")

def create_chat(initial_title="New chat"):
    """Create a new chat session and return its id."""
    chat_id = str(uuid.uuid4())[:8]
    save_chat(chat_id, initial_title, [])
    return chat_id

def delete_chat(chat_id):
    """Delete a specific chat session."""
    _ensure_dir()
    chats = load_all_chats()
    if chat_id in chats:
        del chats[chat_id]
        with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(chats, f, indent=2, ensure_ascii=False)

def clear_all_chats():
    """Clear all chat sessions and reseed defaults."""
    _ensure_dir()
    _seed_default_chats()

def generate_title_from_prompt(prompt):
    """Generate a clean, short title for the chat session from the first prompt."""
    clean = prompt.strip().replace("\n", " ")
    if len(clean) > 30:
        return clean[:28].rstrip() + "..."
    return clean
