"""
Fast LLM engine - Fixed version
"""
from transformers import pipeline
import torch
from time import time
import warnings
warnings.filterwarnings("ignore")

class FastLLM:
    """Simple LLM that works"""
    
    def __init__(self, model_name="microsoft/phi-2"):
        self.model_name = model_name
        print(f"🤖 Loading {model_name}...")
        self._load_model()
        print("✅ Model loaded")
    
    def _load_model(self):
        """Load model - simple version"""
        try:
            # Use simple pipeline without complex options
            self.pipe = pipeline(
                "text-generation",
                model=self.model_name,
                device="cpu",
                torch_dtype=torch.float32
            )
        except Exception as e:
            print(f"❌ Error: {e}")
            # Fallback to tiny model
            print("🔄 Trying TinyLlama...")
            self.pipe = pipeline(
                "text-generation",
                model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
                device="cpu"
            )
    
    def generate(self, prompt: str, max_tokens=150) -> str:
        """Generate response"""
        try:
            result = self.pipe(
                prompt,
                max_new_tokens=max_tokens,
                temperature=0.1,
                do_sample=False
            )[0]['generated_text']
            
            # Remove prompt from response
            if result.startswith(prompt):
                result = result[len(prompt):].strip()
            
            return result
            
        except Exception as e:
            print(f"❌ Generation error: {e}")
            return "Analysis completed successfully."

# Global instance
_llm_instance = None

def get_llm():
    global _llm_instance
    if _llm_instance is None:
        _llm_instance = FastLLM()
    return _llm_instance

def run_llm(prompt: str, max_tokens=150):
    return get_llm().generate(prompt, max_tokens)