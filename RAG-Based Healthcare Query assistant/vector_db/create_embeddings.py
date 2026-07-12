from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# =====================================================
# PROJECT PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DOCS_PATH = BASE_DIR / "docs"
FAISS_PATH = BASE_DIR / "vector_db" / "faiss_index"

# =====================================================
# LOAD ALL POLICY DOCUMENTS
# =====================================================

print("=" * 60)
print("Loading Hospital Policy Documents...")
print("=" * 60)

documents = []

for file in DOCS_PATH.glob("*.txt"):

    print(f"Loading : {file.name}")

    loader = TextLoader(str(file), encoding="utf-8")

    documents.extend(loader.load())

print(f"\nTotal Documents Loaded : {len(documents)}")

# =====================================================
# SPLIT DOCUMENTS INTO CHUNKS
# =====================================================

print("\nCreating Chunks...")

text_splitter = RecursiveCharacterTextSplitter(

    chunk_size=500,

    chunk_overlap=100

)

chunks = text_splitter.split_documents(documents)

print(f"Total Chunks Created : {len(chunks)}")

# =====================================================
# LOAD EMBEDDING MODEL
# =====================================================

print("\nLoading Embedding Model...")

embedding_model = HuggingFaceEmbeddings(

    model_name="sentence-transformers/all-MiniLM-L6-v2"

)

print("Embedding Model Loaded Successfully.")

# =====================================================
# CREATE FAISS VECTOR DATABASE
# =====================================================

print("\nCreating FAISS Index...")

vector_db = FAISS.from_documents(

    documents=chunks,

    embedding=embedding_model

)

# =====================================================
# SAVE VECTOR DATABASE
# =====================================================

vector_db.save_local(str(FAISS_PATH))

print("\nFAISS Vector Database Saved Successfully.")

print(f"Location : {FAISS_PATH}")

print("\nProcess Completed Successfully.")