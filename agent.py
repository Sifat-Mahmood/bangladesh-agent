# agent.py
# This is the core of the project — it assembles the AI agent.
# The agent has an LLM brain, 4 tools, and an executor that runs the reasoning loop.

import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

# Import our 4 tools
from tools.institutions_tool import institutions_db_tool
from tools.hospitals_tool import hospitals_db_tool
from tools.restaurants_tool import restaurants_db_tool
from tools.web_search_tool import web_search_tool

load_dotenv()  # loads GROQ_API_KEY and TAVILY_API_KEY from .env

# ─────────────────────────────────────────────
# STEP 1: Load the LLM (the "brain")
# ChatGroq connects to Groq's cloud API.
# We use llama-3.3-70b-versatile — great at tool calling (deciding which tool to use).
# temperature=0 means deterministic responses — less creative, more factual.
# ─────────────────────────────────────────────
def create_agent():
    try:
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            api_key=os.getenv("GROQ_API_KEY")
        )

        tools = [
            institutions_db_tool,
            hospitals_db_tool,
            restaurants_db_tool,
            web_search_tool
        ]

        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful AI assistant specialized in Bangladesh.
        
You have access to 4 tools:
1. institutions_db_tool — for queries about educational/government institutions in Bangladesh
2. hospitals_db_tool — for queries about hospitals and medical facilities in Bangladesh  
3. restaurants_db_tool — for queries about restaurants and eateries in Bangladesh
4. web_search_tool — for general knowledge, policies, definitions, current events

RULES:
- Always use the most relevant tool for the query
- For data/statistics questions, use the appropriate DB tool
- For general knowledge questions, use web_search_tool
- Write correct SQL queries using the column names described in each tool
- Always use LIMIT in SQL queries (max 20 rows unless user asks for more)
- Present results in a clean, readable format
- If a query spans multiple tools, use them one by one
"""),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])

        agent = create_tool_calling_agent(llm, tools, prompt)

        executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )

        print("✅ Agent created successfully!")
        return executor

    except Exception as e:
        print(f"❌ Failed to create agent: {str(e)}")
        raise e