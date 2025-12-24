# 📈 IPO AI Agent (Retail-Safe)

An AI-powered document intelligence system designed to help retail investors analyze IPO (Initial Public Offering) Red Herring Prospectus (RHP) documents. It uses a **Multi-Agent Architecture** to provide factual, simplified, and risk-aware insights.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-Agentic_Framework-orange?style=for-the-badge)
![Groq](https://img.shields.io/badge/LLM-Groq_(Llama3)-purple?style=for-the-badge)

---

## 🚀 Key Features

*   **RAG Implementation**: Analysis is strictly grounded in the uploaded PDF document (Red Herring Prospectus).
*   **Retail-Safe Guardrails**:
    *   🛡️ **No "Buy/Sell" Advice**: Strictly objective analysis.
    *   🔍 **Citation Enforcement**: Every claim is backed by a page number.
    *   ₹ **INR Formatting**: All valuations are converted/displayed in Rupees.
*   **Multi-Agent System**:
    *   **Financial Agent**: Extracts and explains numbers (Revenue, PAT, EPS) from tables.
    *   **Risk Agent**: Scans specialized "Risk Factors" sections for red flags.
    *   **Business Agent**: Explains the business model in simple "Grade 5" language.
    *   **Chart Agent**: Visualizes multi-year financial trends.
*   **Interactive Charts**: Generates Bar and Line charts for Revenue, Profit, and Net Worth trends.
*   **Explainability**: Uses "Explain Like I'm 5" (ELI5) analogies for complex financial terms.

---

## 🛠️ Technology Stack

*   **Frontend**: [Streamlit](https://streamlit.io/)
*   **Orchestration**: [CrewAI](https://www.crewai.com/)
*   **LLM Provider**: [Groq](https://groq.com/) (Model: `llama-3.3-70b-versatile`)
*   **Vector Database**: [ChromaDB](https://www.trychroma.com/) (Local storage)
*   **Structured DB**: [SQLite](https://www.sqlite.org/index.html) (For precise financial metrics)
*   **Parsing**: PyMuPDF & Regex

---

## 📂 Project Structure

```
ipo-ai-agent/
├── app.py                  # Main Streamlit Application
├── requirements.txt        # Python Dependencies
├── .env                    # Environment Variables (API Keys)
├── agents/                 # Specialized CrewAI Agents
│   ├── router_agent.py     # Classifies user intent
│   ├── financial_agent.py  # Handles numerical queries
│   ├── risk_agent.py       # Extracts risks
│   ├── business_agent.py   # Explains business model
│   ├── chart_agent.py      # Extracts trend data for charts
│   └── ...
├── ingestion/              # PDF Processing Pipeline
│   ├── pdf_parser.py       # Extract text & Detect Sections
│   ├── chunker.py          # Smart Chunking (Page-aware)
│   └── financial_extractor.py # Regex for Table Extraction
├── storage/                # Database Handlers
│   ├── vector_store.py     # ChromaDB wrapper
│   └── financial_db.py     # SQLite wrapper
├── llm/                    # LLM Client
│   └── groq_client.py      # Groq API Wrapper
└── utils/
    └── prompts.py          # System Instructions & Guardrails
```

---

## ⚡ How to Run

### Prerequisities
1.  **Groq API Key**: Get a free key from [Groq Console](https://console.groq.com/).
2.  **Python 3.10+** installed.

### Steps
1.  **Clone the Repository**
    ```bash
    git clone https://github.com/ak18akashrajr/ipo-analyzer-pdf.git
    cd ipo_multi_agent_analyzer
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r ipo-ai-agent/requirements.txt
    ```

3.  **Configure Environment**
    Create a `.env` file in the root folder:
    ```env
    GROQ_API_KEY=gsk_your_api_key_here
    ```

4.  **Run the App**
    Navigate to the inner folder and run:
    ```bash
    cd ipo-ai-agent
    streamlit run app.py
    ```

5.  **Use the Tool**
    *   Upload an IPO PDF (RHP).
    *   Wait for the "Ingestion Complete" message.
    *   Ask questions like *"What are the risks?"* or *"Explain the business model simply."*
    *   Click **"View Financial Trends"** to see charts.

---

## ⚠️ Disclaimer
This tool is for educational purposes only. It uses AI to summarize information provided in the prospectus. It does **not** provide investment advice. Always consult a SEBI-registered financial advisor before investing.
