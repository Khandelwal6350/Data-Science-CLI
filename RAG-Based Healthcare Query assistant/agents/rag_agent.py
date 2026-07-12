import sys
import time
from pathlib import Path

import streamlit as st

# =====================================================
# PROJECT ROOT
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# =====================================================
# IMPORTS
# =====================================================

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from agents.generative_client import generate_content

from config import (
    VECTOR_DB_PATH,
    MODEL_NAME,
    TOP_K,
    MAX_RETRIES,
    RETRY_DELAY
)

# =====================================================
# LOAD VECTOR DATABASE
# =====================================================

@st.cache_resource
def load_vector_db():

    print("=" * 60)
    print("Loading Embedding Model...")
    print("=" * 60)

    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Loading FAISS Vector Database...")

    vector_db = FAISS.load_local(
        VECTOR_DB_PATH,
        embedding_model,
        allow_dangerous_deserialization=True
    )

    print("FAISS Loaded Successfully.")

    return vector_db


# =====================================================
# RETRIEVER
# =====================================================

vector_db = load_vector_db()

retriever = vector_db.as_retriever(
    search_kwargs={
        "k": TOP_K
    }
)

# =====================================================
# GENERATE ANSWER
# =====================================================

def generate_answer(prompt):

    last_error = None

    for attempt in range(MAX_RETRIES):

        try:

            print("=" * 60)
            print(f"Generating Answer (Attempt {attempt + 1})")
            print("=" * 60)

            answer = generate_content(
                prompt=prompt,
                model=MODEL_NAME
            )

            if answer and answer.strip():

                return answer.strip()

            raise Exception("Empty response received from Groq.")

        except Exception as e:

            last_error = e

            print(e)

            if attempt < MAX_RETRIES - 1:

                print("Retrying...\n")

                time.sleep(RETRY_DELAY)

    raise last_error

# =====================================================
# ASK POLICY
# =====================================================

def ask_policy(question):

    docs = retriever.invoke(question)

    if not docs:

        return {

            "question": question,

            "answer": "I could not find this information in the hospital policy.",

            "context": "",

            "sources": []

        }

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    sources = list(
        {
            Path(doc.metadata.get("source", "Unknown")).name
            for doc in docs
        }
    )

    prompt = f"""
You are a Healthcare Policy Assistant.

Use ONLY the context below.

Do not use outside knowledge.

If the answer is not available in the context,
reply exactly:

I could not find this information in the hospital policy.

Context
========
{context}

Question
========
{question}

Answer:
"""

    answer = generate_answer(prompt)

    return {

        "question": question,

        "answer": answer,

        "context": context,

        "sources": sources

    }

# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    print("=" * 60)
    print("Healthcare RAG Agent")
    print("=" * 60)

    while True:

        question = input("\nAsk Policy Question : ")

        if question.lower() == "exit":
            break

        try:

            result = ask_policy(question)

            print("\nAnswer\n")
            print(result["answer"])

            print("\nSources\n")

            if result["sources"]:

                for source in result["sources"]:

                    print("•", source)

            else:

                print("No source documents found.")

        except Exception as e:

            print("\nError\n")
            print(e)