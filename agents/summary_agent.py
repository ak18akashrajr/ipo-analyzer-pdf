from llm.groq_client import GroqClient
from utils.prompts import SUMMARY_PROMPT
from storage.vector_store import IPOVectorStore
from storage.financial_db import FinancialDatabase

class SummaryAgent:
    def __init__(self, llm_client: GroqClient, vector_store: IPOVectorStore, db: FinancialDatabase):
        self.llm = llm_client
        self.vector_store = vector_store
        self.db = db

    def handle(self) -> str:
        """
        Generates a comprehensive summary.
        Aggregates data from Financials, Risks, and Business sections.
        """
        # 1. Get Key Financials
        metrics = self.db.get_all_metrics()
        fin_text = "\n".join([f"{k}: {v}" for k, v in metrics.items()])
        
        # 2. Get Top Risks (Broad search for 'risk')
        risk_results = self.vector_store.query("major risks", n_results=3, section_filter="RISK_FACTORS")
        risk_text = "\n".join([r['text'] for r in risk_results])
        
        # 3. Get Business Summary (Broad search for 'business model')
        biz_results = self.vector_store.query("business model company overview", n_results=3, section_filter="BUSINESS_OVERVIEW")
        biz_text = "\n".join([r['text'] for r in biz_results])
        
        full_context = f"""
        FINANCIAL METRICS:
        {fin_text}
        
        BUSINESS OVERVIEW EXCERPTS:
        {biz_text}
        
        RISK FACTOR EXCERPTS:
        {risk_text}
        """
        
        messages = [
            {"role": "system", "content": SUMMARY_PROMPT.format(context=full_context)},
        ]

        answer = self.llm.chat(messages, temperature=0.2)
        return answer

if __name__ == "__main__":
    pass
