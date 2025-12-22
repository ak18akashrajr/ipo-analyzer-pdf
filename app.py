import streamlit as st
import os
import shutil
import signal
import sys

# FIX: Windows Compatibility for CrewAI (Mock missing Unix signals)
if sys.platform.startswith('win'):
    # Helper to safe-add attributes
    def safe_signal(name, value):
        if not hasattr(signal, name):
            setattr(signal, name, value)

    safe_signal('SIGHUP', 1)
    safe_signal('SIGCONT', 18)
    safe_signal('SIGTSTP', 20) # Stop typed at terminal
    safe_signal('SIGQUIT', 3)  # Quit from keyboard
    safe_signal('SIGUSR1', 10) # User defined signal 1 (just in case)
    safe_signal('SIGUSR2', 12) # User defined signal 2 (just in case) 

# Import Ingestion Logic
from ingestion.pdf_parser import IPOParser
from ingestion.chunker import IPOChunker
from ingestion.financial_extractor import FinancialExtractor

# Import Storage Logic
from storage.vector_store import IPOVectorStore
from storage.financial_db import FinancialDatabase

# Import Agent Logic
from crew.crew_setup import IPOCrew

# Page Config
st.set_page_config(
    page_title="IPO Analyzer Agent",
    page_icon="📈",
    layout="wide"
)

st.title("📈 AI-Powered IPO Analyzer")
st.markdown("### Retail-Safe Document Intelligence System")

# Initialize Session State
if "crew" not in st.session_state:
    st.session_state.crew = None
if "ingested" not in st.session_state:
    st.session_state.ingested = False
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR: Ingestion ---
with st.sidebar:
    st.header("Upload RHP")
    uploaded_file = st.file_uploader("Upload IPO PDF (Red Herring Prospectus)", type=["pdf"])

    if uploaded_file and not st.session_state.ingested:
        if st.button("Start Analysis"):
            with st.spinner("Step 1/4: Parsing PDF & Detecting Sections..."):
                # Save temp file
                temp_path = "temp_rhp.pdf"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                parser = IPOParser(temp_path)
                parsed_data = parser.parse()
                st.success(f"Parsed {len(parsed_data)} pages.")

            with st.spinner("Step 2/4: Chunking & Metadata..."):
                chunker = IPOChunker()
                chunks = chunker.chunk_document(parsed_data)
                st.success(f"Created {len(chunks)} chunks.")

            with st.spinner("Step 3/4: Extracting Financials..."):
                extractor = FinancialExtractor()
                financials = extractor.extract_metrics(chunks)
                st.info(f"Extracted: {financials}")

            with st.spinner("Step 4/4: Populating Databases..."):
                # Vector DB
                vector_store = IPOVectorStore()
                # Clear old data? For now, we append. Ideally, reset collection for new IPO.
                vector_store.add_chunks(chunks)
                
                # Financial DB
                fin_db = FinancialDatabase()
                fin_db.store_metrics(financials)

            st.session_state.ingested = True
            st.session_state.crew = IPOCrew() # Initialize Crew with new data
            st.success("✅ Ingestion Complete! You can now ask questions.")

    if st.session_state.ingested:
        st.success("System Ready")
        if st.button("Reset / New Upload"):
            st.session_state.ingested = False
            st.session_state.messages = []
            st.experimental_rerun()

# --- MAIN: Chat Interface ---

if not st.session_state.ingested:
    st.info("👈 Please upload an IPO PDF/RHP in the sidebar to begin.")
    st.write("This system uses a Multi-Agent architecture to analyze IPO documents strictly for Retail Investors.")
    st.write("**Agents features:**")
    st.markdown("- **Risk Agent**: Scans only Risk Factors.")
    st.markdown("- **Financial Agent**: Uses structured data for exact numbers.")
    st.markdown("- **Citation Agent**: Enforces page number references.")
else:
    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input User Query
    user_query = st.chat_input("Ask about Risks, Financials, or Business Model...")

    if user_query:
        # Display User Message
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Generate Response
        with st.chat_message("assistant"):
            with st.spinner("Agents are consulting the document..."):
                try:
                    response_text = st.session_state.crew.process_query(user_query)
                    st.markdown(response_text)
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                except Exception as e:
                    st.error(f"Error processing query: {e}")

# Footer
st.markdown("---")
st.caption("⚠️ Disclaimer: This tool provides information based on the document provided. It is not financial advice. No 'Buy/Sell' recommendations are generated.")
