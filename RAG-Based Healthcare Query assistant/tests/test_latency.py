import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from agents.orchestrator import ask

questions = [

    "How many patients are there?",

    "What is discharge policy?"

]

print("=" * 60)
print("LATENCY TEST")
print("=" * 60)

for q in questions:

    start = time.time()

    result = ask(q)

    end = time.time()

    print()

    print(q)

    print(result["agent"])

    print(f"{end-start:.2f} sec")

    print("-"*60)