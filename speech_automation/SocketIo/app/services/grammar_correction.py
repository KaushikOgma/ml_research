import os
from google.generativeai import GenerativeModel, configure as genai_config
from dotenv import load_dotenv

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
genai_config(api_key=google_api_key)

async def correct_grammar(text: str) -> str:
    # model = GenerativeModel("models/gemini-1.0-pro-latest")
    model = GenerativeModel("models/gemini-1.5-flash-001")
    prompt = '''
    You are a highly knowledgeable language teacher with in-depth expertise in multiple languages. Your role is to correct grammar and ensure fluent, accurate language.
    Correct the following text and give the correct version of the text without changing the meaning and with doing minimal chnages in the given text:
    '''
    response = model.generate_content(prompt + text)
    return response.text
