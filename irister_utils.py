import streamlit as st
import requests

irister_key = st.secrets["IRISTER_API_KEY"]

irister_url = "https://iris-server-e5f0bc08552d.herokuapp.com"

## irister api
## body should be a json
# {
#     "messages": [
#         {"role": "user", "content": "Hello, how are you?"}
#     ]
# }
# api key should be in bearer token

def request_irister(messages):
    url = f"{irister_url}/v1/purer"
    headers = {
        "Authorization": f"Bearer {irister_key}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": messages
    }
    response = requests.post(url, headers=headers, json=data)
    return response.text

def irister_start_session(user_input):
    url = f"{irister_url}/glow/startsession"
    headers = {
        "Authorization": f"Bearer {irister_key}",
        "Content-Type": "application/json"
    }
    data = {"problem_behavior": user_input}
    response = requests.post(url, headers=headers, json=data)
    return response.json()["session_id"]


def irister_chat_session(session_id, messages):
    url = f"{irister_url}/glow/chat"
    headers = {
        "Authorization": f"Bearer {irister_key}",
        "Content-Type": "application/json"
    }
    data = {"session_id": session_id, "messages": messages}
    response = requests.post(url, headers=headers, json=data)
    return response.json()["response"]

