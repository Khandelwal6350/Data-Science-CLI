import sys
import time
from pathlib import Path

# =====================================================
# PROJECT ROOT
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# =====================================================
# IMPORTS
# =====================================================

from agents.generative_client import generate_content

from config import (
    SQL_PROMPT_FILE,
    MODEL_NAME,
    MAX_RETRIES,
    RETRY_DELAY
)

from database.db_utils import execute_query

# =====================================================
# LOAD SQL PROMPT
# =====================================================

with open(SQL_PROMPT_FILE, "r", encoding="utf-8") as file:
    SYSTEM_PROMPT = file.read()

# =====================================================
# CLEAN SQL
# =====================================================

def clean_sql(sql: str):

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    if sql.endswith(";"):
        sql = sql[:-1]

    return sql.strip()

# =====================================================
# VALIDATE SQL
# =====================================================

def validate_sql(sql: str):

    sql = sql.strip()

    if not sql.lower().startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    blocked_keywords = [
        "drop",
        "delete",
        "update",
        "insert",
        "alter",
        "truncate",
        "create",
        "replace",
        "attach",
        "detach",
        "pragma"
    ]

    lower_sql = sql.lower()

    for keyword in blocked_keywords:

        if keyword in lower_sql:

            raise ValueError(
                f"Blocked SQL keyword detected: {keyword}"
            )

    return sql

# =====================================================
# GENERATE SQL
# =====================================================

def generate_sql(question):

    prompt = f"""
{SYSTEM_PROMPT}

User Question:

{question}

Rules:

1. Return ONLY SQL.
2. SQLite syntax only.
3. Never explain.
4. Never use markdown.
5. Never return ```sql
6. Only SELECT queries are allowed.

SQL:
"""

    last_error = None

    for attempt in range(MAX_RETRIES):

        try:

            print("=" * 60)
            print(f"Generating SQL (Attempt {attempt + 1})")
            print("=" * 60)

            response = generate_content(
                prompt=prompt,
                model=MODEL_NAME
            )

            sql = clean_sql(response)

            sql = validate_sql(sql)

            print("\nGenerated SQL\n")
            print(sql)

            return sql

        except Exception as e:

            last_error = e

            print(f"\nAttempt {attempt + 1} Failed")
            print(e)

            if attempt < MAX_RETRIES - 1:
                print("\nRetrying...\n")
                time.sleep(RETRY_DELAY)

    raise last_error

# =====================================================
# FORMAT RESULT
# =====================================================

def format_result(rows):

    if not rows:
        return "No records found."

    if len(rows) == 1 and len(rows[0]) == 1:
        return str(rows[0][0])

    formatted_rows = []

    for row in rows:

        formatted_rows.append(
            " | ".join(str(value) for value in row)
        )

    return "\n".join(formatted_rows)

# =====================================================
# ASK DATABASE
# =====================================================

def ask_database(question):

    sql = generate_sql(question)

    rows = execute_query(sql)

    formatted_result = format_result(rows)

    return {

        "question": question,

        "sql": sql,

        "rows": rows,

        "result": formatted_result

    }

# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Healthcare SQL Agent")
    print("=" * 60)

    while True:

        question = input("\nAsk Question : ")

        if question.lower() == "exit":
            break

        try:

            result = ask_database(question)

            print("\nGenerated SQL\n")
            print(result["sql"])

            print("\nResult\n")
            print(result["result"])

        except Exception as e:

            print("\nError\n")
            print(e)