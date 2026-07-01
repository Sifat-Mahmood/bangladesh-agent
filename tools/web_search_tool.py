# tools/web_search_tool.py
# This tool searches the internet for general knowledge questions
# that can't be answered from the local databases.

import os
from langchain.tools import tool
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()  # loads TAVILY_API_KEY from your .env file

# ─────────────────────────────────────────────
# WHAT IS TAVILY?
# Tavily is a search API built specifically for AI agents.
# Unlike Google, it returns clean, summarized text results
# that are easy for an LLM to read and use.
# ─────────────────────────────────────────────

@tool
def web_search_tool(query: str) -> str:
    """
    Use this tool to search the internet for general knowledge questions
    that are NOT about specific hospitals, institutions, or restaurants in Bangladesh.
    Use this for questions about:
    - Government policies and healthcare policies
    - Definitions and explanations (e.g. 'What is DGHS?')
    - Current events and news
    - Cultural, historical, or geographical information about Bangladesh
    - Anything that requires up-to-date information from the web
    Input should be a clear search query string.
    Example: 'healthcare policy Bangladesh 2024'
    """
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            return "Error: TAVILY_API_KEY not found in environment variables."

        client = TavilyClient(api_key=api_key)
        response = client.search(query, max_results=3)

        results = response.get("results", [])
        if not results:
            return "No results found from web search."

        # Format the results cleanly for the LLM to read
        formatted = []
        for i, r in enumerate(results, 1):
            title = r.get("title", "No title")
            content = r.get("content", "No content")
            url = r.get("url", "")
            formatted.append(f"Result {i}: {title}\n{content}\nSource: {url}")

        return "\n\n".join(formatted)

    except Exception as e:
        return f"Web search error: {str(e)}"