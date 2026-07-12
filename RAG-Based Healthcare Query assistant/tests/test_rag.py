import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from agents.rag_agent import ask_policy

questions = [

    "What is admission policy?",

    "What is discharge policy?",

    "What is billing policy?",

    "What is emergency policy?",

    "Is prior insurance approval required?"

]

print("=" * 60)
print("RAG AGENT TEST")
print("=" * 60)

for q in questions:

    print("\nQuestion :", q)

    result = ask_policy(q)

    print("\nAnswer\n")

    print(result["answer"])

    print("\nSources")

    print(result["sources"])

    print("-" * 60)