import streamlit as st
import sqlite3
from datetime import datetime

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(page_title="Diary Space", page_icon="🌙")

# ======================
# DARK AESTHETIC + HANDWRITING THEME
# ======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Indie+Flower&family=Caveat:wght@400;600&display=swap');

.stApp {
    background-color: #0b0b10;
    color: #e6e6e6;
}

/* Titles */
h1, h2, h3 {
    color: #c9a7ff;
    font-family: 'Caveat', cursive;
}

/* Text input */
.stTextArea textarea {
    font-family: 'Indie Flower', cursive !important;
    font-size: 18px !important;
    background-color: #151522 !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    border: 1px solid #2c2c3a !important;
}

/* Buttons */
.stButton button {
    background-color: #7c5cff;
    color: white;
    border-radius: 10px;
    border: none;
}

.stButton button:hover {
    background-color: #9a7bff;
}

/* Text display */
.stMarkdown {
    font-family: 'Caveat', cursive;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# PASSWORD LOCK
# ======================
PASSWORD = "1234"  # change this

if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("🔒 Locked Diary Space")
    pw = st.text_input("Enter Password", type="password")

    if st.button("Unlock"):
        if pw == PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("Wrong password")
    st.stop()

# ======================
# DATABASE (SQLite)
# ======================
conn = sqlite3.connect("diary.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS diary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    time TEXT,
    type TEXT
)
""")
conn.commit()

def add_entry(text, entry_type="diary"):
    c.execute(
        "INSERT INTO diary (text, time, type) VALUES (?, ?, ?)",
        (text, str(datetime.now()), entry_type)
    )
    conn.commit()

def get_entries(entry_type):
    return c.execute(
        "SELECT id, text, time FROM diary WHERE type=? ORDER BY id DESC",
        (entry_type,)
    ).fetchall()

def delete_entry(entry_id):
    c.execute("DELETE FROM diary WHERE id=?", (entry_id,))
    conn.commit()

def update_entry(entry_id, new_text):
    c.execute("UPDATE diary SET text=? WHERE id=?", (new_text, entry_id))
    conn.commit()

# ======================
# UI
# ======================
st.title("🌙 My Diary Space")

mode = st.selectbox("Choose mode:", ["📖 Diary", "💔 Unsent Message (Closure Mode)"])

entry = st.text_area("Write your thoughts...")

if st.button("Save ✨"):
    if entry.strip():
        if mode.startswith("💔"):
            add_entry(entry, "unsent")
        else:
            add_entry(entry, "diary")
        st.success("Saved!")
        st.rerun()

st.divider()

# ======================
# DIARY ENTRIES
# ======================
st.subheader("📖 Diary Entries")

diary_entries = get_entries("diary")

for entry_id, text, time in diary_entries:
    st.markdown(f"**{time}**")
    st.write(text)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"🗑 Delete {entry_id} (D)"):
            delete_entry(entry_id)
            st.rerun()

    with col2:
        if st.button(f"✏️ Edit {entry_id} (D)"):
            st.session_state.edit_id = entry_id
            st.session_state.edit_text = text

    st.markdown("---")

# ======================
# UNSENT MESSAGES (CLOSURE MODE)
# ======================
st.subheader("💔 Unsent Messages (Closure Mode)")

unsent_entries = get_entries("unsent")

for entry_id, text, time in unsent_entries:
    st.markdown(f"**{time}**")
    st.write(f"💔 {text}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"🗑 Delete {entry_id} (U)"):
            delete_entry(entry_id)
            st.rerun()

    with col2:
        if st.button(f"✏️ Edit {entry_id} (U)"):
            st.session_state.edit_id = entry_id
            st.session_state.edit_text = text

    st.markdown("---")

# ======================
# EDIT MODE
# ======================
if "edit_id" in st.session_state:
    st.subheader("✏️ Edit Entry")

    new_text = st.text_area("Update your entry", st.session_state.edit_text)

    if st.button("Update"):
        update_entry(st.session_state.edit_id, new_text)
        del st.session_state.edit_id
        del st.session_state.edit_text
        st.success("Updated!")
        st.rerun()