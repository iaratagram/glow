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
        
        # --- 使用 Markdown 显示 Mermaid 图表 ---
        st.subheader("Demo: Mermaid Diagram")
        
        # Mermaid 图表的 HTML 包装
        mermaid_html = """
        <div class="mermaid">
        flowchart TD
            A("fab:fa-youtube Starter Guide")
            B("fab:fa-youtube Make Flowchart")
            C("fa:fa-book-open Learn More")
        
            A --> B --> C --> n1 & D & n2
            D -- Build and Design --> E --> F
            D -- Use AI --> G --> H
            D -- Mermaid js --> I --> J
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
        <script>
            mermaid.initialize({startOnLoad:true});
            document.addEventListener('DOMContentLoaded', function() {
                mermaid.init(undefined, document.querySelectorAll('.mermaid'));
            });
        </script>
        """
        
        # 使用 markdown 显示 HTML
        st.markdown(mermaid_html, unsafe_allow_html=True)
        
        # 使用按钮代替点击事件
        st.write("请选择一个节点:")
        if st.button("Starter Guide (A)"):
            st.session_state["current_quote"] = "引用自节点 A: Starter Guide"
            st.rerun()
        if st.button("Make Flowchart (B)"):
            st.session_state["current_quote"] = "引用自节点 B: Make Flowchart"
            st.rerun()
        if st.button("Learn More (C)"):
            st.session_state["current_quote"] = "引用自节点 C: Learn More"
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

        st.write("prompt: ", prompt)

        # 调用自己的聊天逻辑或后端 API
        # ai_response = request_irister(st.session_state["messages"])
        # st.session_state["messages"].append({"role": "assistant", "content": ai_response})
        # st.chat_message("assistant").markdown(ai_response)
        
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
