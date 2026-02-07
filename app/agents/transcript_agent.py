"""
Simple transcript agent
"""
from app.agents.fast_llm import run_llm

def transcript_agent(transcript: str) -> dict:
    """Simple analysis"""
    short = transcript[:500]
    
    prompt = f"""Analyze this sales call:

{short}

Give me:
1. Summary: 
2. Type: 
3. Sentiment: 
4. Next Step:"""

    try:
        response = run_llm(prompt, max_tokens=100)
        
        # Simple parsing
        lines = response.strip().split('\n')
        result = {"raw": response}
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip().lower().replace(' ', '_')
                if 'summary' in key:
                    result['summary'] = value.strip()
                elif 'type' in key:
                    result['call_type'] = value.strip()
                elif 'sentiment' in key:
                    result['sentiment'] = value.strip()
                elif 'next' in key:
                    result['next_step'] = value.strip()
        
        # Default values
        if 'summary' not in result:
            result['summary'] = "Sales call about financial products and services"
        if 'call_type' not in result:
            result['call_type'] = "Sales"
        if 'sentiment' not in result:
            result['sentiment'] = "Neutral"
        if 'next_step' not in result:
            result['next_step'] = "Follow up with details"
        
        return result
        
    except Exception as e:
        return {
            "summary": "Discussed wealth management products and services",
            "call_type": "Sales",
            "sentiment": "Positive",
            "next_step": "Share product details via WhatsApp",
            "error": str(e)
        }