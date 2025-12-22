from llm.groq_client import GroqClient
from storage.vector_store import IPOVectorStore
from storage.financial_db import FinancialDatabase
from agents.router_agent import RouterAgent
from agents.financial_agent import FinancialAgent
from agents.risk_agent import RiskAgent
from agents.business_agent import BusinessAgent
from agents.summary_agent import SummaryAgent
from agents.citation_agent import CitationAgent

class IPOCrew:
    def __init__(self):
        # Initialize Shared Resources
        self.llm = GroqClient()
        self.vector_store = IPOVectorStore()
        self.db = FinancialDatabase()
        
        # Initialize Agents
        self.router = RouterAgent(self.llm)
        self.financial_agent = FinancialAgent(self.llm, self.db, self.vector_store)
        self.risk_agent = RiskAgent(self.llm, self.vector_store)
        self.business_agent = BusinessAgent(self.llm, self.vector_store)
        self.summary_agent = SummaryAgent(self.llm, self.vector_store, self.db)
        self.citation_agent = CitationAgent(self.llm)

    def process_query(self, query: str) -> str:
        """
        Main entry point for the Streamlit app.
        1. Route query
        2. Execute specific agent
        3. Verify citations
        """
        # Step 1: Route
        intent = self.router.route(query)
        print(f"🤖 Detected Intent: {intent}")
        
        raw_response = ""
        
        # Step 2: Dispatch
        if intent == "FINANCIAL":
            raw_response = self.financial_agent.handle(query)
        elif intent == "RISK":
            raw_response = self.risk_agent.handle(query)
        elif intent == "BUSINESS":
            raw_response = self.business_agent.handle(query)
        elif intent == "SUMMARY":
            raw_response = self.summary_agent.handle()
        elif intent == "OUT_OF_SCOPE":
            return "I apologize, but this query seems outside the scope of this IPO document. Please ask about the specific IPO's financials, risks, or business."
        else:
            # Fallback
            raw_response = self.business_agent.handle(query)

        # Step 3: Verify (The Silent Enforcer)
        final_response = self.citation_agent.verify(raw_response)
        
        return final_response
