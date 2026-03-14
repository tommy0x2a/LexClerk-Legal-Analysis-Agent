"""
draft_engine.py — v2.0 Draft Generator for LexClerk
Uses metadata.db + research engine to create complaints, letters, and briefs
"""
import sqlite3
from pathlib import Path
from datetime import datetime
from llm_router import get_llm
from research_engine import ResearchEngine

class DraftEngine:
    def __init__(self, case_name: str, provider: str = "grok", research_provider: str = "perplexica"):
        self.case_root = Path(f"LexClerk_Case_{case_name.replace(' ', '_')}")
        self.db_path = self.case_root / "metadata.db"
        self.drafts_folder = self.case_root / "Archive" / "Drafts"
        self.drafts_folder.mkdir(parents=True, exist_ok=True)

        self.llm = get_llm(provider)
        self.researcher = ResearchEngine(research_provider)
        print(f"✅ DraftEngine ready — LLM: {provider.upper()} | Research: {research_provider.upper()}")

    def _query_db(self, sql: str, params=()):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute(sql, params)
        rows = c.fetchall()
        conn.close()
        return rows

    def _get_case_summary(self):
        docs = self._query_db("SELECT category, filename, confidence FROM documents ORDER BY confidence DESC LIMIT 50")
        summary = "HIGH-CONFIDENCE EVIDENCE:\n"
        for cat, fname, conf in docs:
            summary += f"• {cat} | {fname} ({conf:.0f}% confidence)\n"
        return summary

    def _research_latest(self, topic: str):
        query = f"Latest {topic} updates 2025-2026 CFPB DFPI RESPA UDAAP Elder Financial Abuse case law statutes of limitations"
        return self.researcher.research(query)

    def draft_complaint(self, agency: str = "CFPB"):
        print(f"📝 Generating {agency} Complaint (using database + real-time research)...")
        summary = self._get_case_summary()
        research = self._research_latest("CFPB complaint requirements and sample templates" if agency == "CFPB" else "DFPI complaint requirements")

        prompt = f"""You are an expert consumer law attorney drafting a formal complaint.
Use ONLY the evidence below. Be factual, cite specific documents and dates where possible.
Include:
- Clear statement of facts
- Specific violations (RESPA, UDAAP, CA HBOR, Elder Financial Abuse)
- Requested relief
- Supporting evidence references

EVIDENCE SUMMARY:
{summary}

LATEST REGULATIONS:
{research}

Generate a complete, ready-to-file {agency} complaint in professional legal language."""

        response = self.llm.invoke(prompt)
        content = response.content if hasattr(response, 'content') else str(response)

        filename = f"{agency}_Complaint_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        path = self.drafts_folder / filename
        path.write_text(content, encoding="utf-8")

        print(f"✅ {agency} Complaint saved: {path.resolve()}")
        return content

    def draft_acceptance_letter(self, firm_name: str = "Consumer Law Firm"):
        print(f"📧 Generating Acceptance Letter to {firm_name}...")
        summary = self._get_case_summary()
        research = self._research_latest("consumer law firm intake requirements mortgage disputes 2026")

        prompt = f"""Draft a professional acceptance letter to {firm_name}.
Highlight the strongest evidence from the database.
Mention why this case has strong merit (high confidence scores).
Request a consultation and include key violations.

EVIDENCE SUMMARY:
{summary}

CURRENT LAW FIRM STANDARDS:
{research}"""

        response = self.llm.invoke(prompt)
        content = response.content if hasattr(response, 'content') else str(response)

        filename = f"Acceptance_Letter_{firm_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        path = self.drafts_folder / filename
        path.write_text(content, encoding="utf-8")

        print(f"✅ Acceptance Letter saved: {path.resolve()}")
        return content

    def analyze_case(self):
        print("🔍 Running full Case Analysis + Merit Brief Summary...")
        summary = self._get_case_summary()
        research = self._research_latest("merit brief requirements mortgage fraud cases California 2026")

        prompt = f"""Provide a professional case analysis and merit brief summary.
Rate overall strength (0-100%).
List top 3 strongest claims with evidence citations.
Recommend next steps (CFPB complaint, DFPI filing, law firm outreach).

EVIDENCE:
{summary}

LATEST LEGAL STANDARDS:
{research}"""

        response = self.llm.invoke(prompt)
        content = response.content if hasattr(response, 'content') else str(response)

        filename = f"Case_Analysis_Merit_Brief_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        path = self.drafts_folder / filename
        path.write_text(content, encoding="utf-8")

        print(f"✅ Full Case Analysis saved: {path.resolve()}")
        return content