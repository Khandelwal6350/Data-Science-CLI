import os

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS


class VectorStore:

    def __init__(self, pdf_path, api_key):

        self.pdf_path = pdf_path
        self.api_key = api_key

        self.embedding_model = CohereEmbeddings(
            model="embed-english-v3.0",
            cohere_api_key=api_key
        )

        self.vector_db = self.create_vector_db()

    def create_vector_db(self):

        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()

        print("✅ PDF Loaded Successfully")

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=50
        )

        chunks = splitter.split_documents(documents)

        print("✅ Total Chunks:", len(chunks))

        if os.path.exists("faiss_index"):

            print("✅ Loading Existing Vector DB")

            db = FAISS.load_local(
                "faiss_index",
                self.embedding_model,
                allow_dangerous_deserialization=True
            )

        else:

            print("✅ Creating New Vector DB")

            db = FAISS.from_documents(
                chunks,
                self.embedding_model
            )

            db.save_local("faiss_index")

        return db

    def retrieve(self, query):

        retriever = self.vector_db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 2}
        )

        return retriever.invoke(query)