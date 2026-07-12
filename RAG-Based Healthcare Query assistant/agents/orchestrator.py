import sys
from pathlib import Path

# =====================================================
# PROJECT ROOT
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# =====================================================
# IMPORT AGENTS
# =====================================================

from agents.sql_agent import ask_database
from agents.rag_agent import ask_policy

# =====================================================
# SQL KEYWORDS
# =====================================================

SQL_KEYWORDS = [

    "patient",
    "patients",
    "doctor",
    "doctors",
    "hospital",
    "medical condition",
    "medication",
    "test result",
    "test results",
    "billing",
    "bill",
    "insurance provider",
    "billing amount",
    "blood",
    "age",
    "gender",
    "room",
    "admission",
    "discharge date",
    "average",
    "avg",
    "count",
    "total",
    "sum",
    "maximum",
    "minimum",
    "highest",
    "lowest",
    "show",
    "list",
    "find",
    "display",
    "which",
    "who",
    "how many",
    "abnormal",
    "normal",
    "diabetes",
    "asthma",
    "cancer",
    "hypertension"

]

# =====================================================
# RAG KEYWORDS
# =====================================================

RAG_KEYWORDS = [

    "policy",
    "policies",
    "guideline",
    "guidelines",
    "procedure",
    "procedures",
    "rule",
    "rules",
    "admission policy",
    "billing policy",
    "discharge policy",
    "insurance policy",
    "emergency policy",
    "privacy policy",
    "refund policy",
    "hospital policy",
    "prior approval",
    "approval"

]

# =====================================================
# QUERY CLASSIFIER
# =====================================================

def classify_question(question: str):

    question = question.lower().strip()

    # Policy queries first

    for keyword in RAG_KEYWORDS:

        if keyword in question:

            return "RAG"

    # Database queries

    for keyword in SQL_KEYWORDS:

        if keyword in question:

            return "SQL"

    # Default

    return "RAG"

# =====================================================
# MAIN ROUTER
# =====================================================

def ask(question):

    agent = classify_question(question)

    print("\n" + "=" * 60)
    print(f"Selected Agent : {agent}")
    print("=" * 60)

    try:

        # =============================================
        # SQL AGENT
        # =============================================

        if agent == "SQL":

            result = ask_database(question)

            return {

                "agent": "SQL",

                "question": result["question"],

                "answer": result["result"],

                "sql": result["sql"]

            }

        # =============================================
        # RAG AGENT
        # =============================================

        result = ask_policy(question)

        return {

            "agent": "RAG",

            "question": result["question"],

            "answer": result["answer"],

            "sources": result["sources"]

        }

    except Exception as e:

        return {

            "agent": agent,

            "question": question,

            "answer": f"Error: {str(e)}"

        }

# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Healthcare Multi-Agent Assistant")
    print("=" * 60)

    while True:

        question = input("\nAsk Question : ")

        if question.lower() == "exit":
            break

        result = ask(question)

        print("\nAgent")
        print("-" * 60)
        print(result["agent"])

        if result["agent"] == "SQL" and "sql" in result:

            print("\nGenerated SQL")
            print("-" * 60)
            print(result["sql"])

        print("\nAnswer")
        print("-" * 60)
        print(result["answer"])

        if result["agent"] == "RAG":

            print("\nSources")
            print("-" * 60)

            for source in result.get("sources", []):

                print("•", source)