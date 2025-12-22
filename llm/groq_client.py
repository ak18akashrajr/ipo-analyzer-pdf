import os
from groq import Groq
from dotenv import load_dotenv

# Load env variables
load_dotenv()

class GroqClient:
    def __init__(self, api_key=None, model="llama-3.3-70b-versatile"):
        """
        Wrapper for Groq API.
        Default model: llama-3.3-70b (High performance, low latency).
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model
        
        if not self.api_key:
            print("⚠️ Warning: No GROQ_API_KEY found. LLM calls will fail.")
            self.client = None
        else:
            self.client = Groq(api_key=self.api_key)

    def chat(self, messages, temperature=0.0):
        """
        Sends a chat completion request to Groq.
        messages: List of dicts [{"role": "user", "content": "..."}]
        """
        if not self.client:
            return "Error: Missing API Key"

        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=False
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"❌ Groq API Error: {e}")
            return f"Error communicating with LLM: {str(e)}"

if __name__ == "__main__":
    pass
