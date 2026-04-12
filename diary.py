import streamlit as st
import sqlite3
from datetime import datetime

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(page_title="Diary Space", page_icon="🌙")

# ======================
# DB CONNECTION (STABLE)
# ======================
@st.cache_resource
def get_db():
    conn = sqlite3.connect("diary.db", check_same_thread=False)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS diary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        text TEXT,
        time TEXT,
        type TEXT
    )
    """)

    conn.commit()
    return conn, c

conn, c = get_db()

# ======================
# AUTH SYSTEM (REAL USERS)
# ======================
if "user" not in st.session_state:
    st.session_state.user = None

def register_user(username, password):
    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False

def login_user(username, password):
    user = c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    ).fetchone()
    return user

# ======================
# LOGIN UI
# ======================
if not st.session_state.user:
    st.title("🔒 Diary Space Login")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(u, p):
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Invalid login")

    with tab2:
        ru = st.text_input("New Username")
        rp = st.text_input("New Password", type="password")

        if st.button("Register"):
            if register_user(ru, rp):
                st.success("Account created! Now login.")
            else:
                st.error("Username already exists")

    st.stop()

# ======================
# USER DASHBOARD
# ======================
user = st.session_state.user

st.title(f"🌙 {user}'s Diary Space")

# ======================
# FUNCTIONS
# ======================
def add_entry(text, entry_type):
    c.execute(
        "INSERT INTO diary (username, text, time, type) VALUES (?, ?, ?, ?)",
        (user, text, str(datetime.now()), entry_type)
    )
    conn.commit()

def get_entries(entry_type):
    return c.execute(
        "SELECT id, text, time FROM diary WHERE username=? AND type=? ORDER BY id DESC",
        (user, entry_type)
    ).fetchall()

def delete_entry(entry_id):
    c.execute("DELETE FROM diary WHERE id=?", (entry_id,))
    conn.commit()

def update_entry(entry_id, new_text):
    c.execute("UPDATE diary SET text=? WHERE id=?", (new_text, entry_id))
    conn.commit()

# ======================
# SIMPLE AI SUMMARY (NO API)
# ======================
def simple_summary(entries):
    if not entries:
        return "No entries yet."

    total_words = sum(len(e[1].split()) for e in entries)

    if total_words < 50:
        return "You’ve been quiet lately. Reflecting or just starting out."
    elif total_words < 200:
        return "You’ve been journaling steadily. Mixed thoughts and reflections."
    else:
        return "You’ve been very expressive. A lot of emotions and thoughts recorded."

# ======================
# UI INPUT
# ======================
mode = st.selectbox("Mode:", ["📖 Diary", "💔 Unsent Messages"])

entry = st.text_area("Write here...")

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
# LOAD DATA
# ======================
diary_entries = get_entries("diary")
unsent_entries = get_entries("unsent")

# ======================
# SUMMARY DASHBOARD
# ======================
st.subheader("🧠 Your Mood Summary")

st.info(simple_summary(diary_entries + unsent_entries))

# ======================
# CALENDAR VIEW (SIMPLE)
# ======================
st.subheader("📅 Recent Activity Dates")

dates = [e[2][:10] for e in diary_entries + unsent_entries]
unique_dates = sorted(list(set(dates)), reverse=True)

st.write(unique_dates[:10])

# ======================
# DISPLAY ENTRIES
# ======================
st.subheader("📖 Diary Entries")

for entry_id, text, time in diary_entries:
    st.markdown(f"**{time}**")
    st.write(text)

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"🗑 Delete D{entry_id}"):
            delete_entry(entry_id)
            st.rerun()

    with col2:
        if st.button(f"✏️ Edit D{entry_id}"):
            st.session_state.edit_id = entry_id
            st.session_state.edit_text = text

    st.markdown("---")

st.subheader("💔 Unsent Messages")

for entry_id, text, time in unsent_entries:
    st.markdown(f"**{time}**")
    st.write(f"💔 {text}")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(f"🗑 Delete U{entry_id}"):
            delete_entry(entry_id)
            st.rerun()

    with col2:
        if st.button(f"✏️ Edit U{entry_id}"):
            st.session_state.edit_id = entry_id
            st.session_state.edit_text = text

    st.markdown("---")

# ======================
# EDIT MODE
# ======================
if "edit_id" in st.session_state:
    st.subheader("✏️ Edit Entry")

    new_text = st.text_area("Update entry", st.session_state.edit_text)

    if st.button("Update"):
        update_entry(st.session_state.edit_id, new_text)
        del st.session_state.edit_id
        del st.session_state.edit_text
        st.success("Updated!")
        st.rerun()
    
