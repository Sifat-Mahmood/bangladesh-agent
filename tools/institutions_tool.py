# tools/institutions_tool.py
# This tool lets the AI agent query the institutions SQLite database.

import sqlite3
import os
from langchain.tools import tool

# Path to the database file
DB_PATH = os.path.join("data", "institutions.db")

# ─────────────────────────────────────────────
# WHAT IS A LANGCHAIN TOOL?
# A tool is just a Python function decorated with @tool
# The function's docstring is what the LLM reads to decide
# WHETHER to use this tool and WHEN.
# So the docstring must be clear and descriptive!
# ─────────────────────────────────────────────

@tool
def institutions_db_tool(query: str) -> str:
    """
    Use this tool to answer questions about educational and government institutions in Bangladesh.
    This includes schools, colleges, madrashas, technical institutes, and government offices.
    
    The database has these columns:
    - institute_name: name of the institution
    - institute_type: EXACT values are: 'School', 'Madrasha', 'College', 'Technical and Vocational', 'School and College'
    - division: EXACT values are UPPERCASE: 'RAJSHAHI', 'DHAKA', 'CHITTAGONG', 'RANGPUR', 'KHULNA', 'BARISAL', 'MYMENSINGH', 'SYLHET'
    - district: district name
    - thana: thana/upazila name
    - union_name: union name
    - area_status: urban or rural
    - management_type: EXACT values are: 'GOVERNMENT', 'NON-GOVERNMENT', 'GOVERNMENT PRIMARY', 'OTHERS', 'LOCAL GOVERNMENT', 'AUTONOMOUS', 'Run by Christian Missionaries'
    - education_level: values include 'Secondary', 'Higher Secondary', 'Degree (Pass)', 'Degree (Honors)', 'Masters', 'POLYTECHNIC INSTITUTE', 'NURSHING COLLEGE', 'INSTITUTE OF HEALTH TECHNOLOGY', 'BASIC TRADE', 'Dakhil', 'Alim', 'Fazil', 'Kamil'
    - affiliation: affiliated board or university
    - mpo_status: MPO status
    - address: full address

    IMPORTANT RULES for writing SQL:
    - management_type values are UPPERCASE: use 'GOVERNMENT' not 'government'
    - For government institutions use: management_type IN ('GOVERNMENT', 'GOVERNMENT PRIMARY', 'LOCAL GOVERNMENT', 'AUTONOMOUS')
    - For medical/health institutions use: education_level IN ('INSTITUTE OF HEALTH TECHNOLOGY', 'NURSHING COLLEGE')
    - For counting use: SELECT COUNT(*) FROM institutions WHERE ...
    - Always use LIMIT in your query (max 20) unless doing a COUNT query
    - Use LIKE '%keyword%' for partial matches on names

    Input should be a valid SQL SELECT query on the 'institutions' table.
    Example: SELECT institute_name, district FROM institutions WHERE management_type='GOVERNMENT' AND division='Rajshahi' LIMIT 10
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        columns = [d[0] for d in cursor.description]
        conn.close()

        if not rows:
            return "No results found for your query."

        # Format results as readable text
        result_lines = []
        for row in rows:
            line = ", ".join(f"{col}: {val}" for col, val in zip(columns, row))
            result_lines.append(line)

        return f"Found {len(rows)} result(s):\n" + "\n".join(result_lines)

    except Exception as e:
        return f"Database error: {str(e)}"