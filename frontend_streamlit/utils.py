import cohere
import streamlit as st
import os
import textwrap
import json
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv(".env")

# Get the COHERE_API_KEY from the environment variables
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# versions
CHAT_URL= "https://api.cohere.ai/v1/chat"
COHERE_MODEL = 'command-r-plus'
co = cohere.Client(api_key=COHERE_API_KEY)

def generate_idea(industry, temperature):
    """
    Generate startup idea given an industry name
    Arguments:
        industry(str): the industry name
        temperature(str): the Generate model `temperature` value
    Returns:
        response(str): the startup idea
    """
    prompt = f"""
    Generate a startup idea given the industry. Return the startup idea and without additional commentary.

    ## Examples
    Industry: Workplace
    Startup Idea: A platform that generates slide deck contents automatically based on a given outline

    Industry: Home Decor
    Startup Idea: An app that calculates the best position of your indoor plants for your apartment

    Industry: Healthcare
    Startup Idea: A hearing aid for the elderly that automatically adjusts its levels and with a battery lasting a whole week

    Industry: Education
    Startup Idea: An online primary school that lets students mix and match their own curriculum based on their interests and goals

    ## Your Task
    Industry: {industry}
    Startup Idea:"""

    # Call the Cohere Chat endpoint
    response = co.chat( 
        message=prompt,
        model='command-r', 
        temperature=temperature,
        preamble="")
    
    return response.text

def generate_name(idea, temperature):
    """
    Generate startup name given a startup idea
    Arguments:
        idea(str): the startup idea
        temperature(str): the Generate model `temperature` value
    Returns:
        response(str): the startup name
    """
    prompt= f"""
    Generate a startup name given the startup idea. Return the startup name and without additional commentary.

    ## Examples
    Startup Idea: A platform that generates slide deck contents automatically based on a given outline
    Startup Name: Deckerize

    Startup Idea: An app that calculates the best position of your indoor plants for your apartment
    Startup Name: Planteasy 

    Startup Idea: A hearing aid for the elderly that automatically adjusts its levels and with a battery lasting a whole week
    Startup Name: Hearspan

    Startup Idea: An online primary school that lets students mix and match their own curriculum based on their interests and goals
    Startup Name: Prime Age

    ## Your Task
    Startup Idea: {idea}
    Startup Name:"""
    # Call the Cohere Chat endpoint
    response = co.chat( 
        message=prompt,
        model='command-r',
        temperature=temperature,
        preamble="")

    return response.text


def get_cohere_response(message):
    response = co.chat(
        model=COHERE_MODEL,
        message=message
    )
    return response.text

