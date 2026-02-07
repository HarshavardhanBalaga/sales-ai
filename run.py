"""
One-click runner for Sales Call Analyzer
"""
import subprocess
import sys
import os

def check_installation():
    """Check if required packages are installed"""
    required = ["streamlit", "torch", "transformers", "whisper"]
    
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            return False
    
    return True

def install_dependencies():
    """Install missing dependencies"""
    print("\n📦 Installing missing packages...")
    os.system("pip install -r requirements.txt")

def main():
    """Main function"""
    print("=" * 50)
    print("🎤 Sales Call Analyzer - Starting...")
    print("=" * 50)
    
    # Check and install dependencies
    if not check_installation():
        install_dependencies()
    
    # Create necessary directories
    os.makedirs("data/uploads", exist_ok=True)
    
    print("\n✅ All dependencies checked")
    print("\n🚀 Starting web interface...")
    print("🌐 Open http://localhost:8501 in your browser")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 50)
    
    # Run Streamlit
    try:
        subprocess.run([
            "streamlit", "run", "app/main.py",
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--browser.gatherUsageStats=false",
            "--theme.base=light"
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()