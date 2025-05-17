import streamlit as st
import irister_utils

# -----------------------------------
# Authentication
# -----------------------------------
def authenticate(username: str, password: str) -> bool:
    users = st.secrets["credentials"]["users"]
    return users.get(username) == password

# Initialize auth state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 Please log in to continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.rerun()
        else:
            st.error("❌ Invalid username or password.")
    st.stop()

# -----------------------------------
# Sidebar: User & Navigation
# -----------------------------------
st.sidebar.title(f"👤 {st.session_state.username}")

# Fetch conversation list
try:
    conversations = irister_utils.glow_get_all_conversations(st.session_state.username)
except Exception:
    st.sidebar.error("Unable to load chat history.")
    conversations = []

# Callback: Reset to new conversation
def reset_to_new():
    st.session_state.mode = "new"
    st.session_state.system_set = False
    st.session_state.pop("conversation_id", None)
    st.session_state.pop("messages", None)

# Callback: When selecting existing convo
def select_history():
    st.session_state.mode = "history"
    st.session_state.system_set = True
    # conversation_id already set via sidebar selection
    st.session_state.pop("messages", None)

# Initialize mode
def init_mode():
    if "mode" not in st.session_state:
        reset_to_new()
init_mode()

# Sidebar controls
st.sidebar.button("➕ New Conversation", on_click=reset_to_new, use_container_width=True)

# 添加一个分隔线
st.sidebar.markdown("---")
st.sidebar.markdown("### 💬 Conversation History")

titles = [conv.get("title") or conv.get("conversation_id") for conv in conversations]
# 为每个对话创建一个可点击的按钮
for title in titles:
    # 创建两列布局：标记列和按钮列
    cols = st.sidebar.columns([1, 9])
    # 标记列
    with cols[0]:
        if st.session_state.get("conv_selected") == title:
            st.markdown("▶️")
        else:
            st.markdown("&nbsp;")
    # 按钮列
    with cols[1]:
        if st.button(
            f"{title}",
            key=f"history_{title}",
            use_container_width=True,
        ):
            st.session_state.conv_selected = title
            # 设置conversation_id
            for conv in conversations:
                if (conv.get("title") or conv.get("conversation_id")) == title:
                    st.session_state.conversation_id = conv.get("conversation_id")
                    break
            select_history()

# -----------------------------------
# Main Area: Content
# -----------------------------------
if st.session_state.mode == "new":
    st.title("🆕 New Conversation")
    if not st.session_state.get("system_set", False):
        prompt = st.text_area("Set system prompt for this conversation:", height=150)
        if st.button("Start Conversation") and prompt.strip():
            st.session_state.system_prompt = prompt
            st.session_state.messages = [{"role": "system", "content": prompt}]
            try:
                cid = irister_utils.glow_create_convo(st.session_state.username, prompt)
                st.session_state.conversation_id = cid
                st.session_state.system_set = True
                st.rerun()
            except Exception:
                st.error("Failed to create conversation thread.")
        else:
            st.info("Please enter a system prompt to begin.")
    else:
        # Chat interface for new conversation
        st.header(f"System Prompt: *{st.session_state.system_prompt}*")
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        user_input = st.chat_input("Type your message...")
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)
            try:
                reply = irister_utils.glow_chat(st.session_state.conversation_id, user_input)
            except Exception:
                st.error("Error during chat API call.")
                reply = ""
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.chat_message("assistant").write(reply)

elif st.session_state.mode == "history":
    st.title(f"💬 Conversation: {st.session_state.conv_selected}")
    cid = st.session_state.get("conversation_id")
    # Load history once
    if "messages" not in st.session_state:
        try:
            msgs = irister_utils.glow_get_all_messages(cid)
        except Exception:
            st.error("Unable to load messages.")
            msgs = []
        # Store loaded messages
        st.session_state.messages = msgs
    # Display and continue chat
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        try:
            reply = irister_utils.glow_chat(cid, user_input)
        except Exception:
            st.error("Error during chat API call.")
            reply = ""
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.chat_message("assistant").write(reply)
