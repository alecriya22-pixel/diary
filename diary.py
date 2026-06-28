import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="I'm Sorry ❤️",
    page_icon="💔",
    layout="centered"
)

st.markdown("""
<style>
.stApp{
    background:linear-gradient(135deg,#fff5f7,#ffe3ec);
}
.title{
    text-align:center;
    color:#ff4d6d;
    font-size:55px;
    font-weight:bold;
}
.message{
    background:white;
    padding:25px;
    border-radius:20px;
    box-shadow:0 8px 20px rgba(0,0,0,.15);
    font-size:20px;
    line-height:1.8;
}
.stButton>button{
    background:#ff4d6d;
    color:white;
    border-radius:30px;
    padding:12px 25px;
    border:none;
    font-size:18px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>💔 I'm Sorry, Carizon ❤️</div>",
unsafe_allow_html=True)

st.write("")

st.image("assets/photos/her1.jpg", use_container_width=True)

st.markdown("""
<div class='message'>

Dear Carizon,

I know I hurt you.

I'm not making this website to erase what happened or to pretend everything is okay.

I'm making it because you deserve a genuine apology.

I'm sorry for my words, my actions, and the way I made you feel.

You mean so much to me, and the last thing I ever wanted was to become the reason you were hurting.

We've only just begun this journey together, and I don't want our first chapter to be remembered for a mistake.

I can't promise to be perfect.

But I can promise to listen better, communicate better, and do better.

Whether you forgive me today or need time, I'll respect that.

Thank you for reading this.

❤️
Love,
Carino

</div>
""", unsafe_allow_html=True)

st.write("")

if st.button("❤️ Can you forgive me?"):
    st.balloons()
    st.success("No matter what happens, thank you for giving me your time.")
