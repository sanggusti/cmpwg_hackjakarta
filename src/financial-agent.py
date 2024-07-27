import os
from typing import List

import cohere
import langchain
import langchain_core
import langchain_experimental
import pandas as pd
from langchain.agents import Tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_experimental.utilities import PythonREPL
from dotenv import load_dotenv

# load the environment variables from .env file
load_dotenv()

# setup the cohere client
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
CHAT_URL= "https://api.cohere.ai/v1/chat"
COHERE_MODEL = 'command-r-plus'
co = cohere.Client(api_key=COHERE_API_KEY)

