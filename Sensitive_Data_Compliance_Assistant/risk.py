from typing import List, Dict, Any, Tuple

def calculate_risk(results: List[Dict[str, Any]]) -> Tuple[int, str]:
    """Calculate total risk score and classify risk level."""
    total_score = 0
    
    # Avoid counting the same exact value multiple times for risk score, 
    # or count every instance? The prompt says "calculate total score".
    # I'll sum the Risk Weight of all detected distinct items.
    
    unique_items = {}
    for item in results:
        val = item["Detected Value"]
        if val not in unique_items:
            unique_items[val] = item["Risk Weight"]
            
    total_score = sum(unique_items.values())
    
    if total_score <= 5:
        risk_level = "Low Risk"
    elif 6 <= total_score <= 15:
        risk_level = "Medium Risk"
    else:
        risk_level = "High Risk"
        
    return total_score, risk_level
