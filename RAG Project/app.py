from dotenv import load_dotenv
import os

from vectorstore import VectorStore
from chatbot import ChatBot


# Load Environment Variables


load_dotenv()

api_key = os.getenv("COHERE_API_KEY")

if api_key is None:
    raise ValueError("❌ COHERE_API_KEY not found in .env file!")

# Create Vector Store

vectorstore = VectorStore(
    pdf_path="Sample.pdf",
    api_key=api_key
)


# Create ChatBot

chatbot = ChatBot(
    vectorstore=vectorstore,
    api_key=api_key
)

print("\n")
print("=" * 60)
print("🤖 RAG DOCUMENT QUESTION ANSWERING SYSTEM")
print("=" * 60)


# Chat Loop

while True:

    query = input("\nAsk Your Question (type 'exit' to quit): ").strip()

    # Exit Program
    if query.lower() == "exit":
        print("\n👋 Good Bye!")
        break

    # Empty Question Check
    if query == "":
        print("❌ Please enter a valid question.")
        continue

    try:
        answer = chatbot.ask(query)

        print("\n")
        print("=" * 60)
        print("FINAL ANSWER")
        print("=" * 60)
        print(answer)

    except Exception as e:
        print("\n❌ Error:", e)