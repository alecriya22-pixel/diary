import streamlit as st
import os
import random
from datetime import date

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="For Mary ❤️",
    page_icon="❤️",
    layout="wide"
)

# -----------------------------
# Load CSS
# -----------------------------
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -----------------------------
# Floating Hearts
# -----------------------------
hearts = ""

for _ in range(50):
    hearts += f"""
    <div class="heart"
        style="
        left:{random.randint(0,100)}%;
        animation-duration:{random.randint(8,15)}s;
        animation-delay:{random.randint(0,10)}s;
        font-size:{random.randint(18,35)}px;">
        ❤️
    </div>
    """

st.markdown(
f"""
<div class="heart-container">
{hearts}
</div>
""",
unsafe_allow_html=True
)

# -----------------------------
# Welcome
# -----------------------------
st.info("💖 Welcome Mary. I made this little website especially for you.")

# -----------------------------
# Hero Section
# -----------------------------
st.markdown("""
<div class='hero'>
<h1>❤️ Dear Mary ❤️</h1>

<h3>Distance may keep us apart, but it has never stopped you from becoming someone incredibly special to me.</h3>

<p>
This little website is my way of reminding you how grateful I am that our paths crossed.
I hope it brings a smile to your face the same way you always bring one to mine.
</p>

</div>
""", unsafe_allow_html=True)

st.balloons()

# -----------------------------
# Relationship Counter
# -----------------------------
st.header("❤️ Our Journey")

start_date = date(2026, 4, 1)   # Change if needed
today = date.today()

days = (today - start_date).days

st.metric("Days Since Our Journey Began", days)

st.write("""
Even though we haven't met in person yet,

every conversation,
every laugh,
every late-night chat,
and every shared dream
has made me appreciate you more.

Distance may separate us physically,
but it has never stopped us from building something meaningful.

I'm thankful for every moment we've shared
and excited for all the memories still waiting for us.

❤️
""")

# -----------------------------
# Love Letter
# -----------------------------
st.header("💌 A Letter For You")

st.write("""
Dear Mary,

I never imagined that someone I met online
could become such an important part of my life.

You've brought happiness into ordinary days,
hope into difficult ones,
and excitement for what the future might hold.

Thank you for your kindness,
your patience,
your beautiful heart,
and simply for being yourself.

No matter how many miles are between us,
I always enjoy hearing from you.

I truly hope that one day
we'll finally meet,
share a laugh,
and create memories together.

Until then,
I'll continue appreciating every message,
every conversation,
and every smile you share with me.

❤️ Yours Always ❤️
""")

# -----------------------------
# Things I Like About You
# -----------------------------
st.header("🌹 Things I Like About You")

likes = [
    "😊 Your beautiful smile",
    "💬 Our conversations",
    "😂 Your sense of humor",
    "❤️ Your kind heart",
    "✨ Your personality",
    "🌸 The peace you bring into my life",
    "🌞 The way you brighten my day",
    "💖 Simply being you"
]

for item in likes:
    st.success(item)

# -----------------------------
# Favorite Quote
# -----------------------------
st.markdown("> **'Distance means so little when someone means so much.'** ❤️")

# -----------------------------
# Looking Forward
# -----------------------------
st.header("🌍 Looking Forward")

st.write("""
The best part of our story hasn't happened yet.

I look forward to the day
we finally meet,
laugh together,
explore new places,
and create beautiful memories.

Until then,
I'm grateful for every conversation we share
because every one of them becomes another reason to smile.

❤️
""")

# -----------------------------
# Surprise
# -----------------------------
st.header("🎁 One Last Surprise")

if st.button("Open Your Surprise ❤️"):

    st.snow()
    st.balloons()

    st.markdown("""
# ❤️ Dear Mary ❤️

Thank you for coming into my life.

You have given me countless reasons to smile,
even from miles away.

I hope this little website reminds you
just how much you mean to me.

No matter where life takes us,
I'll always be grateful that our paths crossed.

❤️ You're Amazing ❤️
""")

# -----------------------------
# Final Message
# -----------------------------
st.markdown("---")

st.success("💖 Thank you for visiting my little corner of the internet.")

st.markdown(
"""
<center>

<h3>Made with ❤️ just for Mary</h3>

<p>
No matter the distance,
you're always close to my heart.
</p>

</center>
""",
unsafe_allow_html=True
)
