import pandas as pd
from config import TRX_URI, REVIEW_URI
import feedback
import financial_calculator as fc

def load_data():
    df_grm = fc.process_data(TRX_URI)
    df_review = feedback.feedback_analysis(REVIEW_URI)
    return df_grm, df_review
