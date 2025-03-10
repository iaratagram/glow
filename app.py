import streamlit as st
from openai import OpenAI  # 如果没有用到可去掉
from irister_utils import request_irister  # 替换为你真实的 API 调用
from streamlit_mermaid import st_mermaid

def show_first_page():
    st.title("Glow AI v0")

    with st.sidebar:
        st.title("Glow AI")
        st.caption("🚀 Glow AI chat")

    # 在这里让用户输入文本
    user_input = st.text_input("Please describe the specific behavior you want to analyze (e.g., 'binge eating when stressed'). Be as concrete as possible.")
    if st.button("Submit"):
        if user_input.strip():
            # 将输入存到 session_state (实际项目中可用于后端调用)
            # st.session_state["session_id"] = irister_start_session(user_input)

            st.session_state["problem_behavior"] = user_input

            st.session_state["page"] = "chat"
            st.rerun()
        else:
            st.warning("Please enter some text before submitting.")

def show_chatbot_page():
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            min-width: 150px;
            max-width: 800px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("Glow AI v0 - Chatbot")

    with st.sidebar:
        st.title("Glow AI")
        st.caption("🚀 Glow AI chat")
        
        # --- 使用 streamlit-mermaid 显示图表 ---
        st.subheader("Demo: Mermaid Diagram")

        mermaid_code = """
        flowchart TD
            A --> B
        """
        
        
        # 使用 st_mermaid 显示图表
        st_mermaid(
            mermaid_code,
            height=600,
            width=500
        )
        

    # 确保 "messages" 存在
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # 显示对话记录
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # 聊天输入框
    # 如果有选定的节点引用，显示在输入框中
    
    if prompt := st.chat_input(accept_file=False):
        # 用户发送消息
        st.session_state["messages"].append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)


        # 调用自己的聊天逻辑或后端 API
        ai_response = request_irister(st.session_state["messages"])
        st.session_state["messages"].append({"role": "assistant", "content": ai_response})
        st.chat_message("assistant").markdown(ai_response)
        

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "input"

    if st.session_state["page"] == "input":
        show_first_page()
    else:
        show_chatbot_page()

if __name__ == "__main__":
    main()
