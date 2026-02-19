import google.generativeai as genai
import PyPDF2

def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file.
    """
    if uploaded_file is not None:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    else:
        return None

def get_gemini_response(api_key, prompt, content):
    """
    Sends a prompt and content to the Gemini model and returns the response.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt + "\n\n" + content)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
