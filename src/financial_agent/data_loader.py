import pandas as pd
from src.financial_agent.config import TRX_URI, REVIEW_URI
import src.financial_agent.feedback as feedback
import src.financial_agent.financial_calculator as fc

def load_data():
    df_grm = fc.process_data(TRX_URI)
    df_review = feedback.feedback_analysis(REVIEW_URI)
    return df_grm, df_review.head(10)
