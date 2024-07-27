import os
from typing import List
from pprint import pprint

import cohere
import langchain
import langchain_core
import langchain_experimental
import pandas as pd
from langchain.agents import Tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_experimental.utilities import PythonREPL
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Get the COHERE_API_KEY from the environment variables
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# versions
CHAT_URL= "https://api.cohere.ai/v1/chat"
COHERE_MODEL = 'command-r-plus'
co = cohere.Client(api_key=COHERE_API_KEY)


# if __name__ == "__main__":
