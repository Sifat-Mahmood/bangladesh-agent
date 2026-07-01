# tools/restaurants_tool.py
# This tool lets the AI agent query the restaurants SQLite database.

import sqlite3
import os
from langchain.tools import tool

DB_PATH = os.path.join("data", "restaurants.db")

@tool
def restaurants_db_tool(query: str) -> str:
    """
    Use this tool to answer questions about restaurants in Bangladesh.
    This includes restaurants, cafes, food courts, and eateries.
    The database has these columns:
    - name: name of the restaurant
    - address: full address including city/area
    - rating: customer rating (numeric)
    - number_of_reviews: how many reviews the restaurant has
    - affluence: price range or affluence level
    - latitude: GPS latitude
    - longitude: GPS longitude
    Input should be a valid SQL SELECT query on the 'restaurants' table.
    Always use LIMIT in your query to avoid too many results.
    Example: SELECT name, address, rating FROM restaurants ORDER BY rating DESC LIMIT 10
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        columns = [d[0] for d in cursor.description]
        conn.close()

        if not rows:
            return "No results found for your query."

        result_lines = []
        for row in rows:
            line = ", ".join(f"{col}: {val}" for col, val in zip(columns, row))
            result_lines.append(line)

        return f"Found {len(rows)} result(s):\n" + "\n".join(result_lines)

    except Exception as e:
        return f"Database error: {str(e)}"