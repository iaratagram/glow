import streamlit as st
import requests
import openai

# -----------------------------------
# Authentication
# -----------------------------------
def authenticate(username: str, password: str) -> bool:
    users = st.secrets["credentials"]["users"]
    user_password = users.get(username)
    if user_password and user_password == password:
        return True
    return False

# Initialize auth state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Login UI
if not st.session_state.authenticated:
    st.title("🔒 Please log in to continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.error("❌ Invalid username or password.")
    st.stop()

# -----------------------------------
# Sidebar: User & Navigation
# -----------------------------------
st.sidebar.title(f"👤 {st.session_state.username}")

# API setup
history_api = "https://api.irister.com/chat/history"
api_key = st.secrets["IRISTER_API_KEY"]
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

# Fetch conversation list
conversations = []
try:
    resp = requests.get(history_api, headers=headers, timeout=5)
    resp.raise_for_status()
    conversations = resp.json()
except Exception:
    st.sidebar.error("Unable to load chat history.")

# Initialize mode
if "mode" not in st.session_state:
    st.session_state.mode = "new"

# New Conversation button in sidebar
def start_new():
    st.session_state.mode = "new"
    st.session_state.system_set = False
    st.session_state.pop("conversation_id", None)

st.sidebar.button("➕ New Conversation", on_click=start_new)

# Conversation selector
titles = [conv.get("title", conv.get("conversation_id")) for conv in conversations]
selected_conv_id = None
if titles:
    def select_history():
        st.session_state.mode = "history"
        st.session_state.pop("conversation_id", None)
    st.sidebar.radio("Chat History", titles, key="conv_selected", on_change=select_history)
    sel_title = st.session_state.conv_selected
    for conv in conversations:
        if conv.get("title", conv.get("conversation_id")) == sel_title:
            selected_conv_id = conv.get("conversation_id")
            break

# -----------------------------------
# Main Area: Content
# -----------------------------------
if st.session_state.mode == "new":
    st.title("🆕 New Conversation")
    # Step 1: Set system prompt
    if not st.session_state.get("system_set", False):
        prompt = st.text_area("Set system prompt for this conversation:", height=150)
        if st.button("Start Conversation") and prompt.strip():
            st.session_state.system_prompt = prompt
            st.session_state.messages = [{"role": "system", "content": prompt}]
            st.session_state.system_set = True
            st.experimental_rerun()
        else:
            st.info("Please enter a system prompt to begin.")
    else:
        # Display system prompt and messages
        st.header("System Prompt:")
        st.write(f"*{st.session_state.system_prompt}*")
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        # Chat input
        user_input = st.chat_input("Type your message...")
        if user_input:
            # On first user message, create conversation thread in history
            if "conversation_id" not in st.session_state:
                data = {"title": st.session_state.system_prompt}
                try:
                    create_resp = requests.post(history_url, headers=headers, json=data, timeout=5)
                    create_resp.raise_for_status()
                    conv_info = create_resp.json()  # expects {"conversation_id": "..."}
                    st.session_state.conversation_id = conv_info.get("conversation_id")
                except Exception:
                    st.error("Failed to create conversation thread.")

            # Append and display user message
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)

            # Call OpenAI
            openai.api_key = st.secrets["openai"]["api_key"]
            with st.spinner("Assistant is typing..."):
                res = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=st.session_state.messages
                )
                reply = res.choices[0].message.content

            # Append and display assistant message
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)
            
            # Optionally, push message to history API
            if st.session_state.get("conversation_id"):
                msg_url = f"{history_url}/{st.session_state.conversation_id}/messages"
                try:
                    requests.post(msg_url, headers=headers, json={"role": "user", "content": user_input})
                    requests.post(msg_url, headers=headers, json={"role": "assistant", "content": reply})
                except Exception:
                    st.warning("Warning: failed to sync messages to history API.")

else:
    # Display selected conversation
    st.title(f"💬 Conversation: {sel_title}")
    if selected_conv_id:
        msgs = []
        conv_url = f"{history_url}/{selected_conv_id}/messages"
        try:
            resp = requests.get(conv_url, headers=headers, timeout=5)
            resp.raise_for_status()
            msgs = resp.json()
        except Exception:
            st.error("Unable to load messages.")
        for msg in msgs:
            st.chat_message(msg["role"]).write(msg["content"])
    else:
        st.info("No conversations available.")