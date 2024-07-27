from typing import List
import cohere
from langchain.agents import Tool
from langchain_cohere.chat_models import ChatCohere
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_experimental.utilities import PythonREPL
from config import COHERE_API_KEY, COHERE_MODEL

# setup the cohere client
co = cohere.Client(api_key=COHERE_API_KEY)

# Python tool setup
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

# Python tool function
def run_python_code(code: str) -> dict:
    try:
        input_code = ToolInput(code=code)
        result = python_tool.func(input_code.code)
        return {'python_answer': result}
    except Exception as e:
        return {'error': str(e)}

# Function map
functions_map = {
    "run_python_code": run_python_code,
}

# Tools
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

# cohere agent with chat
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

