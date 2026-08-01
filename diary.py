import streamlit as st
from PIL import Image
import base64
import os

st.set_page_config(
    page_title="For Mary ❤️",
    page_icon="❤️",
    layout="wide"
)

# Load CSS
if os.path.exists("style.css"):
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Background Music
music_file = "music/stereo_hearts.mp3"

if os.path.exists(music_file):
    with open(music_file, "rb") as f:
        data = f.read()

    b64 = base64.b64encode(data).decode()

    st.markdown(
        f"""
        <audio autoplay loop controls>
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """,
        unsafe_allow_html=True
    )

# Hero Section
st.markdown(
"""
<div class="hero">
<h1>❤️ Dear Mary ❤️</h1>

<h2>You are my sunshine, my happiness, and my forever.</h2>

<p>
Every single day with you is a blessing.
This little website is only a tiny reminder
of how much I love you.
</p>
</div>
""",
unsafe_allow_html=True
)

st.balloons()

# Love Letter
st.header("💌 A Letter For You")

st.write("""
Dear Mary,

You make every ordinary day feel extraordinary.

Thank you for your love,
your kindness,
your smile,
and for always believing in me.

You are my best friend,
my peace,
and my greatest blessing.

I love you today,
tomorrow,
and forever.

❤️
""")

# Gallery
st.header("📸 Our Beautiful Memories")

photos = [
    "images/photo1.jpg",
    "images/photo2.jpg",
    "images/photo3.jpg",
    "images/photo4.jpg"
]

cols = st.columns(2)

for i, photo in enumerate(photos):
    if os.path.exists(photo):
        cols[i % 2].image(photo, use_container_width=True)

# Reasons
st.header("❤️ Reasons I Love You")

reasons = [
    "Your smile 😊",
    "Your beautiful heart ❤️",
    "Your kindness",
    "Your laughter",
    "Your support",
    "Your hugs",
    "Your intelligence",
    "Everything about you."
]

for reason in reasons:
    st.success(reason)

# Surprise
st.header("🎁 Surprise")

if st.button("Click Here ❤️"):
    st.snow()

    st.markdown(
    """
    ## ❤️ Happy Special Occasion ❤️

    Mary,

    Thank you for making my life beautiful.

    I will always choose you.

    **Forever Yours ❤️**
    """
    )
