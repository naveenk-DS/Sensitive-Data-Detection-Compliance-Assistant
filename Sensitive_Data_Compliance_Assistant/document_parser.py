import os
import pdfplumber
import pandas as pd
from pdf2image import convert_from_path
from typing import Dict, Any, Tuple
from ocr import extract_text_with_ocr

def is_scanned_pdf(pdf_path: str) -> bool:
    """Determine if a PDF is scanned by checking if it contains selectable text."""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:3]: # Check first few pages
                text = page.extract_text()
                if text and len(text.strip()) > 50:
                    return False # Has selectable text
    except Exception as e:
        print(f"Error checking PDF: {e}")
    return True # Default to scanned if no text or error

def parse_pdf(pdf_path: str) -> Tuple[str, Dict[int, Any]]:
    """Parse PDF and return combined text and page-wise data."""
    scanned = is_scanned_pdf(pdf_path)
    full_text = []
    page_data = {}
    
    if scanned:
        # Convert to images and use OCR
        images = convert_from_path(pdf_path)
        for i, img in enumerate(images):
            text, boxes = extract_text_with_ocr(img)
            full_text.append(text)
            page_data[i+1] = {"text": text, "boxes": boxes, "scanned": True, "image": img}
    else:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text() or ""
                full_text.append(text)
                # Keep words for potential redaction (pdfplumber provides word bounding boxes)
                words = page.extract_words()
                page_data[i+1] = {"text": text, "words": words, "scanned": False}
                
    return "\n".join(full_text), page_data

def parse_csv(csv_path: str) -> str:
    """Parse CSV to string."""
    df = pd.read_csv(csv_path)
    return df.to_string()

def parse_txt(txt_path: str) -> str:
    """Parse TXT file."""
    with open(txt_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_document(file_path: str) -> Tuple[str, Any]:
    """Route document parsing based on extension."""
    ext = os.path.splitext(file_path)[1].lower()
    page_data = None
    
    if ext == '.pdf':
        text, page_data = parse_pdf(file_path)
    elif ext == '.csv':
        text = parse_csv(file_path)
    elif ext == '.txt':
        text = parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")
        
    return text, page_data
