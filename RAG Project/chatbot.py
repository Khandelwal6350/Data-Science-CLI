from langchain_cohere import ChatCohere


class ChatBot:

    def __init__(self, vectorstore, api_key):

        self.vectorstore = vectorstore

        self.llm = ChatCohere(
            model="command-a-plus-05-2026",
            cohere_api_key=api_key
        )

    def ask(self, query):

        # Retrieve Similar Chunks
        results = self.vectorstore.retrieve(query)

        print("\n")
        print("=" * 60)
        print("RETRIEVED CHUNKS")
        print("=" * 60)

        context = ""

        for i, doc in enumerate(results, start=1):

            print(f"\nChunk {i}")
            print("-" * 40)

            print(doc.page_content)

            context += doc.page_content + "\n"

        # Prompt
        prompt = f"""
You are an AI assistant.

Answer ONLY using the information provided in the context.

If the answer is not available in the context, reply:

"I couldn't find this information in the document."

Context:
{context}

Question:
{query}
"""

        # Generate Answer
        response = self.llm.invoke(prompt)

        # Extract only the text from Cohere response
        answer = ""

        for item in response.content:

            if hasattr(item, "text"):
                answer += item.text

        return answer