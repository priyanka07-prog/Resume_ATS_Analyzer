import streamlit as st
import os
from dotenv import load_dotenv
from utils import extract_text_from_pdf, get_gemini_response

# Load environment variables
load_dotenv()

# Page Configuration
st.set_page_config(page_title="Resume Analyzer & Improver", page_icon="📄", layout="wide")

# Sidebar for API Key
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("Enter Google Gemini API Key", type="password")
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")
    
    st.markdown("---")
    st.markdown("Developed with ❤️ using Streamlit & Gemini AI")

# Main Content
st.title("📄 Smart Resume Analyzer & Improver")
st.markdown("Optimize your resume for ATS and get personalized improvement suggestions.")

# File Uploader
uploaded_file = st.file_uploader("Upload your Resume (PDF)", type=["pdf"])

# Job Description
job_description = st.text_area("Paste the Job Description (Optional)", height=150)

# Initialize Session State
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = None
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = None
if 'improvement_result' not in st.session_state:
    st.session_state.improvement_result = None
if 'last_uploaded_file' not in st.session_state:
    st.session_state.last_uploaded_file = None

# Analysis Options
col1, col2 = st.columns(2)

with col1:
    analyze_btn = st.button("🔍 Analyze Resume")

with col2:
    improve_btn = st.button("✨ Improve Resume")

if uploaded_file is not None:
    # Check if a new file is uploaded
    if st.session_state.last_uploaded_file != uploaded_file:
        with st.spinner("Extracting text from resume..."):
            text = extract_text_from_pdf(uploaded_file)
            st.session_state.resume_text = text
            st.session_state.last_uploaded_file = uploaded_file
            # Reset results for new file
            st.session_state.analysis_result = None
            st.session_state.improvement_result = None
    
    text = st.session_state.resume_text

    if analyze_btn:
        if not api_key:
            st.error("Please provide a Google Gemini API Key.")
        else:
            with st.spinner("Analyzing Resume..."):
                prompt = """
                You are an experienced HR and ATS (Applicant Tracking System) expert. 
                Please analyze the provided resume against the job description (if provided) and general best practices.
                
                Provide a detailed report including:
                1. **ATS Compatibility Score**: (0-100%)
                2. **Key Strengths**: What stands out?
                3. **Weaknesses & Gaps**: What is missing or needs improvement?
                4. **Missing Keywords**: Specific keywords from the job description (if any) that are missing.
                5. **Formatting Issues**: Any layout or formatting problems.
                
                Resume Content:
                """
                # Combine prompt with job description if available
                full_prompt_content = f"Resume Content:\n{text}\n\nJob Description:\n{job_description}"
                response = get_gemini_response(api_key, prompt, full_prompt_content)
                st.session_state.analysis_result = response

    if improve_btn:
        if not api_key:
            st.error("Please provide a Google Gemini API Key.")
        else:
            with st.spinner("Generating Improvements..."):
                prompt = """
                You are a professional resume writer. 
                Based on the provided resume and job description (if provided), rewrite the resume to make it more impactful.
                
                Focus on:
                1. **Action Verbs**: Use strong action verbs.
                2. **Quantifiable Results**: Highlight achievements with numbers where possible.
                3. **Keyword Optimization**: integrate relevant keywords naturally.
                4. **Professional Summary**: Create a compelling summary.
                
                Provide the improved sections in Markdown format.
                
                Resume Content:
                """
                full_prompt_content = f"Resume Content:\n{text}\n\nJob Description:\n{job_description}"
                response = get_gemini_response(api_key, prompt, full_prompt_content)
                st.session_state.improvement_result = response

    # Display Results
    if st.session_state.analysis_result:
        st.subheader("Analysis Results")
        st.markdown(st.session_state.analysis_result)
        st.markdown("---")

    if st.session_state.improvement_result:
        st.subheader("Improved Resume Suggestions")
        st.markdown(st.session_state.improvement_result)

elif analyze_btn or improve_btn:
    st.warning("Please upload a resume first.")

