import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai import errors as genai_errors

load_dotenv()

def get_client():
    """Initializes and returns the Gemini Client."""
    api_key = None
    
    # Try getting from streamlit secrets first
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        pass
        
    # Fallback to environment variable (incl. .env file loaded via load_dotenv)
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
        
    if not api_key:
        return None
        
    return genai.Client(api_key=api_key)

def _categorize_api_error(e):
    """Categorizes a Gemini API exception into a user-friendly message and error category."""
    err_str = str(e).lower()
    
    if isinstance(e, genai_errors.ClientError):
        if e.code == 401 or e.code == 403 or "api_key" in err_str or "permission" in err_str or "unauthorized" in err_str or "auth" in err_str:
            return "auth", "🔑 Es gab ein Problem mit deinem API-Schlüssel. Bitte überprüfe die GEMINI_API_KEY-Einstellung in deiner .streamlit/secrets.toml-Datei."
        if e.code == 429 or "rate" in err_str or "quota" in err_str or "resource_exhausted" in err_str:
            return "rate_limit", "⏳ Der KI-Dienst ist gerade ausgelastet. Bitte warte etwa 30 Sekunden und versuche es erneut."
        if e.code == 400 or "bad request" in err_str or "invalid" in err_str:
            return "invalid_request", "⚠️ Die Anfrage an die KI war ungültig. Bitte überprüfe deine Eingaben und versuche es erneut."
        return "client_error", f"⚠️ Der KI-Dienst meldet einen Fehler (Code {e.code}). Bitte versuche es später erneut."
    
    if isinstance(e, genai_errors.ServerError):
        return "server", "🔧 Der KI-Dienst hat momentan einen internen Fehler. Bitte versuche es in einigen Minuten erneut."
    
    # Connection / network errors
    if "connection" in err_str or "timeout" in err_str or "dns" in err_str or "reset" in err_str or "refused" in err_str:
        return "network", "🌐 Es gab ein kleines Problem bei der Verbindung mit der KI. Bitte überprüfe deine Internetverbindung oder versuche es in wenigen Augenblicken noch einmal."
    
    return "unknown", f"❌ Ein unerwarteter Fehler ist aufgetreten: {e}"


def parse_existing_cv(file_bytes, mime_type):
    """
    Uses Gemini to extract structured information from an existing CV file.
    """
    client = get_client()
    if not client:
        raise Exception("Gemini API key is not configured.")
        
    prompt = """
    You are an expert recruitment assistant. Extract all professional information from the attached CV.
    Return the information strictly as a JSON object with this structure:
    {
        "personal": { "first_name": "...", "last_name": "...", "email": "...", "phone": "...", "address": "...", "postal_code": "...", "birth_date": "DD.MM.YYYY", "birth_place": "..." },
        "experience": [ { "job_title": "...", "company": "...", "start_date": "...", "end_date": "...", "description": "..." } ],
        "education": [ { "degree": "...", "institution": "...", "start_date": "...", "end_date": "...", "description": "..." } ],
        "skills": [ { "skill_name": "...", "level": "Beginner/Intermediate/Advanced/Expert" } ],
        "languages": [ { "language": "...", "level_desc": "e.g. Native/Fluent/Basic" } ],
        "hobbies": [ "...", "..." ],
        "links": [ { "platform": "...", "url": "..." } ]
    }
    If information is missing, use empty strings or empty lists.
    Do NOT include markdown formatting like ```json in the output.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(data=file_bytes, mime_type=mime_type),
                prompt
            ]
        )
        return response.text
    except Exception as e:
        category, message = _categorize_api_error(e)
        raise Exception(f"{category}||{message}")


def translate_and_format_cv(user_data):
    """
    Sends the raw user data to Gemini and requests a structured JSON response
    with professional German translations.
    """
    client = get_client()
    if not client:
        raise Exception("Gemini API key is not configured.")
        
    prompt = f"""
    You are an expert German HR professional and translator. 
    The user is applying for a job in Germany and provided their CV information in their native language (or mixed).
    Translate all text to formal, professional German (C1 business level) suitable for a German CV (Lebenslauf) and Cover Letter (Anschreiben).
    
    Here is the user's raw input data:
    {user_data}
    
    Return the output strictly as a JSON object with the following structure:
    {{
        "company": {{ "name": "...", "job_title": "...", "address": "...", "contact_person": "..." }},
        "personal": {{ "first_name": "...", "last_name": "...", "email": "...", "phone": "...", "address": "...", "postal_code": "...", "birth_date": "...", "birth_place": "..." }},
        "experience": [ {{ "job_title": "...", "company": "...", "start_date": "...", "end_date": "...", "description": "..." }} ],
        "education": [ {{ "degree": "...", "institution": "...", "start_date": "...", "end_date": "...", "description": "..." }} ],
        "skills": [ {{ "skill_name": "...", "level": "..." }} ],
        "languages": [ {{ "language": "...", "cefr_level": "..." }} ],
        "links": [ {{ "platform": "...", "url": "..." }} ],
        "hobbies": [ "...", "..." ],
        "cover_letter_text": "..."
    }}
    
    If the user provided company information, please also write a full professional German Cover Letter body text (do not include the sender/receiver addresses in the text, just the actual body starting from 'Sehr geehrte...' or 'Sehr geehrter...' to 'Mit freundlichen Grüßen'). Place this in "cover_letter_text" (use \\n for line breaks).
    
    For languages, evaluate the user's description (e.g. "I speak good English") and map it to the CEFR level (A1, A2, B1, B2, C1, C2, Muttersprache).
    Make sure to translate job titles, descriptions, degrees, and hobbies into standard German equivalents where possible.
    Do NOT include markdown formatting like ```json in the output, just the raw JSON.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        category, message = _categorize_api_error(e)
        raise Exception(f"{category}||{message}")
