from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

FAISS_PATH = BASE_DIR / "vector_db" / "faiss_index"

# =====================================================
# LOAD EMBEDDING MODEL
# =====================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =====================================================
# LOAD FAISS DATABASE
# =====================================================

vector_db = FAISS.load_local(
    str(FAISS_PATH),
    embedding_model,
    allow_dangerous_deserialization=True
)

retriever = vector_db.as_retriever(
    search_kwargs={"k": 3}
)

# =====================================================
# FUNCTION
# =====================================================

def retrieve_documents(query: str):

    documents = retriever.invoke(query)

    return documents


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":

    question = input("Ask your question: ")

    docs = retrieve_documents(question)

    print("\nRetrieved Documents\n")

    for i, doc in enumerate(docs, start=1):

        print("=" * 60)

        print(f"Chunk {i}")

        print(doc.page_content)

        print("=" * 60)