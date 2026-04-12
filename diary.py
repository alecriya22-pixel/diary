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
# DATABASE
# ======================
DB_PATH = "/tmp/diary.db"

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

    c.execute("""
    CREATE TABLE IF NOT EXISTS user_security (
        username TEXT PRIMARY KEY,
        private_pin TEXT
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
# SESSION STATE
# ======================
if "user" not in st.session_state:
    st.session_state.user = None

if "private_unlocked" not in st.session_state:
    st.session_state.private_unlocked = False

if "mode" not in st.session_state:
    st.session_state.mode = "📖 Diary"

# ======================
# AUTH
# ======================

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
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    return user

# ======================
# PRIVATE SECURITY
# ======================

def set_private_pin(user, pin):
    conn = get_conn()
    c = conn.cursor()
    c.execute("REPLACE INTO user_security VALUES (?, ?)",
              (user, hash_password(pin)))
    conn.commit()
    conn.close()


def check_private_pin(user, pin):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT private_pin FROM user_security WHERE username=?", (user,))
    data = c.fetchone()
    conn.close()

    if not data:
        return False

    return data[0] == hash_password(pin)

# ======================
# LOGIN
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
    st.session_state.private_unlocked = False
    st.session_state.mode = "📖 Diary"
    st.rerun()

# ======================
# DB FUNCTIONS
# ======================

def add_entry(user, text, entry_type):
    conn = get_conn()
    c = conn.cursor()
    c.execute("INSERT INTO diary (username, text, time, type) VALUES (?, ?, ?, ?)",
              (user, text, datetime.now().isoformat(), entry_type))
    conn.commit()
    conn.close()


def get_entries(user, entry_type):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, text, time FROM diary WHERE username=? AND type=? ORDER BY id DESC",
              (user, entry_type))
    data = c.fetchall()
    conn.close()
    return data


def delete_entry(entry_id):
    conn = get_conn()
    c = conn.cursor()
    c.execute("DELETE FROM diary WHERE id=?", (entry_id,))
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

# ======================
# MODE SELECTOR
# ======================

st.session_state.mode = st.selectbox(
    "Mode:",
    ["📖 Diary", "💔 Unsent", "💫 Showcase", "🔐 Private"]
)

# ======================
# PRIVATE GATE (FULL SCREEN LOCK FLOW)
# ======================

if st.session_state.mode == "🔐 Private" and not st.session_state.private_unlocked:
    st.title("🔐 Private Vault Locked")
    st.info("Enter your password to access your private thoughts.")

    pin = st.text_input("Private Password", type="password")

    if st.button("Unlock Vault"):
        if check_private_pin(user, pin):
            st.session_state.private_unlocked = True
            st.rerun()
        else:
            st.error("Incorrect password")

    st.stop()

# lock again button
if st.session_state.mode == "🔐 Private" and st.session_state.private_unlocked:
    if st.button("🔒 Lock Again"):
        st.session_state.private_unlocked = False
        st.rerun()

# ======================
# INPUT
# ======================
entry = st.text_area("Write here...", placeholder="What's on your mind?")

if st.button("Save ✨"):
    if entry.strip():
        if st.session_state.mode == "💔 Unsent":
            add_entry(user, entry, "unsent")
        elif st.session_state.mode == "💫 Showcase":
            add_entry(user, entry, "showcase")
        elif st.session_state.mode == "🔐 Private":
            add_entry(user, entry, "private")
        else:
            add_entry(user, entry, "diary")
        st.rerun()

st.divider()

# ======================
# DISPLAY
# ======================

def show(title, entries, tag):
    st.subheader(title)
    for eid, text, time_val in entries:
        st.markdown(f"""
        <div style='background:#151522;padding:15px;border-radius:12px;margin-bottom:10px;'>
        <small>{time_val}</small><br><br>{text}
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑 Delete", key=f"del_{tag}_{eid}"):
                delete_entry(eid)
                st.rerun()

# fetch entries

diary = get_entries(user, "diary")
unsent = get_entries(user, "unsent")
showcase = get_entries(user, "showcase")
private = get_entries(user, "private")

show("📖 Diary", diary, "D")
show("💔 Unsent", unsent, "U")
show("💫 Showcase", showcase, "S")

# private only after unlock
if st.session_state.mode == "🔐 Private" and st.session_state.private_unlocked:
    st.subheader("🔐 Private Vault")
    for eid, text, time_val in private:
        st.markdown(f"""
        <div style='background:#111;padding:15px;border-radius:12px;margin-bottom:10px;'>
        <small>{time_val}</small><br><br>{text}
        </div>
        """, unsafe_allow_html=True)

        if st.button("🗑 Delete", key=f"delP_{eid}"):
            delete_entry(eid)
            st.rerun()

# ======================
# EDIT
# ======================
if "edit_id" in st.session_state:
    st.subheader("✏️ Edit")
    new = st.text_area("Update", st.session_state.edit_text)
    if st.button("Update"):
        conn = get_conn()
        c = conn.cursor()
        c.execute("UPDATE diary SET text=? WHERE id=?",
                  (new, st.session_state.edit_id))
        conn.commit()
        conn.close()
        del st.session_state.edit_id
        del st.session_state.edit_text
        st.rerun()
