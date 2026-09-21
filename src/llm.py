from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os
load_dotenv()
llm = ChatGoogleGenerativeAI(
    model = os.getenv("MODEL", "gemini-3.5-flash-lite"),
    api_key = os.getenv("GEMINI_API_KEY"),
    project = os.getenv("GEMINI_PROJECT_ID")
)