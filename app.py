import streamlit as st
from openai import OpenAI
from irister_utils import request_irister

st.title("mindfulness AI v0")

with st.sidebar:
    st.title("mindfulness AI")
    st.caption("🚀 mindfulness AI chat")

starting_msg = 'DEBUG: Current Node - [NODE 1: Best Experience]  \nHello and welcome to your mindfulness feedback session! Let\'s start by reflecting on your recent practice. Could you please share what you enjoyed most about your session?'

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": starting_msg}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    ## replace with irister api
    AI_RESPONSE = request_irister(st.session_state.messages)
    msg = AI_RESPONSE
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").markdown(msg)
