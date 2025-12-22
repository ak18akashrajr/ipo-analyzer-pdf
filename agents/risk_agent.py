from llm.groq_client import GroqClient
from utils.prompts import RISK_PROMPT
from storage.vector_store import IPOVectorStore

class RiskAgent:
    def __init__(self, llm_client: GroqClient, vector_store: IPOVectorStore):
        self.llm = llm_client
        self.vector_store = vector_store

    def handle(self, query: str) -> str:
        """
        Handles risk-related queries.
        STRICTLY searches only 'RISK_FACTORS' section.
        """
        # Fetch context ONLY from Risk Factors
        vector_results = self.vector_store.query(query, n_results=5, section_filter="RISK_FACTORS")
        
        if not vector_results:
            return "No specific risks found in the 'Risk Factors' section for this query. Please check the document manually."

        context_text = ""
        for res in vector_results:
            context_text += f"-- Risk Source (Page {res['metadata']['page']}): {res['text']}\n"

        messages = [
            {"role": "system", "content": RISK_PROMPT.format(context=context_text, question=query)},
        ]

        answer = self.llm.chat(messages, temperature=0.2) # Slightly higher temp for better fluency, but still low
        return answer

if __name__ == "__main__":
    pass
