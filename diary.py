import streamlit as st
import os
from datetime import date

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="For Mary ❤️",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# Load CSS
# -----------------------------
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -----------------------------
# Welcome Banner
# -----------------------------
st.info("💖 Welcome Mary. This little corner of the internet was made just for you.")

# -----------------------------
# Hero Section
# -----------------------------
st.markdown("""
<div class="hero">

<h1>❤️ Dear Mary ❤️</h1>

<h3>
Sometimes the most meaningful connections begin in the most unexpected ways.
</h3>

<p>
This website is my little gift to you.

A reminder that even though there's distance between us,
you've become someone I genuinely appreciate,
care about,
and look forward to talking to every day.

I hope this brings a smile to your face.
</p>

<div class="pulse-heart">❤️</div>

</div>
""", unsafe_allow_html=True)

st.balloons()

# -----------------------------
# Journey Counter
# -----------------------------
st.header("❤️ Our Journey")

start_date = date(2026, 4, 1)   # Change to your actual date

today = date.today()

days = (today - start_date).days

col1, col2 = st.columns(2)

with col1:
    st.metric("Days Since Our Journey Began", days)

with col2:
    st.metric("Conversations Shared", "Countless 💬")

st.write("""

Even though we've never met in person,

you've become someone I genuinely look forward to hearing from.

Every conversation,

every joke,

every late-night chat,

and every dream we've talked about

has made this journey special.

Distance may separate us physically,

but it has never stopped us from building something meaningful.

I'm grateful for every single day.

❤️

""")

# -----------------------------
# Love Letter
# -----------------------------
st.header("💌 A Letter For You")

st.markdown("""

Dear **Mary**,

Sometimes I stop and think about how strange life can be.

Out of all the people in the world,

our paths crossed.

And somehow,

you've become someone who makes ordinary days feel brighter.

Thank you for your kindness.

Thank you for your patience.

Thank you for every laugh we've shared.

Thank you for simply being yourself.

I don't know exactly what the future holds,

but I do know this—

meeting you has already made my life better.

Until the day we finally meet,

I'll keep looking forward to every message,

every conversation,

and every smile you share with me.

❤️ **Yours Always**

""")
# -----------------------------
# Things I Like About You
# -----------------------------
st.header("🌹 Things I Like About You")

likes = [
    "😊 Your beautiful smile",
    "💬 The way our conversations never feel forced",
    "😂 Your amazing sense of humor",
    "❤️ Your kind heart",
    "🌸 Your caring nature",
    "✨ Your personality",
    "🌞 The happiness you bring into my day",
    "🤍 The way you make distance feel smaller",
    "🌍 Your dreams and ambitions",
    "💖 Simply being yourself"
]

for item in likes:
    st.success(item)

st.markdown("---")

# -----------------------------
# Quote
# -----------------------------
st.markdown(
"""
<div class="quote-box">

<h3>💭 A Little Thought</h3>

<p>

"Distance means so little when someone means so much."

</p>

</div>
""",
unsafe_allow_html=True
)

# -----------------------------
# Looking Forward
# -----------------------------
st.header("🌍 Looking Forward")

st.write("""

The best part of our story
hasn't happened yet.

One day,

I hope we'll finally get to meet,
share a meal together,
walk side by side,
and laugh about how it all started.

Until then,

I'll continue appreciating every conversation,
every good morning,
every good night,
and every little moment we share.

Because every day brings us one step closer.

❤️

""")

st.markdown("---")

# -----------------------------
# Little Promise
# -----------------------------
st.header("🤍 A Small Promise")

st.info("""

No matter how busy life gets,

I'll always try to make time for you.

I'll always appreciate your kindness.

And I'll never stop cheering you on
to become everything you dream of becoming.

""")

# -----------------------------
# Surprise
# -----------------------------
st.header("🎁 One Last Surprise")

if st.button("Click Here ❤️"):

    st.snow()
    st.balloons()

    st.markdown(
    """
    <div class="surprise-card">

    <h1>❤️ Dear Mary ❤️</h1>

    <h3>

    Thank you.

    </h3>

    <p>

    Thank you for being part of my life.

    Thank you for every smile.

    Thank you for every conversation.

    Thank you for making ordinary days feel special.

    I hope this little website reminds you
    that you are appreciated more than you know.

    ❤️

    </p>

    </div>
    """,
    unsafe_allow_html=True
    )

    st.success("💖 You make my world a little brighter every day.")

# -----------------------------
# Final Message
# -----------------------------
st.markdown("---")

st.markdown(
"""
<div class="ending">

<h2>❤️ Until Next Time ❤️</h2>

<p>

Every story starts somewhere.

I'm really glad ours started with a simple conversation.

Here's to many more.

🌸

</p>

</div>
""",
unsafe_allow_html=True
)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")

st.caption("Made with ❤️ especially for Mary.")
st.markdown("---")
