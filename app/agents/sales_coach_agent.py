"""
Simple coaching agent
"""
from app.agents.fast_llm import run_llm

def sales_coach_agent(transcript: str) -> dict:
    """Simple coaching"""
    short = transcript[:400]
    
    prompt = f"""As sales coach, give feedback on:

{short}

Feedback:
Good: 
Improve: 
Score: /10"""

    try:
        response = run_llm(prompt, max_tokens=100)
        
        result = {
            "strengths": [],
            "improvements": [],
            "score": "7/10",
            "raw": response
        }
        
        lines = response.strip().split('\n')
        for line in lines:
            if line.startswith("Good:"):
                items = line.replace("Good:", "").strip()
                result["strengths"] = [i.strip() for i in items.split(',') if i.strip()]
            elif line.startswith("Improve:"):
                items = line.replace("Improve:", "").strip()
                result["improvements"] = [i.strip() for i in items.split(',') if i.strip()]
            elif "Score:" in line:
                result["score"] = line.split(":")[1].strip()
        
        # Defaults
        if not result["strengths"]:
            result["strengths"] = ["Clear introduction", "Explained products"]
        if not result["improvements"]:
            result["improvements"] = ["Ask more questions", "Better closing"]
        
        return result
        
    except Exception as e:
        return {
            "strengths": ["Professional tone", "Product knowledge"],
            "improvements": ["Could engage customer more", "Ask for needs"],
            "score": "6/10",
            "error": str(e)
        }