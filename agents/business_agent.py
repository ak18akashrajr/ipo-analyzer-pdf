from llm.groq_client import GroqClient
from utils.prompts import BUSINESS_PROMPT
from storage.vector_store import IPOVectorStore

class BusinessAgent:
    def __init__(self, llm_client: GroqClient, vector_store: IPOVectorStore):
        self.llm = llm_client
        self.vector_store = vector_store

    def handle(self, query: str) -> str:
        """
        Handles business-related queries.
        Searches 'BUSINESS_OVERVIEW' and 'USE_OF_PROCEEDS' (if possible) or generl search.
        """
        # Try specific section first
        vector_results = self.vector_store.query(query, n_results=5, section_filter="BUSINESS_OVERVIEW")
        
        # Fallback to general search if no business section results (sometimes section detection fails)
        if not vector_results:
            vector_results = self.vector_store.query(query, n_results=5) # No filter

        context_text = ""
        for res in vector_results:
            context_text += f"-- Source (Page {res['metadata']['page']} - {res['metadata']['section']}): {res['text']}\n"

        messages = [
            {"role": "system", "content": BUSINESS_PROMPT.format(context=context_text, question=query)},
        ]

        answer = self.llm.chat(messages, temperature=0.1)
        return answer

if __name__ == "__main__":
    pass
