from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain import hub
from dotenv import load_dotenv
import os

load_dotenv()

# LLM (Groq brain)
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# Web search tool (Tavily)
search = TavilySearchResults()
tools = [search]

# ReAct prompt (standard LangChain agent brain structure)
prompt = hub.pull("hwchase17/react")

# Create agent
agent = create_react_agent(llm, tools, prompt)

# Executor (runs everything)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

# Run query
result = agent_executor.invoke({
    "input": "What are the latest developments in AI agents in 2025? Give me a simple summary."
})

print("\nFINAL ANSWER:\n")
print(result["output"])