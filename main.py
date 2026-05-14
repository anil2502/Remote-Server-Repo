from fastmcp import FastMCP
import os
import json
import sqlite3
import aiosqlite
import tempfile
import random
from tavily import TavilyClient



# =========================================================
# DATABASE CONFIGURATION
# =========================================================

# IMPORTANT:
# In FastMCP Cloud / serverless containers,
# /app is read-only.
# So we must use writable temp directory.

# DB_PATH = os.path.join(
#     tempfile.gettempdir(),
#     "expenses.db"
# )

# print(f"Database path: {DB_PATH}")

# # Optional categories file path
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# CATEGORIES_PATH = os.path.join(
#     BASE_DIR,
#     "categories.json"
# )

# # =========================================================
# # MCP SERVER
# # =========================================================
# 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
mcp = FastMCP("ExpenseTracker")

client = TavilyClient(
    api_key = "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"
)

# # =========================================================
# # DATABASE INITIALIZATION
# # =========================================================

# def init_db():

#     try:

#         with sqlite3.connect(DB_PATH) as conn:

#             conn.execute("PRAGMA journal_mode=WAL")

#             conn.execute("""
#                 CREATE TABLE IF NOT EXISTS expenses(
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     date TEXT NOT NULL,
#                     amount REAL NOT NULL,
#                     category TEXT NOT NULL,
#                     subcategory TEXT DEFAULT '',
#                     note TEXT DEFAULT ''
#                 )
#             """)

#             conn.commit()

#         print("Database initialized successfully")

#     except Exception as e:

#         print(f"Database initialization error: {e}")

#         raise

# # Initialize database on startup
# init_db()

# # =========================================================
# # TOOLS
# # =========================================================

# @mcp.tool()
# async def add_expense(
#     date: str,
#     amount: float,
#     category: str,
#     subcategory: str = "",
#     note: str = ""
# ):
#     """
#     Add a new expense entry to the database.
#     """

#     try:

#         async with aiosqlite.connect(DB_PATH) as conn:

#             cursor = await conn.execute(
#                 """
#                 INSERT INTO expenses(
#                     date,
#                     amount,
#                     category,
#                     subcategory,
#                     note
#                 )
#                 VALUES (?, ?, ?, ?, ?)
#                 """,
#                 (
#                     date,
#                     amount,
#                     category,
#                     subcategory,
#                     note
#                 )
#             )

#             await conn.commit()

#             expense_id = cursor.lastrowid

#             return {
#                 "status": "success",
#                 "id": expense_id,
#                 "message": "Expense added successfully"
#             }

#     except Exception as e:

#         return {
#             "status": "error",
#             "message": str(e)
#         }

# @mcp.tool()
# async def list_expenses(
#     start_date: str,
#     end_date: str
# ):
#     """
#     List expenses between dates.
#     """

#     try:

#         async with aiosqlite.connect(DB_PATH) as conn:

#             cursor = await conn.execute(
#                 """
#                 SELECT
#                     id,
#                     date,
#                     amount,
#                     category,
#                     subcategory,
#                     note
#                 FROM expenses
#                 WHERE date BETWEEN ? AND ?
#                 ORDER BY date DESC
#                 """,
#                 (start_date, end_date)
#             )

#             rows = await cursor.fetchall()

#             columns = [col[0] for col in cursor.description]

#             return [
#                 dict(zip(columns, row))
#                 for row in rows
#             ]

#     except Exception as e:

#         return {
#             "status": "error",
#             "message": str(e)
#         }

# @mcp.tool()
# async def summarize(
#     start_date: str,
#     end_date: str,
#     category: str = None
# ):
#     """
#     Summarize expenses by category.
#     """

#     try:

#         async with aiosqlite.connect(DB_PATH) as conn:

#             query = """
#                 SELECT
#                     category,
#                     SUM(amount) as total_amount,
#                     COUNT(*) as total_entries
#                 FROM expenses
#                 WHERE date BETWEEN ? AND ?
#             """

#             params = [start_date, end_date]

#             if category:

#                 query += " AND category = ?"

#                 params.append(category)

#             query += """
#                 GROUP BY category
#                 ORDER BY total_amount DESC
#             """

#             cursor = await conn.execute(query, params)

#             rows = await cursor.fetchall()

#             columns = [col[0] for col in cursor.description]

#             return [
#                 dict(zip(columns, row))
#                 for row in rows
#             ]

#     except Exception as e:

#         return {
#             "status": "error",
#             "message": str(e)
#         }

# # =========================================================
# # RESOURCE
# # =========================================================

# @mcp.resource(
#     "expense:///categories",
#     mime_type="application/json"
# )
# def categories():

#     default_categories = {
#         "categories": [
#             "Food & Dining",
#             "Transportation",
#             "Shopping",
#             "Entertainment",
#             "Bills & Utilities",
#             "Healthcare",
#             "Travel",
#             "Education",
#             "Business",
#             "Other"
#         ]
#     }

#     try:

#         if os.path.exists(CATEGORIES_PATH):

#             with open(
#                 CATEGORIES_PATH,
#                 "r",
#                 encoding="utf-8"
#             ) as f:

#                 return f.read()

#         return json.dumps(
#             default_categories,
#             indent=2
#         )

#     except Exception as e:

#         return json.dumps({
#             "error": str(e)
#         })




#NOTE:- Rolling  dice With N number of times

@mcp.tool
async def roll_dice(n_dice: int = 1) -> list[int]:
    """Roll n_dice 6-sided dice and return the results."""
    return [random.ranint(1, 6) for i in range(n_dice)]

@mcp.toll
async def tavily_search(query: str) -> str:
    """
    Search the web using Tavily.
    """
    result = client.search(
        query = query,
        search_depth = "advanced",
        max_results = 5
    )

    return str(result)


# =========================================================
# START MCP SERVER
# =========================================================

if __name__ == "__main__":

    print("\nStarting FastMCP Server...")
    print("Server URL: http://localhost:8000/mcp\n")

    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8000
    )