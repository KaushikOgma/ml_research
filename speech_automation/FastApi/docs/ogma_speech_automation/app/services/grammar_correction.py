# @Author : Rahul Sinha
# @Date : 22 October 2024

import os
from google.generativeai import GenerativeModel, configure as genai_config
from dotenv import load_dotenv

load_dotenv()

google_api_key = os.getenv("GOOGLE_API_KEY")
genai_config(api_key=google_api_key)

async def correct_grammar(text: str) -> str:
    model = GenerativeModel("models/gemini-1.0-pro-latest")
    
    # Prompt for grammar correction
    prompt = '''
    You are a highly knowledgeable language teacher with in-depth expertise in multiple languages. Your role is to correct grammar and ensure fluent, accurate language.
    Correct the following sentence:
    '''
    
    # Append text to the prompt and get response from the model
    response = model.generate_content(prompt + text)
    
    return response.text
