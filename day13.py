# hub.pull("hwchase17/react-chat") instead of custom prompt
# ConversationBufferMemory for memory(do ctrl+/ for commenting multiple lines)
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
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

search = DuckDuckGoSearchRun()

@tool
def read_url(url: str) -> str:
    """Read and extract text content from any URL"""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text()
    lines = []
    for line in text.splitlines():
        if line.strip() != '':
            lines.append(line)
    return '\n'.join(lines)[:3000]

@tool
def cal(string: str) -> str:
    """Evaluate a mathematical expression like '2 + 2' or '15 * 4'"""
    try:
        result = eval(string)
        return str(result)
    except:
        return "invalid input"

tools = [search, read_url, cal]

prompt = hub.pull("hwchase17/react-chat")

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=False
)

agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5
)

print("Agent ready! Type 'quit' to exit\n")

while True:
    question = input("You: ")
    if question == "quit":
        break
    result = agent_executor.invoke({"input": question})
    print(f"\nAgent: {result['output']}\n")