# services/gemini_service.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.prompt_templates import resume_analysis_prompt

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="models/gemini-2.0-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def analyze_resume(resume_text, job_role):
    prompt = resume_analysis_prompt(resume_text, job_role)
    response = llm.invoke(prompt)
    return response.content
