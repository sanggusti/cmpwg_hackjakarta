import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
CHAT_URL = "https://api.cohere.ai/v1/chat"
COHERE_MODEL = 'command-r-plus'

TRX_URI = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data', 'food_dataset_v1.csv')
REVIEW_URI = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data', 'merchant_reviews_sample.csv')
