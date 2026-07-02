import json
from typing import List, Dict, Any
from qa import get_llm

def generate_compliance_summary(text: str, sensitive_items: List[Dict[str, Any]], risk_level: str, risk_score: int) -> str:
    """Generates an executive compliance summary using LLM."""
    llm = get_llm()
    
    # We only send a subset of text if it's too large to save tokens and context limit
    content_sample = text[:15000] if len(text) > 15000 else text
    
    # Format items
    items_summary = {}
    for item in sensitive_items:
        cat = item['Category']
        items_summary[cat] = items_summary.get(cat, 0) + 1
        
    prompt = f"""
    You are an AI Compliance and Security Expert.
    Analyze the provided document sample and the detected sensitive items to generate a professional Compliance Summary Report.
    
    Risk Level: {risk_level} (Score: {risk_score})
    Detected Sensitive Data Summary: {json.dumps(items_summary)}
    
    Document Sample:
    {content_sample}
    
    Generate a markdown report with exactly these sections:
    ## Executive Summary
    ## Compliance Observations
    ## Possible Violations (e.g., GDPR, HIPAA, PCI-DSS if applicable)
    ## Security Risks
    ## Business Risks
    ## Privacy Risks
    ## Suggested Remediation
    ## Overall Recommendation
    """
    
    response = llm.invoke(prompt)
    return response.content
