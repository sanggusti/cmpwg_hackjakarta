import os
import cohere
from dotenv import load_dotenv
from langchain_cohere.chat_models import ChatCohere
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL
from langchain.agents import AgentExecutor
from langchain_cohere.react_multi_hop.agent import create_cohere_react_agent
from langchain_core.prompts import ChatPromptTemplate

class TavilySearchInput(BaseModel):
    query: str = Field(description="Query to search the internet with")

class ToolInput(BaseModel):
    code: str = Field(description="Python code to execute.")

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

chat = ChatCohere(model="command-r-plus", temperature=0.3)

internet_search = TavilySearchResults()
internet_search.name = "internet_search"
internet_search.description = "Returns a list of relevant document snippets for a textual query retrieved from the internet."


internet_search.args_schema = TavilySearchInput
python_repl = PythonREPL()
repl_tool = Tool(
    name="python_repl",
    description="Executes python code and returns the result. The code runs in a static sandbox without interactive mode, so print output or save output to a file.",
    func=python_repl.run,
)

repl_tool.name = "python_interpreter"


repl_tool.args_schema = ToolInput

prompt = ChatPromptTemplate.from_template("{input}")


agent = create_cohere_react_agent(
    llm=chat,
    tools=[internet_search, repl_tool],
    prompt=prompt,
)

agent_executor = AgentExecutor(agent=agent, tools=[internet_search, repl_tool], verbose=True)

agent_executor.invoke({
    "input": "Create a plot of the number of full time employees at the 3 tech companies with the highest market cap in the United States in 2024.",
})


