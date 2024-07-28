import os
import json
import requests
import pandas as pd
import streamlit as st
import cohere
import streamlit.components.v1 as components
from dotenv import load_dotenv
from utils import *
import numpy as np
from collections import defaultdict
from src.financial_agent.agent import cohere_agent, tools
from src.financial_agent.preamble import create_preamble
from src.financial_agent.data_loader import load_data

# Load environment variables
load_dotenv(".env")

# Initialize Cohere client
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
co = cohere.Client(api_key=COHERE_API_KEY)

@st.cache_data(show_spinner=False)
def get_data():
    """Load data only once and cache the results."""
    df_grm, df_review = load_data()
    return df_grm, df_review

@st.cache_resource(show_spinner=False)
def get_preamble(df_grm, df_review):
    """Create preamble only once and cache the result."""
    return create_preamble(df_grm, df_review)

# Load data and create preamble
df_grm, df_review = get_data()
preamble = get_preamble(df_grm, df_review)

def display_home_dashboard():
    st.set_page_config(
        page_title="Home Dashboard",
        page_icon="🐱",
        layout="wide"
    )

    # Display HTML content
    with open('index.html', 'r') as file:
        html_content = file.read()
    components.html(html_content, height=150)

    # Main page content
    st.write("Welcome CMPWG Merchant!")
    st.sidebar.success("Main Menu")

    # Create tabs
    tab1, tab2 = st.tabs(['Selling Overview', 'Chat with AI Agent'])

    with tab1:
        st.info("This is your merchant analysis dashboard")
        col1, col2 = st.columns(2)
        with col1:
            st.text("Financial Analysis Report")
            # Placeholder for Generated Report
            
        with col2:
            st.text("Latest Transaction")
            # Placeholder for Dataset Graph
            st.table(df_grm.head())

    with tab2:
        # Initialize chat messages in session state
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "CHATBOT", "message": "How can I help you?"}]

        # Display chat messages
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["message"])

        # Check if the session state contains user data for personalization
        if "user_data" not in st.session_state:
            st.session_state["user_data"] = {"name": None}

        # Greet the user with their name if available
        if st.session_state["user_data"]["name"]:
            st.write(f"Welcome back, {st.session_state['user_data']['name']}!")
        else:
            name_input = st.text_input("What's your name?")
            if name_input:
                st.session_state["user_data"]["name"] = name_input
                st.write(f"Nice to meet you, {name_input}!")

        # Handle user input
        prompt = st.chat_input()
        if prompt:
            st.chat_message("USER").write(prompt)
            st.session_state.messages.append({"role": "USER", "message": prompt})

            # Get response from Cohere agent
            response = cohere_agent(
                message=prompt,
                preamble=preamble,
                tools=tools,
                verbose=True,
            )
            st.session_state.messages.append({"role": "CHATBOT", "message": response})
            st.chat_message("CHATBOT").write(response)

            # Optionally, provide feedback buttons for the user
            lofeedback = st.radio("Was this response helpful?", ("Yes", "No"))

if __name__ == "__main__":
    display_home_dashboard()
