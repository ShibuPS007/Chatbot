import streamlit as st
import requests

BACKEND = "https://chatbot-backend-latest-7ncz.onrender.com"



st.set_page_config(layout="wide")
st.title("🤖 Stark AI")

# -------- LOGIN / SIGNUP --------

if "user_id" not in st.session_state:

    tab1, tab2 = st.tabs(["Login", "Signup"])

    with tab1:
        st.subheader("Login")
        email = st.text_input("Email (login)")
        password = st.text_input("Password (login)", type="password")

        if st.button("Login"):

            res = requests.post(
                f"{BACKEND}/login",
                json={"email": email, "password": password}
            )

            data = res.json()

            if "error" in data:
                st.error(data["error"])
                st.stop()

            st.session_state.user_id = data["user_id"]
            st.session_state.token = data["access_token"]
            st.success("Logged in!")
            st.rerun()

    with tab2:
        st.subheader("Signup")
        email = st.text_input("Email (signup)")
        password = st.text_input("Password (signup)", type="password")

        if st.button("Signup"):

            res = requests.post(
                f"{BACKEND}/signup",
                json={"email": email, "password": password}
            )

            data = res.json()

            if "error" in data:
                st.error(data["error"])
                st.stop()

            st.session_state.user_id = data["user_id"]
            st.session_state.token = data["access_token"]
            st.success("Account created!")
            st.rerun()

    st.stop()

# -------- SIDEBAR --------

headers = {"token": st.session_state.token}

with st.sidebar:
    st.write(f"User: {st.session_state.user_id}")

    if st.button("🚀 New Chat"):
        res = requests.post(
        f"{BACKEND}/chats",
        json={"title": "New Chat"},   # ✅ important change
        headers=headers
        )

        data = res.json()

    # Safety guard (prevents KeyError forever)
        if "id" not in data:
            st.error(f"Backend error: {data}")
            st.stop()

        st.session_state.chat_id = data["id"]
        st.rerun()

    res = requests.get(
        f"{BACKEND}/chats",
        headers=headers
    )

    chats = res.json()

    for chat in chats:
        if st.button(chat["title"], key=chat["id"]):
            st.session_state.chat_id = chat["id"]
            st.rerun()

# -------- MAIN CHAT UI --------

if "chat_id" not in st.session_state:
    st.info("Select or create a chat from the sidebar")
    st.stop()

res = requests.get(
    f"{BACKEND}/chats/{st.session_state.chat_id}",
    headers=headers
)

messages = res.json()

for msg in messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask something...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    res = requests.post(
        f"{BACKEND}/chats/{st.session_state.chat_id}",
        json={"content": user_input},
        headers=headers
    )

    reply = res.json()["reply"]

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.rerun()
