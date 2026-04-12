import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import time

# ======================
# PAGE CONFIG
# ======================
st.set_page_config(page_title="Diary Space", page_icon="🌙")

# ======================
# DATABASE (CRASH-PROOF)
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
# STYLES
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

.card {
    background:#151522;
    padding:15px;
    border-radius:12px;
    border:1px solid #2c2c3a;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# ======================
# AUTH
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
                st.error("Username exists")

    st.stop()

# ======================
# USER
# ======================
user = st.session_state.user
st.title(f"🌙 {user}'s Diary Space")

# ======================
# DB FUNCTIONS (SAFE + RETRY)
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
# EMOTION + SUMMARY
# ======================
def detect_emotion(text):
    text = text.lower()

    happy = ["happy", "good", "great", "love", "excited", "calm"]
    sad = ["sad", "hurt", "lonely", "miss", "bad"]
    stress = ["stress", "anxious", "overthink", "worried"]

    score = {"happy":0, "sad":0, "stress":0}

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
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT text, time FROM diary WHERE username=?", (user,))
    data = c.fetchall()
    conn.close()

    week_ago = datetime.now() - timedelta(days=7)

    emotions = {"happy":0, "sad":0, "stress":0, "neutral":0}

    for text, time_str in data:
        try:
            t = datetime.strptime(time_str.split(".")[0], "%Y-%m-%d %H:%M:%S")
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

# ======================
# CALENDAR
# ======================
def get_dates(user):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT time FROM diary WHERE username=?", (user,))
    data = c.fetchall()
    conn.close()
    return data

# ======================
# UI INPUT
# ======================
mode = st.selectbox(
    "Mode:",
    ["📖 Diary", "💔 Unsent", "💫 Showcase"]
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

        st.rerun()

st.divider()

# ======================
# SUMMARY + CALENDAR
# ======================
st.subheader("🧠 Weekly Summary")
st.info(weekly_summary(user))

st.subheader("📅 Calendar (Dates with entries)")

dates = [d[0].split(" ")[0] for d in get_dates(user)]
st.write(sorted(list(set(dates)), reverse=True)[:10])

# ======================
# DISPLAY
# ======================
def show(title, entries, tag):
    st.subheader(title)

    for eid, text, time in entries:
        st.markdown(f"""
        <div class="card">
        <small>{time}</small><br><br>
        {text}
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"🗑 {tag}{eid}"):
                delete_entry(eid)
                st.rerun()

        with col2:
            if st.button(f"✏️ {tag}{eid}"):
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
