import os
import json
import requests
import pandas as pd
import streamlit as st
import cohere
import streamlit.components.v1 as components
from streamlit.components.v1 import html
import time
import datetime
from dotenv import load_dotenv
from utils import *

import numpy as np
from collections import defaultdict

# Load the environment variables from .env file
load_dotenv(".env")

# Get the COHERE_API_KEY from the environment variables
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# versions
CHAT_URL= "https://api.cohere.ai/v1/chat"
COHERE_MODEL = 'command-r-plus'
co = cohere.Client(api_key=COHERE_API_KEY)

def run():
    st.set_page_config(
        page_title= "Home Dashboard",
        page_icon="🐱",
        layout="wide"
    )

    st.write("Welcome CMPWG Merchant!")

    st.sidebar.success("Main Menu")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role":"CHATBOT", "message":"How I can Help you?"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["message"])

    prompt = st.chat_input()
    
    if prompt:
        st.chat_message("USER").write(prompt)
        response = co.chat(chat_history=st.session_state.messages, message=prompt)
        st.session_state.messages.append({"role": "USER", "message":prompt})
        msg = response.text
        st.session_state.messages.append({"role": "CHATBOT", "message":msg})
        st.chat_message("CHATBOT").write(msg)


if __name__ == "__main__":
    run()
