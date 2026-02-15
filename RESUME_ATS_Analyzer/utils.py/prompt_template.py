# utils/prompt_templates.py
def resume_analysis_prompt(resume_text, job_role):
    return f"""
You are an ATS resume analyzer.

Job Role: {job_role}

Resume:
{resume_text}

Tasks:
1. Give ATS score out of 100
2. List missing skills
3. Suggest improvements
4. Mention keywords to add
"""
