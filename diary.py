import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import time
import hashlib
import os

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(page_title="Diary Space", page_icon="🌙")

# ======================
# DATABASE (CLOUD SAFE)
# ======================
DB_PATH = "/tmp/diary.db"

# Ensure DB file exists
if not os.path.exists(DB_PATH):
    open(DB_PATH, "w").close()


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=3000")
    return conn


def init_db():
    conn = get_conn()
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
    conn.close()


init_db()

# ======================
# SECURITY
# ======================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ======================
# AUTH
# ======================
if "user" not in st.session_state:
    st.session_state.user = None


def register_user(username, password):
    try:
        conn = get_conn()
        init_db()
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def login_user(username, password):
    conn = get_conn()
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )

    user = c.fetchone()
    conn.close()
    return user

# ======================
# LOGIN PAGE
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
                st.success("Account created!")
            else:
                st.error("Username exists")

    st.stop()

# ======================
# USER
# ======================
user = st.session_state.user
st.title(f"🌙 {user}'s Diary Space")

if st.button("Logout"):
    st.session_state.user = None
    st.rerun()

# ======================
# DB FUNCTIONS
# ======================

def add_entry(user, text, entry_type):
    for _ in range(3):
        try:
            conn = get_conn()
            init_db()
            c = conn.cursor()

            c.execute(
                "INSERT INTO diary (username, text, time, type) VALUES (?, ?, ?, ?)",
                (user, text, datetime.now().isoformat(), entry_type)
            )

            conn.commit()
            conn.close()
            return
        except sqlite3.OperationalError:
            time.sleep(0.2)


def get_entries(user, entry_type):
    for _ in range(3):
        try:
            conn = get_conn()
            init_db()
            c = conn.cursor()

            c.execute(
                "SELECT id, text, time FROM diary WHERE username=? AND type=? ORDER BY id DESC",
                (user, entry_type)
            )

            data = c.fetchall()
            conn.close()
            return data
        except sqlite3.OperationalError:
            time.sleep(0.2)

    return []


def delete_entry(entry_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM diary WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()


def update_entry(entry_id, new_text):
    conn = get_conn()
    c = conn.cursor()
    c.execute("UPDATE diary SET text=? WHERE id=?", (new_text, entry_id))
    conn.commit()
    conn.close()

# ======================
# EMOTION
# ======================

def detect_emotion(text):
    text = text.lower()

    happy = ["happy", "good", "great", "love", "excited", "calm", "joy"]
    sad = ["sad", "hurt", "lonely", "miss", "bad", "cry", "tired"]
    stress = ["stress", "anxious", "overthink", "worried", "panic"]

    score = {"happy": 0, "sad": 0, "stress": 0}

    for w in happy:
        if w in text: score["happy"] += 1
    for w in sad:
        if w in text: score["sad"] += 1
    for w in stress:
        if w in text: score["stress"] += 1

    if max(score.values()) == 0:
        return "neutral"

    return max(score, key=score.get)


def weekly_summary(user):
    try:
        conn = get_conn()
        init_db()
        c = conn.cursor()

        c.execute("SELECT text, time FROM diary WHERE username=?", (user,))
        data = c.fetchall()
        conn.close()

        week_ago = datetime.now() - timedelta(days=7)

        emotions = {"happy": 0, "sad": 0, "stress": 0, "neutral": 0}

        for text, time_str in data:
            try:
                t = datetime.fromisoformat(time_str)
                if t >= week_ago:
                    emo = detect_emotion(text)
                    emotions[emo] += 1
            except:
                pass

        dominant = max(emotions, key=emotions.get)

        return f"""
📊 Weekly Emotional Summary

😊 Happy: {emotions['happy']}
😔 Sad: {emotions['sad']}
😰 Stress: {emotions['stress']}
⚪ Neutral: {emotions['neutral']}

🧠 Overall: {dominant.upper()}
"""

    except sqlite3.OperationalError:
        return "No data yet."

# ======================
# UI INPUT
# ======================
mode = st.selectbox(
    "Mode:",
    ["📖 Diary", "💔 Unsent", "💫 Showcase"]
)

entry = st.text_area("Write here...", placeholder="What's on your mind?")

if st.button("Save ✨"):
    if entry.strip():
        if mode.startswith("💔"):
            add_entry(user, entry, "unsent")
        elif mode.startswith("💫"):
            add_entry(user, entry, "showcase")
        else:
            add_entry(user, entry, "diary")

        st.rerun()

st.divider()

# ======================
# SUMMARY
# ======================
st.subheader("🧠 Weekly Summary")
st.info(weekly_summary(user))

# ======================
# DISPLAY
# ======================

def show(title, entries, tag):
    st.subheader(title)

    for eid, text, time_val in entries:
        st.markdown(f"""
        <div style='background:#151522;padding:15px;border-radius:12px;margin-bottom:10px;'>
        <small>{time_val}</small><br><br>
        {text}
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🗑 Delete", key=f"del_{tag}_{eid}"):
                delete_entry(eid)
                st.rerun()

        with col2:
            if st.button("✏️ Edit", key=f"edit_{tag}_{eid}"):
                st.session_state.edit_id = eid
                st.session_state.edit_text = text


diary = get_entries(user, "diary")
unsent = get_entries(user, "unsent")
showcase = get_entries(user, "showcase")

show("📖 Diary", diary, "D")
show("💔 Unsent", unsent, "U")
show("💫 Showcase", showcase, "S")

# ======================
# EDIT
# ======================
if "edit_id" in st.session_state:
    st.subheader("✏️ Edit")

    new = st.text_area("Update", st.session_state.edit_text)

    if st.button("Update"):
        update_entry(st.session_state.edit_id, new)
        del st.session_state.edit_id
        del st.session_state.edit_text
        st.rerun()
