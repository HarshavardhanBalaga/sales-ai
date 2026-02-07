"""
Simple Sales Call Analyzer - Ready to Run
"""
import streamlit as st
import uuid
import os
import sys
from pathlib import Path
import time

# Add to path
sys.path.append(str(Path(__file__).parent.parent))

# Simple imports
try:
    from app.agents.simple_orchestrator import run_agents
    from app.stt.simple_whisper import transcribe_audio
    from app.utils.text_cleaner import clean_text
except ImportError as e:
    st.error(f"Import error: {e}. Please check all agent files exist.")
    st.stop()

# Page config
st.set_page_config(
    page_title="Sales Call Coach",
    page_icon="🎤",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #28a745;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #ffc107;
    }
    .info-box {
        background-color: #d1ecf1;
        padding: 10px;
        border-radius: 5px;
        border-left: 4px solid #17a2b8;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🎤 Sales Call Analyzer</h1>', unsafe_allow_html=True)
st.markdown("Upload a sales call audio and get instant AI feedback")

# File upload section
st.markdown("### 📁 Upload Audio File")
uploaded_file = st.file_uploader(
    "Choose an MP3 or WAV file",
    type=["mp3", "wav", "m4a"],
    label_visibility="collapsed"
)

if uploaded_file:
    # Save file
    file_id = str(uuid.uuid4())[:8]
    audio_path = f"temp_audio_{file_id}.{uploaded_file.name.split('.')[-1]}"
    
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.read())
    
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📝 Transcription", "🧠 Analysis", "📊 Insights"])
    
    with tab1:
        # Transcribe
        with st.spinner("Transcribing audio... This may take a moment."):
            try:
                transcript = transcribe_audio(audio_path)
                transcript = clean_text(transcript)
                st.success("✅ Transcription complete!")
            except Exception as e:
                st.error(f"❌ Transcription failed: {str(e)}")
                transcript = "Transcription error. Please try a different audio file."
        
        st.markdown("### Transcript")
        st.write(transcript)
        
        # Show transcript stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Characters", len(transcript))
        with col2:
            st.metric("Words", len(transcript.split()))
        with col3:
            st.metric("Estimated Duration", f"{len(transcript.split())/2:.0f}s")
    
    # Analysis tab
    with tab2:
        if transcript and len(transcript) > 20:
            # Analyze with AI
            with st.spinner("🤖 Analyzing call with AI... This may take 10-30 seconds."):
                start_time = time.time()
                try:
                    results = run_agents(transcript)
                    processing_time = time.time() - start_time
                except Exception as e:
                    st.error(f"Analysis failed: {str(e)}")
                    results = {
                        "error": str(e),
                        "transcript_analysis": {"summary": "Analysis failed"},
                        "coaching_feedback": {"score": "N/A"},
                        "objection_analysis": {"objections_found": 0}
                    }
                    processing_time = 0
            
            if "error" not in results:
                st.success(f"✅ Analysis complete in {processing_time:.1f} seconds!")
                
                # Display results in columns
                st.markdown("## 📋 Analysis Results")
                
                # Call Understanding
                st.markdown("### 🧠 Call Understanding")
                trans = results.get("transcript_analysis", {})
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Summary**")
                    st.info(trans.get("summary", "No summary available"))
                    
                    st.markdown("**Call Type**")
                    st.success(trans.get("call_type", trans.get("type", "Unknown")))
                
                with col2:
                    st.markdown("**Sentiment**")
                    sentiment = trans.get("sentiment", "Neutral")
                    if sentiment.lower() == "positive":
                        st.success(f"😊 {sentiment}")
                    elif sentiment.lower() == "negative":
                        st.error(f"😟 {sentiment}")
                    else:
                        st.info(f"😐 {sentiment}")
                    
                    st.markdown("**Next Step**")
                    st.warning(trans.get("next_step", trans.get("next", "None")))
                
                # Sales Coaching
                st.markdown("### 📈 Sales Coaching")
                coaching = results.get("coaching_feedback", {})
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**✅ Strengths**")
                    strengths = coaching.get("strengths", [])
                    if strengths:
                        for strength in strengths[:3]:  # Show max 3
                            st.markdown(f"<div class='success-box'>✓ {strength}</div>", unsafe_allow_html=True)
                    else:
                        st.info("No strengths identified")
                
                with col2:
                    st.markdown("**🔧 Areas to Improve**")
                    improvements = coaching.get("improvements", [])
                    if improvements:
                        for improve in improvements[:3]:  # Show max 3
                            st.markdown(f"<div class='warning-box'>⚠️ {improve}</div>", unsafe_allow_html=True)
                    else:
                        st.info("No improvement areas identified")
                
                st.markdown("**🎯 Recommended Actions**")
                actions = coaching.get("actions", [])
                if actions:
                    for action in actions[:3]:  # Show max 3
                        st.markdown(f"<div class='info-box'>→ {action}</div>", unsafe_allow_html=True)
                else:
                    st.info("No specific actions recommended")
                
                # Coaching score
                score = coaching.get("score", "N/A")
                st.metric("📊 Coaching Score", score)
    
    # Insights tab
    with tab3:
        if transcript and len(transcript) > 20 and "error" not in results:
            # Objection Analysis
            st.markdown("### ⚠️ Objection Analysis")
            objections = results.get("objection_analysis", {})
            
            col1, col2 = st.columns(2)
            with col1:
                objections_found = objections.get("objections_found", 0)
                st.metric("Objections Found", objections_found)
            
            with col2:
                if "quick_stats" in objections:
                    st.metric("Handling Score", f"{objections['quick_stats'].get('avg_handling_score', 0)}/10")
            
            if objections.get("objections"):
                st.markdown("**🔍 Key Objections:**")
                for i, obj in enumerate(objections.get("objections", [])[:3], 1):  # Show max 3
                    with st.expander(f"Objection {i}: {obj.get('type', 'Unknown')}"):
                        st.markdown(f"**Customer said:** {obj.get('customer_quote', 'N/A')}")
                        st.markdown(f"**Handling:** {obj.get('handling', 'N/A')}")
                        st.markdown(f"**Better response:** {obj.get('better_response', 'N/A')}")
            else:
                st.info("No objections detected in this call")
            
            # Recommendations
            if objections.get("recommendations"):
                st.markdown("### 💡 Recommendations")
                for rec in objections.get("recommendations", [])[:3]:  # Show max 3
                    st.success(f"• {rec}")
            
            # Download button
            st.markdown("---")
            st.markdown("### 📥 Export Analysis")
            
            # Create simple report
            report = f"""Sales Call Analysis Report
================================

Call Summary: {trans.get('summary', 'N/A')}
Call Type: {trans.get('call_type', trans.get('type', 'N/A'))}
Sentiment: {trans.get('sentiment', 'N/A')}
Coaching Score: {coaching.get('score', 'N/A')}
Objections Found: {objections.get('objections_found', 0)}

STRENGTHS:
{chr(10).join(['- ' + s for s in coaching.get('strengths', [])])}

IMPROVEMENTS:
{chr(10).join(['- ' + i for i in coaching.get('improvements', [])])}

ACTIONS:
{chr(10).join(['- ' + a for a in coaching.get('actions', [])])}

Analysis completed in: {processing_time:.1f} seconds
"""
            
            st.download_button(
                label="📄 Download Report (TXT)",
                data=report,
                file_name=f"sales_analysis_{file_id}.txt",
                mime="text/plain"
            )
    
    # Cleanup
    try:
        if os.path.exists(audio_path):
            os.remove(audio_path)
    except:
        pass

else:
    # Show instructions when no file uploaded
    st.info("👆 Please upload a sales call audio file to begin analysis")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 What it does:")
        st.write("""
        • Transcribes audio to text
        • Analyzes call structure
        • Provides coaching feedback
        • Identifies objections
        • Suggests improvements
        """)
    
    with col2:
        st.markdown("### 📁 Supported formats:")
        st.write("""
        • MP3 files
        • WAV files
        • M4A files
        • Up to 200MB
        • Clear audio recommended
        """)
    
    with col3:
        st.markdown("### ⚡ Quick start:")
        st.write("""
        1. Upload audio file
        2. Wait for transcription
        3. View AI analysis
        4. Get actionable insights
        5. Download report
        """)

# Footer
st.markdown("---")
st.caption("🎤 Sales Call Analyzer v1.0 • Powered by AI • Free and Open Source")