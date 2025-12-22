from llm.groq_client import GroqClient
from utils.prompts import FINANCIAL_PROMPT
from storage.financial_db import FinancialDatabase
from storage.vector_store import IPOVectorStore

class FinancialAgent:
    def __init__(self, llm_client: GroqClient, db: FinancialDatabase, vector_store: IPOVectorStore):
        self.llm = llm_client
        self.db = db
        self.vector_store = vector_store

    def handle(self, query: str) -> str:
        """
        Orchestrates extracting data and generating an answer.
        """
        # 1. Fetch exact numbers from SQL
        metrics = self.db.get_all_metrics()
        metrics_str = "\n".join([f"{k}: {v}" for k, v in metrics.items()])
        
        # 2. Fetch context from Vector Store (search primarily for financial keywords)
        # We can broaden the search to "FINANCIAL_STATEMENTS" section
        vector_results = self.vector_store.query(query, n_results=3, section_filter="FINANCIAL_STATEMENTS")
        
        context_text = ""
        for res in vector_results:
            context_text += f"-- Text (Page {res['metadata']['page']}): {res['text']}\n"

        # 3. Construct Prompt
        full_context = f"Structured Data found in DB:\n{metrics_str}\n\nUnstructured Text Context:\n{context_text}"
        
        messages = [
            {"role": "system", "content": FINANCIAL_PROMPT.format(context=full_context, question=query)},
        ]

        # 4. Generate Answer
        answer = self.llm.chat(messages, temperature=0.1)
        return answer

if __name__ == "__main__":
    pass
