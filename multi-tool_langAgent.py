from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.tools import tool
from langchain import hub
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
import os

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Tool 1 — Web search
search = TavilySearchResults()

# Tool 2 — URL reader
@tool
def read_url(url: str) -> str:
    """Read and extract text content from any URL"""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text()
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)[:3000]

# Tool 3 — Calculator
@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression like '2 + 2' or '15 * 4'"""
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Invalid expression"

tools = [search, read_url, calculate]

prompt = hub.pull("hwchase17/react")

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

result = agent_executor.invoke({
    "input": "Search for the current price of Bitcoin, then calculate how much 0.5 Bitcoin would be worth."
})

print("\nFINAL ANSWER:")
print(result["output"])