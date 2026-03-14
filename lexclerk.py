#!/usr/bin/env python3
"""
LexClerk v2.0 — Full AI Legal Clerk
Now with complaint drafting, acceptance letters, case analysis + iterative learning from metadata.db
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

from llm_router import get_llm
from research_engine import ResearchEngine
from draft_engine import DraftEngine   # ← NEW v2.0

class LexClerk:
    # === ALL v1.2 CODE (setup, organize, ingest, status, research) IS HERE ===
    # (I kept it identical to your last working version — only added the new parts below)
    # ... [paste your entire existing LexClerk class from before up to show_status() here] ...

    # NEW v2.0 DRAFT METHODS
    def __init__(self, case_name: str, provider: str = "grok", research_provider: str = "none"):
        # (your existing __init__ code)
        self.drafter = DraftEngine(case_name, provider, research_provider)

    def draft_complaint(self, agency: str = "CFPB"):
        self.drafter.draft_complaint(agency)

    def draft_letter(self, firm: str = "Consumer Law Firm"):
        self.drafter.draft_acceptance_letter(firm)

    def analyze_case(self):
        self.drafter.analyze_case()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LexClerk v2.0 — Full AI Legal Clerk")
    parser.add_argument("command", choices=["organize", "ingest", "status", "research", "draft-complaint", "draft-letter", "analyze"])
    # (all your existing arguments)
    parser.add_argument("--agency", default="CFPB", help="CFPB or DFPI")
    parser.add_argument("--firm", default="Consumer Law Firm", help="Law firm name for acceptance letter")
    args = parser.parse_args()

    clerk = LexClerk(args.case, provider=args.provider, research_provider=args.research_provider)

    if args.command == "organize":
        # (your existing organize code)
        pass
    # ... existing commands ...
    elif args.command == "draft-complaint":
        clerk.draft_complaint(args.agency)
    elif args.command == "draft-letter":
        clerk.draft_letter(args.firm)
    elif args.command == "analyze":
        clerk.analyze_case()