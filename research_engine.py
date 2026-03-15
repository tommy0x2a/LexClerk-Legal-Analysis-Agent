#!/usr/bin/env python3
"""
research_engine.py — v2.0
Supports Vane, Perplexica, Grok tools, and None
"""
import requests
from llm_router import get_llm

class ResearchEngine:
    def __init__(self, provider: str = "none"):
        self.provider = provider
        self.llm = get_llm(provider) if provider in ["grok", "gemini", "local"] else None

    def research(self, query: str) -> str:
        if self.provider == "none":
            return "Research disabled."

        if self.provider in ["vane", "perplexica"]:
            try:
                url = "http://localhost:3000/api/search"
                payload = {
                    "query": query,
                    "chatModel": {"providerId": "ollama", "modelId": "llama3.2:latest"},
                    "embeddingModel": {"providerId": "ollama", "modelId": "nomic-embed-text"}
                }
                resp = requests.post(url, json=payload, timeout=60)
                resp.raise_for_status()
                data = resp.json()
                return data.get("answer", data.get("response", str(data)))
            except Exception as e:
                return f"Local research failed ({self.provider}): {e}"

        # Grok/Gemini/Local fallback
        prompt = f"Research this legal question with citations: {query}"
        response = self.llm.invoke(prompt)
        return response.content if hasattr(response, 'content') else str(response)