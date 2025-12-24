from llm.groq_client import GroqClient
from storage.vector_store import IPOVectorStore
import json
import re

class ChartAgent:
    def __init__(self, llm_client: GroqClient, vector_store: IPOVectorStore):
        self.llm = llm_client
        self.vector_store = vector_store

    def get_trend_data(self) -> dict:
        """
        Extracts multi-year financial data for visualization.
        Returns a dict: { "Revenue": {"2023": 100, "2024": 120}, ... }
        """
        # 1. Get Context (Targeting Financial Statements)
        # We query for broader terms to get the full table context
        results = self.vector_store.query("Revenue Profit Net Worth for last 3 years", n_results=4, section_filter="FINANCIAL_STATEMENTS")
        context = "\n".join([r['text'] for r in results])

        # 2. Prompt for JSON extraction
        prompt = [
            {"role": "system", "content": """You are a Data Extraction Engine.
            Your job is to extract financial metrics for the LAST 3 AVAIALBLE YEARS/PERIODS from the text.
            
            Output strictly valid JSON in this format:
            {
                "years": ["FY23", "FY24", "FY25"],
                "data": {
                    "Revenue": [100, 150, 200],
                    "Profit": [10, 15, 20],
                    "Net Worth": [500, 600, 700]
                }
            }
            - "years": Labels for the X-axis (e.g., "Mar-23", "Mar-24", "Sep-25"). Earliest to Latest.
            - "data": Arrays of numbers corresponding to those years. Use 0.0 if missing.
            - STRICTLY OUTPUT JSON ONLY. NO MARKDOWN. NO EXPLANATION.
            """},
            {"role": "user", "content": f"Extract financial trends from this text:\n{context}"}
        ]

        # 3. Call LLM
        response = self.llm.chat(prompt, temperature=0.0)
        
        # 4. Parse JSON
        try:
            # Clean md blocks if present
            cleaned = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned)
            return data
        except json.JSONDecodeError:
            print(f"❌ ChartAgent JSON Error: {response}")
            return None

if __name__ == "__main__":
    pass
