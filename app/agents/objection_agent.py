"""
Simple objection agent
"""
from app.agents.fast_llm import run_llm

def objection_agent(transcript: str) -> dict:
    """Simple objection analysis"""
    short = transcript[:300]
    
    prompt = f"""Find objections in sales call:

{short}

Answer: Found [0-2] objections. Main issue: [brief]"""

    try:
        response = run_llm(prompt, max_tokens=80)
        
        # Simple parsing
        result = {
            "objections_found": 0,
            "objections": [],
            "recommendations": ["Always ask about budget and timeline"],
            "raw": response
        }
        
        # Check for price/timing objections
        if any(word in short.lower() for word in ["expensive", "cost", "price", "budget"]):
            result["objections_found"] = 1
            result["objections"] = [{
                "type": "Price",
                "customer_quote": "Potential budget concern",
                "better_response": "Focus on ROI and value proposition"
            }]
        
        return result
        
    except Exception as e:
        return {
            "objections_found": 0,
            "objections": [],
            "recommendations": ["Practice objection handling"],
            "error": str(e)
        }