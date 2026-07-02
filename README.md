# AI-Powered Sensitive Data Detection & Compliance Assistant 🛡️

A production-ready, modular AI application built with **Python**, **Streamlit**, and **Ollama** designed to detect, classify, and redact highly sensitive information from documents.

## Features
* **Multi-Format Parsing**: Extracts text from PDFs (both digital and scanned), TXT, and CSV files using `pdfplumber` and `PaddleOCR`.
* **Advanced Detection Engine**: Uses strict Regex and algorithmic validation (like Luhn for Credit Cards) to detect PII, PCI, and PHI data (PAN, Aadhaar, Bank Accounts, etc.) with zero false positives.
* **Intelligent Redaction**: Automatically generates heavily redacted PDFs by rendering black boxes or blurs over sensitive text to ensure compliance.
* **Local Offline AI (Ollama)**: 100% private, offline RAG implementation using FAISS and `Llama3` to generate executive compliance reports and answer security questions about the document without sending data to the cloud.
* **Premium Dashboard**: Real-time interactive UI built with Plotly, featuring neon-themed data distribution donuts, hierarchical treemaps, and live risk-score heartbeat monitors.

## Tech Stack
* **Frontend**: Streamlit, Plotly
* **Backend**: Python 3.12+ (managed with `uv`)
* **AI/NLP**: LangChain, FAISS, Ollama (Llama3)
* **Processing**: PyMuPDF (fitz), PaddleOCR, pdfplumber

## How to Run Locally

1. **Install Dependencies**
   ```bash
   uv sync
   ```

2. **Start Local Ollama**
   Ensure Ollama is installed and running the `llama3` model:
   ```bash
   ollama run llama3
   ```

3. **Launch the Application**
   ```bash
   cd Sensitive_Data_Compliance_Assistant
   uv run streamlit run app.py
   ```
