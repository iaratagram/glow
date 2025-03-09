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


