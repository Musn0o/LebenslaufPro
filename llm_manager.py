import os
import streamlit as st
import google.generativeai as genai

def setup_gemini():
    """Initializes the Gemini API with the key from secrets or environment."""
    api_key = None
    
    # Try getting from streamlit secrets first
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass
        
    # Fallback to environment variable
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
        
    if not api_key:
        return False
        
    genai.configure(api_key=api_key)
    return True

def get_gemini_model():
    """Returns the generative model."""
    # We use gemini-1.5-flash as it's fast and suitable for text translation/formatting
    return genai.GenerativeModel('gemini-1.5-flash')

def translate_and_format_cv(user_data):
    """
    Sends the raw user data to Gemini and requests a structured JSON response
    with professional German translations.
    """
    if not setup_gemini():
        raise Exception("Gemini API key is not configured.")
        
    model = get_gemini_model()
    
    prompt = f"""
    You are an expert German HR professional and translator. 
    The user is applying for a job in Germany and provided their CV information in their native language (or mixed).
    Translate all text to formal, professional German (C1 business level) suitable for a German CV (Lebenslauf) and Cover Letter (Anschreiben).
    
    Here is the user's raw input data:
    {user_data}
    
    Return the output strictly as a JSON object with the following structure:
    {{
        "personal": {{ "first_name": "...", "last_name": "...", "email": "...", "phone": "...", "address": "...", "postal_code": "...", "birth_date": "...", "birth_place": "..." }},
        "experience": [ {{ "job_title": "...", "company": "...", "start_date": "...", "end_date": "...", "description": "..." }} ],
        "education": [ {{ "degree": "...", "institution": "...", "start_date": "...", "end_date": "...", "description": "..." }} ],
        "skills": [ {{ "skill_name": "...", "level": "..." }} ],
        "languages": [ {{ "language": "...", "cefr_level": "..." }} ]
    }}
    
    For languages, evaluate the user's description (e.g. "I speak good English") and map it to the CEFR level (A1, A2, B1, B2, C1, C2, Muttersprache).
    Make sure to translate job titles, descriptions, and degrees into standard German equivalents where possible.
    Do NOT include markdown formatting like ```json in the output, just the raw JSON.
    """
    
    response = model.generate_content(prompt)
    return response.text
