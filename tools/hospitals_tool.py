# tools/hospitals_tool.py
# This tool lets the AI agent query the hospitals SQLite database.

import sqlite3
import os
from langchain.tools import tool

DB_PATH = os.path.join("data", "hospitals.db")

@tool
def hospitals_db_tool(query: str) -> str:
    """
    Use this tool to answer questions about hospitals and medical facilities in Bangladesh.
    This includes community clinics, diagnostic centers, private hospitals, NGO clinics, and government health centers.

    The database has these columns:
    - name: name of the hospital or facility
    - type: EXACT values are: 'Community Clinic', 'Consultancy & Diagnostic Center', 'Private Hospital / Clinic', 'Union Health Center', 'NGO Hospital/Clinic', 'Upazila Health Complex', 'Medical College', 'Other Hospital', 'Blood Bank', 'Maternal & Child Welfare Centre (MCWC)'
    - division: EXACT values (Title Case): 'Dhaka', 'Chattogram', 'Rajshahi', 'Khulna', 'Rangpur', 'Barishal', 'Mymensingh', 'Sylhet'
    - district: district name (Title Case)
    - upazila: upazila name
    - city_corporation: city corporation if applicable
    - paurasava: municipality name
    - union: union name
    - agency: managing agency
    - private: 1 = private, 0 = government

    IMPORTANT RULES:
    - Division names are Title Case: use 'Dhaka' not 'DHAKA'
    - There is NO bed capacity column in this database — do not mention bed counts
    - For hospital counts use: SELECT COUNT(*) FROM hospitals WHERE ...
    - For listing hospitals use: SELECT name, district, type FROM hospitals WHERE ... LIMIT 10
    - Use LIKE '%keyword%' for partial name matches

    Input should be a valid SQL SELECT query on the 'hospitals' table.
    Example: SELECT name, district, type FROM hospitals WHERE division='Dhaka' AND type LIKE '%Hospital%' LIMIT 10
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