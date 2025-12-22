from crewai import Agent, Task
from llm.groq_client import GroqClient
from utils.prompts import ROUTER_PROMPT

class RouterAgent:
    def __init__(self, llm_client: GroqClient):
        self.llm = llm_client

    def route(self, query: str) -> str:
        """
        Determines the intent of the query.
        """
        messages = [
            {"role": "system", "content": ROUTER_PROMPT},
            {"role": "user", "content": query}
        ]
        
        response = self.llm.chat(messages, temperature=0.0)
        cleaned_response = response.strip().upper().replace('"', '').replace("'", "")
        
        valid_intents = ["FINANCIAL", "RISK", "BUSINESS", "SUMMARY", "OUT_OF_SCOPE"]
        
        # Fallback if LLM creates a sentence
        for intent in valid_intents:
            if intent in cleaned_response:
                return intent
                
        return "OUT_OF_SCOPE" # Default safety

if __name__ == "__main__":
    pass
