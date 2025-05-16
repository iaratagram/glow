import streamlit as st
import requests

glow_api_key = st.secrets["GLOW_API_KEY"]

irister_url = "https://iris-server-e5f0bc08552d.herokuapp.com"

## irister api
## body should be a json
# {
#     "messages": [
#         {"role": "user", "content": "Hello, how are you?"}
#     ]
# }
# api key should be in bearer token

def glow_create_convo(user_id: str, system_prompt: str):
    url = f"{irister_url}/glow-ai/create_conversation"
    headers = {
        "Authorization": f"Bearer {glow_api_key}",
        "Content-Type": "application/json"
    }
    data = {"user_id": user_id, "system_prompt": system_prompt}
    response = requests.post(url, headers=headers, json=data)
    return response.json()["data"]["conversation_id"]


def glow_chat(conversation_id: str, message: str):
    url = f"{irister_url}/glow-ai/chat"
    headers = {
        "Authorization": f"Bearer {glow_api_key}",
        "Content-Type": "application/json"
    }
    data = {"conversation_id": conversation_id, "message": message}
    response = requests.post(url, headers=headers, json=data)
    return response.json()["message"]


def glow_get_all_conversations(user_id: str):
    url = f"{irister_url}/glow-ai/get_all_conversations?user_id={user_id}"
    headers = {
        "Authorization": f"Bearer {glow_api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()["conversations"]


def glow_get_all_messages(conversation_id: str):
    url = f"{irister_url}/glow-ai/getallmessageswithconversationid?conversation_id={conversation_id}"
    headers = {
        "Authorization": f"Bearer {glow_api_key}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    return response.json()["messages"]

