import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from agents.sql_agent import ask_database

questions = [
    "How many patients are there?",
    "Show all abnormal test results.",
    "Show average billing amount by insurance provider.",
    "Show all diabetic patients.",
    "List all female patients."
]

print("=" * 60)
print("SQL AGENT TEST")
print("=" * 60)

for q in questions:

    print("\nQuestion :", q)

    try:

        result = ask_database(q)

        print("\nGenerated SQL\n")

        print(result["sql"])

        print("\nAnswer\n")

        print(result["result"])

    except Exception as e:

        print(e)

    print("-" * 60)