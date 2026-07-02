import os
import re
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# Directory configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "vector_db")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Ensure directories exist
for directory in [UPLOADS_DIR, OUTPUTS_DIR, VECTOR_DB_DIR, LOGS_DIR]:
    os.makedirs(directory, exist_ok=True)

# Regex Patterns for Sensitive Data Detection
PATTERNS: Dict[str, str] = {
    "Aadhaar Number": r"\b\d{4}\s\d{4}\s\d{4}\b",
    "PAN Number": r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",
    "Passport Number": r"\b[A-Z]{1}[1-9]{1}\d{6}\b",
    "Driving License Number": r"\b[A-Z]{2}[0-9]{2}[ -]?[0-9]{4}[0-9]{7}\b",
    "Email Address": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    "Phone Number": r"\b(?:\+?91[\-\s]?)?[6-9]\d{9}\b",
    "Credit Card Number": r"\b(?:\d{4}[ -]?){3}\d{4}\b",
    "Bank Account Number": r"\b(?![6-9]\d{9}\b)\d{9,18}\b",
    "IFSC Code": r"\b[A-Z]{4}0[A-Z0-9]{6}\b",
    "UPI ID": r"\b[\w.-]+@[a-zA-Z0-9]+(?!\.[a-zA-Z]{2,})\b",  # Simple UPI ID regex excluding emails
    "API Key": r"(?i)\b(?:sk-[a-zA-Z0-9]{48}|AIza[0-9A-Za-z-_]{35}|ghp_[a-zA-Z0-9]{36}|AKIA[0-9A-Z]{16})\b",
    "Password": r"(?i)\b(?:password|pwd|secret|token|access_key|private_key)\s*[:=]\s*[\w!@#$%^&*()-]+\b",
    "Employee ID": r"\b(?:EMP|ID|STAFF)\d{3,6}\b",
}

# Business Confidentiality Keywords
CONFIDENTIAL_KEYWORDS = [
    "Confidential", "Internal", "Salary", "Payroll", "Trade Secret", 
    "Financial Report", "Acquisition", "Merger", "Customer Database", 
    "Employee Database", "Business Strategy", "Not For Distribution", 
    "Private", "Restricted"
]

# Risk Scoring System
RISK_WEIGHTS: Dict[str, int] = {
    "Email Address": 1,
    "Phone Number": 1,
    "Employee ID": 1,
    "Bank Account Number": 3,
    "IFSC Code": 2,
    "Business Confidentiality": 3,
    "PAN Number": 4,
    "Passport Number": 4,
    "Driving License Number": 4,
    "Aadhaar Number": 5,
    "Credit Card Number": 5,
    "Password": 6,
    "API Key": 6,
    "UPI ID": 2
}
