import re
from typing import List, Dict, Any
from config import PATTERNS, CONFIDENTIAL_KEYWORDS, RISK_WEIGHTS

def is_luhn_valid(card_num: str) -> bool:
    """Validate credit card number using Luhn algorithm."""
    # Remove non-digits
    digits = [int(d) for d in str(card_num) if d.isdigit()]
    if not digits:
        return False
    
    checksum = 0
    reverse_digits = digits[::-1]
    
    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
        
    return checksum % 10 == 0

def detect_sensitive_data(text: str, page_num: int = 1) -> List[Dict[str, Any]]:
    """Detects sensitive information from text using regex and keywords."""
    results = []
    
    # 1. Regex based matching
    for category, pattern in PATTERNS.items():
        matches = set(re.findall(pattern, text))
        for match in matches:
            # Additional validation for credit cards
            if category == "Credit Card Number":
                if not is_luhn_valid(match):
                    continue
            
            results.append({
                "Category": category,
                "Detected Value": match,
                "Count": text.count(match),
                "Confidence": "High",
                "Page Number": page_num,
                "Risk Weight": RISK_WEIGHTS.get(category, 1)
            })

    # 2. Business Confidentiality Keywords
    for keyword in CONFIDENTIAL_KEYWORDS:
        # Case insensitive exact match or word match
        pattern = r"(?i)\b" + re.escape(keyword) + r"\b"
        matches = set(re.findall(pattern, text))
        if matches:
            results.append({
                "Category": "Business Confidentiality",
                "Detected Value": matches.pop(),  # Use the matched string
                "Count": len(re.findall(pattern, text)),
                "Confidence": "Medium",
                "Page Number": page_num,
                "Risk Weight": RISK_WEIGHTS.get("Business Confidentiality", 3)
            })
            
    # 3. Deduplicate overlapping matches
    # If the exact same string is matched across multiple categories (e.g. Phone vs Bank Account)
    # we should only keep the one with the highest confidence/weight or specific logic.
    # To keep it simple and clean the UI, if a value exists, we only keep the first one detected
    # (since the categories in PATTERNS are roughly ordered from most specific to least).
    
    unique_results = {}
    for res in results:
        val = res["Detected Value"]
        if val not in unique_results:
            unique_results[val] = res
            
    return list(unique_results.values())

def aggregate_results(all_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Aggregate results from multiple pages."""
    # Since same item might be detected across pages, we group them or just list them.
    # We will just list them as a comprehensive report.
    return all_results
