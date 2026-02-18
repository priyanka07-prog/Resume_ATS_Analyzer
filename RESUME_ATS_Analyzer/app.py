# app.py
import streamlit as st
from utils.resume_reader import read_resume
from services.gemini_service import analyze_resume

st.title("📄 Resume Analyzer (ATS Friendly)")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
job_role = st.text_input("Enter Job Role (e.g. Data Analyst)")

if st.button("Analyze Resume"):
    if uploaded_file and job_role:
        resume_text = read_resume(uploaded_file)
        result = analyze_resume(resume_text, job_role)
        st.write(result)
    else:
        st.warning("Please upload resume and enter job role")
