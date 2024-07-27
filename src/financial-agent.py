import os
from typing import List

import cohere
import pandas as pd
from langchain.agents import Tool
from langchain_cohere.chat_models import ChatCohere
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_experimental.utilities import PythonREPL
from dotenv import load_dotenv

# utility functions
import utils.feedback as feedback
import financial_calculator as fc

# load the environment variables from .env file
load_dotenv()

# setup the cohere client
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
CHAT_URL= "https://api.cohere.ai/v1/chat"
COHERE_MODEL = 'command-r-plus'
co = cohere.Client(api_key=COHERE_API_KEY)


# get URI
TRX_URI = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data', 'food_dataset_v1.csv')
REVIEW_URI = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data', 'merchant_reviews_sample.csv')


# load data
def load_data():    
    df_grm = fc.process_data(TRX_URI)
    df_review = feedback.feedback_analysis(REVIEW_URI)
    return df_grm, df_review


# create preamble
def create_preamble(df_grm: pd.DataFrame, df_review: pd.DataFrame) -> str:
    preamble = f"""
    You are an expert who answers the user's question. You are working with two pandas dataframe in Python. Also, you are financial analyst that can analyze both 
    numerical and categorical data. The name of the dataframe is `{TRX_URI}`. When you are asked a question, you will analyze it in details and provide
    the answer. If the question is not clear, you can ask for clarification. If the user asks a question that is not in the list, you can ask the user to rephrase.
    for weekly report for merchant and `{REVIEW_URI}` for weekly summarization of review and weekly sentiment for each merchant.
    When user ask about which item has highest/lowest/common, you provide the item name along with the value. 
    Here is a preview of the dataframe of GRM:
    {df_grm.drop('product', axis=1).head().to_markdown()} 
    Here is a preview of the dataframe of Review: 
    {df_review.drop('reviews', axis=1).head().to_markdown()}
    """

    return preamble

# python tool setup
python_repl = PythonREPL()
python_tool = Tool(
    name="python_repl",
    description="Executes python code and returns the result. The code runs in a static sandbox without interactive mode, so print output or save output to a file.",
    func=python_repl.run,
)
python_tool.name = "python_interpreter"

class ToolInput(BaseModel):
    code: str = Field(description="Python code to execute.")

python_tool.args_schema = ToolInput

# python tool function
def run_python_code(code: str) -> dict:
    try:
        input_code = ToolInput(code=code)
        result = python_tool.func(input_code.code)
        return {'python_answer': result}
    except Exception as e:
        return {'error': str(e)}
    
# function map
functions_map = {
    "run_python_code": run_python_code,
}

# tools
tools = [
    {
        "name": "run_python_code",
        "description": "given a python code, runs it",
        "parameter_definitions": {
            "code": {
                "description": "executable python code",
                "type": "str",
                "required": True
            }
        }
    },
]


# cohere agent
def cohere_agent(message: str, preamble: str, tools: List[dict], verbose: bool = False) -> str:
    counter = 0
    response = co.chat(
        model=COHERE_MODEL,
        message=message,
        preamble=preamble,
        tools=tools,
    )

    if verbose:
        print(f"\nrunning 0th step.")
        print(response.text)

    while response.tool_calls and counter < 5:
        tool_results = []

        if verbose:
            print(f"\nrunning {counter + 1}th step.")

        for tool_call in response.tool_calls:
            try:
                output = functions_map[tool_call.name](**tool_call.parameters)
                outputs = [output]
                tool_results.append({"call": tool_call, "outputs": outputs})

                if verbose:
                    print(
                        f"= running tool {tool_call.name}, with parameters: {tool_call.parameters}"
                    )
                    print(f"== tool results: {outputs}")
            except Exception as e:
                if verbose:
                    print(f"Error running tool {tool_call.name}: {e}")
                tool_results.append({"call": tool_call, "outputs": [{"error": str(e)}]})

        response = co.chat(
            model=COHERE_MODEL,
            message="",
            chat_history=response.chat_history,
            preamble=preamble,
            tools=tools,
            tool_results=tool_results,
        )

        if verbose:
            print(response.text)

        counter += 1

    return response.text

# main function
def main():
    df_grm, df_review = load_data()
    preamble = create_preamble(df_grm, df_review)

    print(preamble)

    while True:
        user_question = input("Please enter your question (or type 'exit' to quit): ")
        if user_question.lower() == 'exit':
            break
        try:
            response = cohere_agent(
                message=user_question,
                preamble=preamble,
                tools=tools,
                verbose=True,
            )
            print(f"Answer: {response}")
        except Exception as e:
            print(f"Error handling question: {e}")

if __name__ == "__main__":
    main()