import os
from dotenv import load_dotenv
from crewai import LLM

def get_llm():
    load_dotenv()

    return LLM(
        model="gemini/gemini-2.5-flash",
        api_key=os.getenv("GOOGLE_API_KEY")
    )