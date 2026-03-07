import os
from dotenv import load_dotenv
from langchain_xai import ChatXAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama

# Load .env from the current script's directory
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

def get_llm(provider: str = "grok"):
    """Switch effortlessly between the three best options"""
    if provider == "grok":
        return ChatXAI(
            model="grok-4-1-fast-reasoning",   # ← fastest + best tool-calling for agents
            temperature=0.1,
            api_key=os.getenv("XAI_API_KEY"),
            max_tokens=8192
        )
    elif provider == "gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-3.1-pro-preview",    # ← 2M context king for docs/PDFs
            temperature=0.1,
            google_api_key=os.getenv("GEMINI_API_KEY"),
            max_tokens=8192
        )
    else:  # local (zero cost, private)
        return ChatOllama(
            model="llama3.2",   
            temperature=0.1,
            num_ctx=8192
        )

# Example usage in ANY CrewAI or LangGraph project:
# llm = get_llm("grok")      # or "gemini" or "local"
