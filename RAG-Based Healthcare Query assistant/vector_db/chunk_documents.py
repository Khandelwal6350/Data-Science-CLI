from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ------------------------------------------------
# Paths
# ------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DOCS_PATH = BASE_DIR / "docs"

# ------------------------------------------------
# Load Documents
# ------------------------------------------------

documents = []

for file in DOCS_PATH.glob("*.txt"):

    loader = TextLoader(str(file), encoding="utf-8")

    documents.extend(loader.load())

print(f"\nLoaded Documents : {len(documents)}")

# ------------------------------------------------
# Chunk Documents
# ------------------------------------------------

text_splitter = RecursiveCharacterTextSplitter(

    chunk_size=500,

    chunk_overlap=100

)

chunks = text_splitter.split_documents(documents)

print(f"Total Chunks : {len(chunks)}")

print("\nFirst Chunk\n")

print(chunks[0].page_content)