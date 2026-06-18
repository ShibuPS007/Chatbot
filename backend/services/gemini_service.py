import os
import google.generativeai as genai
from fastapi import HTTPException


def get_gemini_model():
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="Gemini API key not configured")

    genai.configure(api_key=api_key)

    return genai.GenerativeModel("models/gemini-flash-latest")
