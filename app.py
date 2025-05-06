import streamlit as st
from openai import OpenAI  # 如果没有用到可去掉
from irister_utils import request_irister  # 替换为你真实的 API 调用
from streamlit_mermaid import st_mermaid

def show_chatbot_page():
    st.title("Glow AI v0 - Chatbot")

    ## larger sidebar
    st.markdown("""
    <style>
        [data-testid="stSidebar"] {
            min-width: 200px;
            max-width: 1800px;
        }
    </style>    
    """, unsafe_allow_html=True)

    with st.sidebar:
        st.title("Glow AI")
        st.caption("🚀 Glow AI chat")
        
        # --- 使用 streamlit-mermaid 显示图表 ---
        # st.subheader("Demo: Mermaid Diagram")

        # mermaid_code = """
        # flowchart TD
        #     B[Vulnerability Factors: Sleep Deprivation for 3 Days] --> A[Trigger Event: Received Harsh Feedback at Work]
        #     A --> C[Thoughts: I'm a Failure at Everything]
        #     A --> D[Emotions: Intense Anxiety]
        #     C & D --> E{{Behavior: Binge Eating High-Calorie Foods}}
        #     E --> F[Immediate Consequences: Physical Discomfort]
        #     E --> G[Emotional Consequences: Guilt and Shame]
        #     E --> H[Long-Term Consequences: Weight Gain and Increased Anxiety]

        #     style E fill:#f9f,stroke:#333,stroke-width:2px
        # """
        
        
        # # 使用 st_mermaid 显示图表
        # st_mermaid(
        #     mermaid_code,
        #     height=1600,
        #     width=1600
        # )
        

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
    show_chatbot_page()

if __name__ == "__main__":
    main()
