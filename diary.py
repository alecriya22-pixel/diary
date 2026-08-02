import streamlit as st
import os
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
# Hero Section
# -----------------------------
st.markdown("""
<div class='hero'>
    <h1>❤️ Dear Mary ❤️</h1>

    <h3>
        This little website is just for you.
    </h3>

    <p>
        I wanted to create something special that reminds you
        how much you mean to me.
    </p>
</div>
""", unsafe_allow_html=True)

st.balloons()

# -----------------------------
# Relationship Counter
# -----------------------------
st.header("❤️ Our Journey")

start_date = date(2025, 1, 1)   # Change this to when your journey started
today = date.today()

days = (today - start_date).days

st.metric("Days Since Our Journey Began", days)

st.write("""
Even though we haven't met in person yet,
you've become someone very special to me.

Every conversation,
every laugh,
every late-night chat,
and every moment we've shared
has brought us closer.

Distance may separate us,
but it has never stopped me from appreciating you.

I look forward to the day
we finally get to meet.

Until then,
I'll treasure every moment we share.
❤️
""")

# -----------------------------
# Love Letter
# -----------------------------
st.header("💌 A Letter For You")

st.write("""
Dear Mary,

I never expected that someone I met online
could have such a positive impact on my life.

You make my days brighter,
my heart happier,
and my future feel more exciting.

Thank you for your kindness,
your patience,
your beautiful personality,
and for always being yourself.

No matter how many miles separate us,
I appreciate every conversation we have.

I'm excited for all the memories we'll create in the future.

Until then,
I'll keep smiling every time I see your name appear on my screen.

❤️ Yours Always ❤️
""")

# -----------------------------
# Things I Like About You
# -----------------------------
st.header("🌹 Things I Like About You")

likes = [
    "😊 Your beautiful smile",
    "❤️ Your kind heart",
    "😂 Your sense of humor",
    "💬 Our conversations",
    "🌸 Your caring nature",
    "✨ Your personality",
    "🌞 The happiness you bring into my life",
    "💖 Simply being you"
]

for item in likes:
    st.success(item)

# -----------------------------
# Future Dreams
# -----------------------------
st.header("🌍 Looking Forward")

st.write("""
One day,
I hope we get to meet in person,
explore new places together,
laugh until our stomachs hurt,
and create beautiful memories together.

Until that day comes,
I'm grateful that I met you.
❤️
""")

# -----------------------------
# Surprise Section
# -----------------------------
st.header("🎁 One Last Surprise")

if st.button("Open Your Surprise ❤️"):
    st.snow()

    st.markdown("""
    ## ❤️ Dear Mary ❤️

    Thank you for being part of my life.

    No matter the distance,
    you've given me countless reasons to smile.

    I hope this little website reminds you
    how much you mean to me.

    ❤️ You're Amazing ❤️
    """)

    st.balloons()

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")

st.markdown(
    "<center><h4>Made with ❤️ just for Mary</h4></center>",
    unsafe_allow_html=True
)
