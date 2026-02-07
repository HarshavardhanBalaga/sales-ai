"""
Simple Whisper transcription
"""
import whisper
import warnings
warnings.filterwarnings("ignore")

# Cache model globally
_model = None

def get_model():
    """Load Whisper model once (cached)"""
    global _model
    if _model is None:
        print("🔊 Loading Whisper model (first time may take a minute)...")
        try:
            _model = whisper.load_model("base")  # Small, fast model
            print("✅ Whisper model loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load Whisper: {e}")
            raise
    return _model

def transcribe_audio(audio_path: str) -> str:
    """
    Transcribe audio file using Whisper
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Transcribed text
    """
    try:
        model = get_model()
        print(f"📝 Transcribing: {audio_path}")
        
        # Transcribe with basic options
        result = model.transcribe(
            audio_path,
            language='en',  # Force English
            fp16=False,     # Use CPU
            verbose=False   # Don't print progress
        )
        
        return result.get("text", "").strip()
        
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return f"Error in transcription: {str(e)}"