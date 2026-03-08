#!/usr/bin/env python3
"""
LexClerk v1.1+ — Legal Analysis Agent with Switchable Research
Fully integrated with llm_router + Perplexica / Grok research
"""
import os
from pathlib import Path
import sqlite3
import hashlib
import shutil
import argparse
import json
import re
from datetime import datetime
from rapidfuzz import fuzz
import pymupdf
from docx import Document

# NEW: LLM router + Research engine
from llm_router import get_llm
from research_engine import ResearchEngine

class LexClerk:
    def __init__(self, case_name: str, provider: str = "grok", research_provider: str = "none"):
        self.case_root = Path(f"LexClerk_Case_{case_name.replace(' ', '_')}")
        self.db_path = self.case_root / "metadata.db"
        self.ingest_watch = self.case_root / "ingest"
        self.archive = self.case_root / "Archive" / "Drafts"
       
        self.provider = provider
        self.llm = get_llm(provider)
        print(f"✅ LLM initialized: {provider.upper()}")

        # NEW: Switchable research backend
        self.research_provider = research_provider
        self.researcher = ResearchEngine(research_provider)
        print(f"🔬 Research backend: {research_provider.upper() if research_provider != 'none' else 'DISABLED'}")

        self.setup_structure()
        self.setup_database()

    # === ALL ORIGINAL METHODS (unchanged) ===
    def setup_structure(self):
        # (exact same as your v1.1 — omitted for brevity in this preview)
        # ... paste your original setup_structure, setup_database, extract_text,
        # get_file_hash, classify_document, fuzzy_duplicate_check, generate_readme,
        # organize, ingest, show_status here ...
        pass  # ← REPLACE THIS WITH YOUR FULL ORIGINAL CODE FROM THE PREVIOUS VERSION

    # NEW RESEARCH METHOD
    def research(self, query: str):
        """Real-time legal research using the chosen backend"""
        print(f"🔍 Researching: {query}")
        full_query = f"{query}. Focus on mortgage/loan disputes, RESPA, UDAAP, CA HBOR, Elder Financial Abuse, CFPB, DFPI, recent case law, statutes of limitations, and regulatory updates (2025-2026). Always include citations and dates."
        result = self.researcher.research(full_query)
        print("\n" + result)

    # (your original organize, ingest, show_status etc. go here — unchanged)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LexClerk v1.1+ with switchable research")
    parser.add_argument("command", choices=["organize", "ingest", "status", "research"])
    parser.add_argument("--source", type=str)
    parser.add_argument("--file", type=str)
    parser.add_argument("--case", default="TommyLoanDispute")
    parser.add_argument("--provider", choices=["grok", "gemini", "local"], default="grok")
    parser.add_argument("--research-provider", choices=["none", "perplexica", "grok"], default="none",
                        help="Research backend: perplexica (best citations) or grok (best reasoning)")
    parser.add_argument("--query", type=str, help="Research query when using 'research' command")
    args = parser.parse_args()

    clerk = LexClerk(args.case, provider=args.provider, research_provider=args.research_provider)

    if args.command == "organize":
        source = Path(args.source) if args.source else Path(".")
        clerk.organize(source)
    elif args.command == "ingest":
        if args.file:
            clerk.ingest(Path(args.file))
    elif args.command == "status":
        clerk.show_status()
    elif args.command == "research":
        if args.query:
            clerk.research(args.query)
        else:
            print("❌ Use --query \"your legal question\" with the research command")