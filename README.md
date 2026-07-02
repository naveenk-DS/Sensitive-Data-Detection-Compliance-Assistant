<div align="center">

# 🛡️ Sensitive Data Detection & Compliance Assistant

### AI-Powered Document Security, Compliance Analysis & Automatic Redaction

<img src="https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Streamlit-Web_App-red?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Ollama-Local_LLM-success?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Llama3-Local_AI-orange?style=for-the-badge"/>
<img src="https://img.shields.io/badge/OCR-PaddleOCR-yellow?style=for-the-badge"/>
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>

---

**[🌐 View Working Prototype / Deployment](#)**

---

### 🔒 Detect • Analyze • Classify • Redact • Summarize

An AI-powered compliance assistant that automatically detects sensitive information from documents, classifies security risks, generates compliance reports, performs intelligent document Q&A, and redacts confidential information — **completely offline using Local Ollama + Llama 3.**

</div>

---

# 🚀 Features

✅ Upload PDF, TXT, CSV

✅ Automatic OCR for Scanned PDFs

✅ Detect Sensitive Information

- Aadhaar Number
- PAN Number
- Passport Number
- Driving License
- Employee IDs
- Phone Numbers
- Email Addresses
- Credit Cards
- Bank Accounts
- IFSC Codes
- API Keys
- Passwords
- JWT Tokens
- Private Keys
- Business Confidential Data

---

✅ AI Compliance Report

Generate

- Executive Summary
- Security Risks
- Compliance Issues
- Privacy Risks
- Recommendations
- Overall Risk Score

---

✅ AI Question Answering

Ask questions like

> How many emails exist?

> Summarize this document.

> What sensitive data exists?

> What compliance risks were found?

---

✅ Automatic PDF Redaction

Supports

✔ Text PDFs

✔ OCR PDFs

✔ Black Mask

✔ Partial Mask

✔ Highlight Mode

---

## 🧠 Local AI

This project **does NOT require OpenAI API**.

Everything runs locally using

- Ollama
- Llama 3

Benefits

✔ No Internet Required

✔ No API Cost

✔ Better Privacy

✔ Faster Development

---

# 🏗️ Architecture

```text
                 Upload Document
                        │
                        ▼
            PDF / TXT / CSV Parser
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
 Text PDF                     Scanned PDF
         │                             │
         ▼                             ▼
 Text Extraction                PaddleOCR
         │                             │
         └──────────────┬──────────────┘
                        ▼
          Sensitive Data Detection
         (Regex + NLP + AI Validation)
                        │
        ┌───────────────┴──────────────┐
        ▼                              ▼
 Risk Classification         AI Compliance Report
        │                              │
        └───────────────┬──────────────┘
                        ▼
            Local Llama3 (Ollama)
                        │
        ┌───────────────┴──────────────┐
        ▼                              ▼
 Question Answering         Automatic Redaction
                        │
                        ▼
              Download Reports
```

---

# ⚙️ Technology Stack

| Technology | Purpose |
|------------|----------|
| Python | Backend |
| Streamlit | UI |
| Ollama | Local LLM Runtime |
| Llama3 | AI Model |
| PaddleOCR | OCR |
| pdfplumber | PDF Parsing |
| PyMuPDF | PDF Redaction |
| Pandas | CSV Processing |
| Regex | Sensitive Data Detection |
| LangChain | AI Pipeline |
| FAISS | Vector Database |

---

# 📂 Project Structure

```text
Sensitive Data Detection/
│
├── Sensitive_Data_Compliance_Assistant/
│   ├── app.py
│   ├── document_parser.py
│   ├── detector.py
│   ├── ocr.py
│   ├── redactor.py
│   ├── summary.py
│   ├── qa.py
│   ├── risk.py
│   ├── rag.py
│   ├── utils.py
│   ├── config.py
│   ├── uploads/
│   ├── outputs/
│   ├── logs/
│   └── vector_db/
│
├── README.md
├── pyproject.toml
└── uv.lock
```

---

# 🔄 Workflow

```text
Upload Document
        │
        ▼
Extract Text
        │
        ▼
Detect Sensitive Information
        │
        ▼
Risk Classification
        │
        ▼
Generate AI Compliance Report
        │
        ▼
Ask Questions
        │
        ▼
Generate Redacted PDF
        │
        ▼
Download Results
```

---

# 🛡️ Risk Classification

| Score | Level |
|---------|---------|
| 0–5 | 🟢 Low |
| 6–15 | 🟡 Medium |
| 16+ | 🔴 High |

---

# 📊 Dashboard

✔ Risk Score

✔ Compliance Summary

✔ Detection Statistics

✔ Sensitive Data Table

✔ AI Recommendations

✔ Download Reports

---

# 📸 Screenshots

## Dashboard

```text
(Add Screenshot Here)
```

---

## OCR Detection

```text
(Add Screenshot Here)
```

---

## Compliance Report

```text
(Add Screenshot Here)
```

---

## Masked PDF

```text
(Add Screenshot Here)
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/naveenk-DS/Sensitive-Data-Detection.git

cd "Sensitive Data Detection"
```

---

## Install Dependencies

This project uses `uv` for fast dependency management:

```bash
uv sync
```

*(Alternatively, you can use standard pip: `pip install -r requirements.txt`)*

---

# 🦙 Install Ollama

Download from the official site:

https://ollama.com

---

Pull Llama3

```bash
ollama pull llama3
```

Verify

```bash
ollama run llama3
```

---

# ▶️ Run Project

Navigate to the source directory and run Streamlit:

```bash
cd Sensitive_Data_Compliance_Assistant
uv run streamlit run app.py
```

Open your browser to:

```text
http://localhost:8501
```

---

# 🤖 AI/ML Approach Used

This project utilizes a multi-layered hybrid AI/ML pipeline for maximum accuracy and privacy:
1. **Computer Vision & OCR**: Employs `PaddleOCR` and `pdfplumber` to perform optical character recognition on scanned PDFs and images, enabling text extraction regardless of the document's original format.
2. **Deterministic NLP & Regex**: Utilizes highly optimized Regular Expressions and checksum validation algorithms (like the Luhn algorithm for Credit Cards) to ensure zero-false-positive detection of strictly formatted PII and financial data.
3. **Retrieval-Augmented Generation (RAG)**: Integrates `FAISS` vector databases and `LangChain` to dynamically chunk and retrieve document context, overcoming the context-window limitations of standard LLMs.
4. **Local Generative AI**: Uses `Ollama` and the `Llama-3` foundational model to analyze the retrieved context, generate executive compliance reports, and answer natural language queries completely offline, ensuring zero data leakage.

---

# 🧠 AI Model Details

Model

```text
Llama 3
```

Running

```text
Ollama
```

Inference

```text
Offline
```

API Cost

```text
₹0
```

---

# ⚠️ Challenges Faced

- **Scanned PDF Accuracy**: Accurately extracting text from heavily pixelated or skewed scanned PDFs required implementing a robust OCR fallback (`PaddleOCR`) specifically tuned to recognize structured data.
- **Regex False Positives**: Differentiating between generic 10-digit numbers (like Bank Accounts) and Phone Numbers required highly specific negative lookaheads and algorithmic deduplication in the detection engine to prevent overlapping categories.
- **Offline RAG Latency**: Running complex RAG pipelines on a local machine without API keys initially caused high latency. This was solved by chunking document processing efficiently and strictly optimizing the FAISS vector retrieval size.

---

# 📈 Future Improvements

- Multi Document Support
- ChromaDB
- Docker
- Kubernetes
- Multi-language OCR
- Azure Blob Storage
- Authentication
- RBAC
- Audit Dashboard
- Compliance Scorecard
- PDF Watermark Detection
- AI Risk Prediction

---

# 👨💻 Author

**Naveen Kumar**

AI / ML Engineer

[GitHub](https://github.com/naveenk-DS) | LinkedIn | Portfolio

---

# ⭐ If you like this project

Give this repository a ⭐ on GitHub.

---

<div align="center">

### 🛡️ Secure Documents • Protect Privacy • Ensure Compliance

Made with ❤️ using Python, Streamlit, Ollama & Llama 3

</div>
