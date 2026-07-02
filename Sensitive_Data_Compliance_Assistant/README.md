# AI-Powered Sensitive Data Detection & Compliance Assistant

## Project Description
The AI-Powered Sensitive Data Detection & Compliance Assistant is a production-quality Streamlit application designed to help organizations secure their sensitive information. It automatically scans uploaded documents (PDFs, TXTs, CSVs), detects Personally Identifiable Information (PII), confidential business data, and security credentials, calculates an overall compliance risk score, and generates executive summaries. Additionally, it offers document QA via LLMs and allows users to automatically redact sensitive information from PDFs.

## Features
- **Multi-Format Support**: Upload PDF, TXT, and CSV files.
- **Advanced OCR Integration**: Automatically detects and processes scanned PDFs using PaddleOCR.
- **Sensitive Data Detection**: Highlights Aadhaar, PAN, Passports, emails, phone numbers, credit cards, bank accounts, passwords, API keys, and more using Regex and Keyword matching.
- **Luhn Validation**: Employs mathematical validation for extracted credit card numbers.
- **Compliance Risk Scoring**: Quantifies risk based on the severity of the detected sensitive information.
- **Automatic Redaction**: Generates an obscured ("Masked") PDF (supports Full Black Box, Partial Mask, Blur, Highlight).
- **RAG-based Document Q&A**: Employs LangChain + FAISS to allow users to ask specific questions about uploaded documents.
- **Executive Summaries**: Generates AI compliance reports detailing risks and remediations.
- **Interactive Dashboard**: Visualizes data distributions across the entire session using Plotly.
- **Audit Logging**: Keeps a SQLite trail of all performed scans and detections.
- **Export Options**: Export reports as PDF, CSV, and JSON.

## Architecture Diagram
```
User -> Streamlit UI -> Parser (pdfplumber/pdf2image) -> OCR (PaddleOCR)
  |                              |
  |                              -> Detector (Regex/Luhn/Keywords) -> Risk Scorer
  v                              |
Langchain/FAISS (RAG QA) <- AI Features (Gemini/OpenAI) -> Compliance Summary
  |
  v
Redactor (PyMuPDF / Pillow) -> Download Masked Document
```

## Installation & Requirements

Ensure you have Python 3.11+ installed.

```bash
# Optional: Setup a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

Note: OCR requires Poppler. If you are on Windows, download Poppler, extract it, and add the `bin` directory to your `PATH` environment variable. Also, ensure you have Microsoft Visual C++ Redistributable installed for PaddleOCR.

## How to Run

1. Add your API keys to the `.env` file (or enter them directly in the Streamlit Sidebar).
2. Run the Streamlit application:
```bash
streamlit run app.py
```
3. Open the provided local URL in your web browser.

## Folder Structure
```
Sensitive_Data_Compliance_Assistant/
│
├── app.py              # Streamlit Application Interface
├── parser.py           # Document extraction logic (pdfplumber, scanned logic)
├── detector.py         # Regex, keyword detection, Luhn validation
├── risk.py             # Risk classification and scoring logic
├── summary.py          # AI Executive Summary generation
├── qa.py               # Document Q&A setup
├── redactor.py         # PyMuPDF and PIL based redaction
├── ocr.py              # PaddleOCR implementations
├── rag.py              # FAISS and Langchain integrations
├── config.py           # App configuration, weights, keywords, regex patterns
├── utils.py            # SQLite Audit Logging and helpers
│
├── uploads/            # Temporary upload directory
├── outputs/            # Redacted outputs
├── vector_db/          # Persistent local FAISS embeddings
├── logs/               # Audit Log SQLite DB
│
├── requirements.txt    # Python Dependencies
├── README.md           # Documentation
└── .env                # Environment Variables
```

## Future Improvements
- Add support for DOCX and XLSX files.
- Implement robust User Authentication (OAuth).
- Integrate advanced Named Entity Recognition (NER) models for complex, contextual detection.
- Add support for real-time compliance alerting via Slack/Email.

## License
MIT License

## Author
AI Assistant
