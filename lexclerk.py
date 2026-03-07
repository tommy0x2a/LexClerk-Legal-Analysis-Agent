#!/usr/bin/env python3
"""
LexClerk v1.1 — Legal Analysis Agent (Digital Clerk Phase)
Fully integrated with your llm_router.py (Grok / Gemini / Local)
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

# NEW: Your LLM router
from llm_router import get_llm

class LexClerk:
    def __init__(self, case_name: str, provider: str = "grok"):
        self.case_root = Path(f"LexClerk_Case_{case_name.replace(' ', '_')}")
        self.db_path = self.case_root / "metadata.db"
        self.ingest_watch = self.case_root / "ingest"
        self.archive = self.case_root / "Archive" / "Drafts"
        
        # Initialize LLM via your router
        self.provider = provider
        self.llm = get_llm(provider)
        print(f"✅ LLM initialized: {provider.upper()}")

        self.setup_structure()
        self.setup_database()

    def setup_structure(self):
        dirs = [
            "00_Master_Overview",
            "01_Evidence_By_Legal_Theory/RESPA_Violations",
            "01_Evidence_By_Legal_Theory/UDAAP_Abusive_Practices",
            "01_Evidence_By_Legal_Theory/CA_HBOR",
            "01_Evidence_By_Legal_Theory/Elder_Financial_Abuse",
            "02_Agency_Interactions/CFPB",
            "02_Agency_Interactions/DFPI",
            "03_Internal_Analysis",
            "04_Outreach_Recruitment",
            "Archive/Drafts"
        ]
        for d in dirs:
            (self.case_root / d).mkdir(parents=True, exist_ok=True)
        self.ingest_watch.mkdir(exist_ok=True)
        self.archive.mkdir(parents=True, exist_ok=True)
        print(f"📁 Structure created at: {self.case_root.resolve()}")

    def setup_database(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY, filename TEXT, path TEXT, hash TEXT,
            category TEXT, confidence REAL, extracted_text TEXT, added_date TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS entities (
            id INTEGER PRIMARY KEY, doc_id TEXT, type TEXT, value TEXT, date TEXT
        )''')
        c.execute('''CREATE TABLE IF NOT EXISTS timeline (
            id INTEGER PRIMARY KEY, date TEXT, event TEXT, doc_id TEXT
        )''')
        conn.commit()
        conn.close()

    def extract_text(self, file_path: Path) -> str:
        text = ""
        try:
            if file_path.suffix.lower() == ".pdf":
                doc = pymupdf.open(file_path)
                text = "\n".join([page.get_text() for page in doc])
            elif file_path.suffix.lower() == ".docx":
                doc = Document(file_path)
                text = "\n".join([p.text for p in doc.paragraphs])
            else:
                text = file_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            text = f"[Extraction failed: {e}]"
        return text[:45000]

    def get_file_hash(self, file_path: Path) -> str:
        return hashlib.md5(file_path.read_bytes()).hexdigest()

    def classify_document(self, text: str) -> tuple[str, float]:
        """Uses your llm_router (Grok/Gemini/Local) + smart JSON parsing + keyword fallback"""
        prompt = f"""You are an expert legal document classifier for mortgage/loan disputes.

Classify into **exactly one** category:
- RESPA_Violations
- UDAAP_Abusive_Practices
- CA_HBOR
- Elder_Financial_Abuse
- Other

Return ONLY valid JSON: {{"category": "CATEGORY_NAME", "confidence": 87}}

Document excerpt:
{text[:1800]}"""

        try:
            response = self.llm.invoke(prompt)
            content = response.content if hasattr(response, 'content') else str(response)

            # Extract JSON safely
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                category = data.get("category", "Other").strip()
                confidence = float(data.get("confidence", 70))
                
                valid = ["RESPA_Violations", "UDAAP_Abusive_Practices", "CA_HBOR", "Elder_Financial_Abuse", "Other"]
                if category not in valid:
                    category = "Other"
                return category, min(98.0, confidence)
        except Exception as e:
            print(f"LLM ({self.provider}) failed — using keyword fallback...")

        # Keyword fallback (unchanged reliability)
        keywords = {
            "RESPA_Violations": ["qualified written request", "qwr", "escrow", "force placed", "respa"],
            "UDAAP_Abusive_Practices": ["unfair", "deceptive", "abusive", "udaap"],
            "CA_HBOR": ["homeowner bill of rights", "hbor", "single point of contact"],
            "Elder_Financial_Abuse": ["elder", "senior", "65", "financial abuse"]
        }
        best_cat = "Other"
        best_score = 0
        lower = text.lower()
        for cat, words in keywords.items():
            score = sum(1 for w in words if w in lower)
            if score > best_score:
                best_score, best_cat = score, cat
        return best_cat, min(92.0, 65 + best_score * 12)

    def fuzzy_duplicate_check(self, new_text: str) -> tuple[bool, Path | None]:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT path, extracted_text FROM documents")
        for row in c.fetchall():
            old_path = Path(row[0])
            if old_path.exists():
                similarity = fuzz.ratio(new_text[:2500], (row[1] or "")[:2500])
                if similarity > 91:
                    return True, old_path
        return False, None

    def generate_readme(self, folder: Path, category: str):
        readme = folder / "README.md"
        content = f"""# {category.replace('_', ' ')} Folder

**Purpose**: All documents related to {category.replace('_', ' ')}.

## Most Damning Evidence
(See highest-confidence files in metadata.db)

## Filing Protocols & Deadlines (2026)
- **CFPB**: Company must respond in 15 days
- **DFPI**: Priority processing for elder abuse cases

**Statutes of Limitations**:
- RESPA §6: 3 years
- CA Elder Financial Abuse: Up to 4 years

**Key Contacts**:
- CFPB: 1-855-411-2372 | consumerfinance.gov/complaint
- DFPI: 1-866-275-2677 | dfpi.ca.gov

*Auto-generated by LexClerk • Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        readme.write_text(content)

    def organize(self, source_dir: Path):
        print(f"🚀 Starting semantic reorganization with {self.provider.upper()}...")
        processed = 0
        for file in source_dir.rglob("*"):
            if file.is_file() and file.suffix.lower() in [".pdf", ".docx", ".txt", ".png", ".jpg"]:
                text = self.extract_text(file)
                category, confidence = self.classify_document(text)

                is_dup, _ = self.fuzzy_duplicate_check(text)
                if is_dup:
                    shutil.move(str(file), self.archive / file.name)
                    print(f"→ Duplicate archived: {file.name}")
                    continue

                target_folder = self.case_root / "01_Evidence_By_Legal_Theory" / category
                target_folder.mkdir(parents=True, exist_ok=True)
                new_path = target_folder / file.name
                shutil.copy2(file, new_path)

                doc_id = hashlib.md5(str(new_path).encode()).hexdigest()
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                c.execute("INSERT OR REPLACE INTO documents VALUES (?,?,?,?,?,?,?,?)",
                          (doc_id, file.name, str(new_path), self.get_file_hash(new_path),
                           category, confidence, text[:8000], datetime.now().isoformat()))
                conn.commit()
                conn.close()

                if not (target_folder / "README.md").exists():
                    self.generate_readme(target_folder, category)

                print(f"✅ {file.name} → {category} ({confidence:.0f}%)")
                processed += 1
        print(f"🎉 Reorganization complete! {processed} documents processed.")

    def ingest(self, file_path: Path):
        print(f"📥 Delta ingest: {file_path.name} ({self.provider.upper()})")
        self.organize(file_path.parent)

    def show_status(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT category, COUNT(*) as count, AVG(confidence) as avg_conf FROM documents GROUP BY category")
        print("\n📊 Current Case Status:")
        for row in c.fetchall():
            print(f"   • {row[0]:25} | {row[1]} docs | Avg confidence: {row[2]:.1f}%")
        conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LexClerk v1.1 — Powered by llm_router")
    parser.add_argument("command", choices=["organize", "ingest", "status"])
    parser.add_argument("--source", type=str, help="Source directory for organize")
    parser.add_argument("--file", type=str, help="New file for ingest")
    parser.add_argument("--case", default="TommyLoanDispute", help="Case name")
    parser.add_argument("--provider", choices=["grok", "gemini", "local"], default="grok",
                        help="LLM provider (grok = best quality)")
    args = parser.parse_args()

    clerk = LexClerk(args.case, provider=args.provider)

    if args.command == "organize":
        source = Path(args.source) if args.source else Path(".")
        clerk.organize(source)
    elif args.command == "ingest":
        if args.file:
            clerk.ingest(Path(args.file))
    elif args.command == "status":
        clerk.show_status()