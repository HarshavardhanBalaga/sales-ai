"""
Simple text cleaning utilities
"""
import re

def clean_text(text: str) -> str:
    """
    Clean transcript text
    """
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?\'"-]', '', text)
    
    # Fix common transcription errors
    text = text.replace("what's up", "whatsapp")
    text = text.replace("whats up", "whatsapp")
    text = text.replace(" i ", " I ")
    text = text.replace(" i'm ", " I'm ")
    
    # Capitalize sentences
    sentences = text.split('. ')
    sentences = [s.strip().capitalize() for s in sentences if s.strip()]
    text = '. '.join(sentences)
    
    return text.strip()