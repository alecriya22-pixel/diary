import streamlit as st
import sqlite3
from datetime import datetime
import time

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(page_title="Diary Space", page_icon="🌙")

# ======================
# DB CONFIG (CRASH-PROOF)
# ======================
DB_PATH = "diary.db"

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
# STYLES (DARK AESTHETIC)
# ======================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Indie+Flower&family=Caveat:wght@400;600&display=swap');

.stApp {
    background-color: #0b0b10;
    color: #e6e6e6;
}

h1, h2, h3 {
    color: #c9a7ff;
    font-family: 'Caveat', cursive;
}

.stTextArea textarea {
    font-family: 'Indie Flower', cursive !important;
    font-size: 18px !important;
    background-color: #151522 !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    border: 1px solid #2c2c3a !important;
}

.stButton button {
    background-color: #7c5cff;
    color: white;
    border-radius: 10px;
}

.stButton button:hover {
    background-color: #9a7bff;
}
</style>
""", unsafe_allow_html=True)

# ======================
# AUTH SYSTEM
# ======================
if "user" not in st.session_state:
    st.session_state.user = None

def register_user(username, password):
    conn = get_conn()
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (?, ?)", (username, password))
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
        (username, password)
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
                st.error("Username already exists")

    st.stop()

# ======================
# USER
# ======================
user = st.session_state.user
st.title(f"🌙 {user}'s Diary Space")

# ======================
# SAFE DB FUNCTIONS (WITH RETRY)
# ======================
def add_entry(user, text, entry_type):
    for _ in range(3):
        try:
            conn = get_conn()
            c = conn.cursor()

            c.execute(
                "INSERT INTO diary (username, text, time, type) VALUES (?, ?, ?, ?)",
                (user, text, str(datetime.now()), entry_type)
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
    for _ in range(3):
        try:
            conn = get_conn()
            c = conn.cursor()

            c.execute("DELETE FROM diary WHERE id=?", (entry_id,))
            conn.commit()
            conn.close()
            return

        except sqlite3.OperationalError:
            time.sleep(0.2)

def update_entry(entry_id, new_text):
    for _ in range(3):
        try:
            conn = get_conn()
            c = conn.cursor()

            c.execute("UPDATE diary SET text=? WHERE id=?", (new_text, entry_id))
            conn.commit()
            conn.close()
            return

        except sqlite3.OperationalError:
            time.sleep(0.2)

# ======================
# INPUT UI
# ======================
mode = st.selectbox(
    "Mode:",
    ["📖 Diary", "💔 Unsent Messages", "💫 Showcase Mode"]
)

entry = st.text_area("Write here...")

if st.button("Save ✨"):
    if entry.strip():
        if mode.startswith("💔"):
            add_entry(user, entry, "unsent")
        elif mode.startswith("💫"):
            add_entry(user, entry, "showcase")
        else:
            add_entry(user, entry, "diary")

        st.success("Saved!")
        st.rerun()

st.divider()

# ======================
# DISPLAY FUNCTION
# ======================
def show_entries(title, entries, tag):
    st.subheader(title)

    for entry_id, text, time in entries:
        st.markdown(f"""
        <div style="
            background:#151522;
            padding:15px;
            border-radius:12px;
            border:1px solid #2c2c3a;
            margin-bottom:10px;
        ">
            <small style="color:#aaa">{time}</small><br><br>
            {text}
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"🗑 Delete {tag}{entry_id}"):
                delete_entry(entry_id)
                st.rerun()

        with col2:
            if st.button(f"✏️ Edit {tag}{entry_id}"):
                st.session_state.edit_id = entry_id
                st.session_state.edit_text = text

# ======================
# LOAD DATA
# ======================
diary_entries = get_entries(user, "diary")
unsent_entries = get_entries(user, "unsent")
showcase_entries = get_entries(user, "showcase")

# ======================
# SHOW SECTIONS
# ======================
show_entries("📖 Diary Entries", diary_entries, "D")
show_entries("💔 Unsent Messages", unsent_entries, "U")
show_entries("💫 Showcase Mode", showcase_entries, "S")

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
