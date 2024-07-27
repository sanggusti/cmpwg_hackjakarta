import os
from typing import List
import json

import numpy as np
import cohere
import langchain
import langchain_core
import langchain_experimental
import pandas as pd
from langchain.agents import Tool
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_experimental.utilities import PythonREPL
from dotenv import load_dotenv

load_dotenv()

# setup the cohere client
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
CHAT_URL= "https://api.cohere.ai/v1/chat"
COHERE_MODEL = 'large'
co = cohere.Client(api_key=COHERE_API_KEY)

DIR = os.path.dirname(os.path.abspath(__file__))
DATA_URI = os.path.join(DIR, '../../data', 'merchant_reviews_sample.csv')

def summarize_reviews(reviews):
    text = ' '.join(reviews)
    max_text_size = 2048
    if len(text) > max_text_size:
        text = text[:max_text_size]
    summary = co.summarize(text=text).summary
    return summary


def get_sentiment(reviews: str):
    text = ' '.join(reviews)
    max_text_size = 2048
    max_text_size = 2048
    if len(text) > max_text_size:
        text = text[:max_text_size]

    with open(os.path.join(DIR, '../../sentiment.json')) as f:
        examples_data = json.load(f)

    examples = [cohere.ClassifyExample(text=example['text'], label=example['label']) for example in examples_data]
    
    response = co.classify(
        model=COHERE_MODEL,
        inputs=[text],
        examples=examples,
        )
    predictions = [classification.prediction for classification in response.classifications]
    sentiment = predictions[0]
    return sentiment


def feedback_analysis(PATH: str) -> pd.DataFrame:
    df_review = pd.read_csv(PATH)
    df_review_grouped = df_review.groupby('Merchant_ID').agg(
        rating=('rating', 'mean'),
        reviews=('reviews', list),
    ).reset_index()

    print(df_review_grouped.head())

    print("Processing reviews...")

    df_review_grouped['summary'] = df_review_grouped['reviews'].apply(summarize_reviews)

    print("Processing sentiment...")

    df_review_grouped['sentiment'] = df_review_grouped['summary'].apply(get_sentiment)

    # df_review_grouped.to_csv(os.path.join(DIR, '../../data', 'review_summary.csv'), index=False)
    
    # print("Review summary saved to review_summary.csv")

    return df_review_grouped


if __name__ == "__main__":
    feedback_analysis(DATA_URI)