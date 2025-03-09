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
        
        # --- 将 Mermaid 图表设置为可交互，并调整大小以适应侧边栏 ---
        st.subheader("Demo: Mermaid Diagram")

        print("mermaid_chart rendering...")
        
        mermaid_chart = """
        flowchart LR
            A[Start] --> B{Condition?}
            B -->|Yes| C[Option 1]
            B -->|No| D[Option 2]
            C --> E[End]
            D --> E[End]
            
            click A callback
            click B callback
            click C callback
            click D callback
            click E callback
        """
        
        clicked = st_mermaid(
            mermaid_chart,
            height=800,
            width=600, 
            key="interactive_diagram"
        )
        
        # 统一处理点击事件 - 确保在sidebar内部正确缩进
        if clicked:
            # 这里可以根据点击的节点执行相同的操作，只是节点名称不同
            st.session_state["current_quote"] = f"引用自节点 {clicked}"
            ## LOG CURRENT NODE
            print(f"Current Node: {clicked}")
            st.rerun()

        

    # 确保 "messages" 存在
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    # 显示对话记录
    for msg in st.session_state["messages"]:
        st.chat_message(msg["role"]).markdown(msg["content"])

    # 聊天输入框
    # 如果有选定的节点引用，显示在输入框中
    initial_input = st.session_state.get("current_quote", "")
    
    if prompt := st.chat_input(accept_file=False, placeholder=initial_input):
        # 用户发送消息
        st.session_state["messages"].append({"role": "user", "content": prompt})
        st.chat_message("user").markdown(prompt)

        # 调用自己的聊天逻辑或后端 API
        ai_response = request_irister(st.session_state["messages"])
        st.session_state["messages"].append({"role": "assistant", "content": ai_response})
        st.chat_message("assistant").markdown(ai_response)
        
        # 清除当前引用，以便下次输入
        if "current_quote" in st.session_state:
            del st.session_state["current_quote"]

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "input"

    if st.session_state["page"] == "input":
        show_first_page()
    else:
        show_chatbot_page()

if __name__ == "__main__":
    main()
