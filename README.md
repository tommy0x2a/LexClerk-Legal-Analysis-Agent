```markdown
# LexClerk v1.2 — Legal Analysis Agent

**Your AI Digital Clerk for Mortgage & Loan Disputes**  
*Now with switchable real-time research (Perplexica OR Grok tools) + full `llm_router.py` integration*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg)
![Version](https://img.shields.io/badge/version-1.2-brightgreen.svg)

> ✅ **v1.2 is live!** Added **switchable real-time legal research** powered by your `llm_router.py`.  
> Choose **Perplexica** (best citations + official .gov sources) or **Grok tools** (strongest reasoning + real-time web search).  
> Everything from v1.1 is preserved — classification, organization, deduplication, living READMEs, and SQLite tracking are unchanged.

---

## ✨ Features

- **Multi-LLM Router Integration** — Instant switching between Grok (default), Gemini, or local (Llama 3.2) via `--provider`
- **🔬 Switchable Real-Time Research Engine** — New in v1.2!  
  - **Perplexica** → Best citations from official sources (CFPB, DFPI, courtlistener.com, etc.)  
  - **Grok tools** → Strongest reasoning + DuckDuckGo-powered live search (no extra server)  
  - **None** → Zero overhead (default — keeps v1.1 behavior)
- **Semantic Reorganization** — Automatic classification into precise legal taxonomy (RESPA, UDAAP, CA HBOR, Elder Financial Abuse, etc.)
- **Fuzzy Duplicate & Version Detection** — 91%+ similarity threshold with `rapidfuzz`
- **Living README.md Files** — Auto-generated and updated per folder with statutes, deadlines, and contacts
- **SQLite Metadata Database** — Tracks documents, confidence scores, entities, and timeline
- **Delta Ingest** — Drop new files without full re-scans
- **Rich Status Dashboard** — One-command overview of case health

---

## 🚀 Quick Setup (One-Time)

```bash
pip install pymupdf rapidfuzz python-docx langchain-xai langchain-google-genai langchain-ollama langchain-core python-dotenv requests duckduckgo-search
```

**Requirements**
1. Place **`llm_router.py`** and **`research_engine.py`** in the **same folder** as `lexclerk.py`
2. Create `.env` in the project root:

```env
XAI_API_KEY=your_grok_key_here
GEMINI_API_KEY=your_gemini_key_here
# OLLAMA is local — no key needed
```

---

## 🔬 Real-Time Legal Research (New in v1.2)

LexClerk now has a **fully switchable research backend** that integrates seamlessly with your existing `llm_router.py`.

### Why Two Backends?
| Backend       | Best For                          | Citations & Sources                  | Setup Required                  | Speed & Privacy          |
|---------------|-----------------------------------|--------------------------------------|---------------------------------|--------------------------|
| **Perplexica** | Official .gov regs + case law    | Excellent (with titles + URLs)      | Run Perplexica locally         | Fast, fully private     |
| **Grok tools** | Deep reasoning + quick lookups   | Good (DuckDuckGo results)           | None (uses `duckduckgo-search`) | Fastest, no extra server|
| **None**      | Pure classification (v1.1 mode)  | N/A                                 | None                            | Zero overhead           |

### Real-Time Legal Research Setup (Windows 10/11)

#### Recommended: Docker + One-Click Batch Files (2 minutes)

1. Install **Docker Desktop** → https://www.docker.com/products/docker-desktop/
2. Download these two files into your LexClerk folder:
   - `start_perplexica.bat`
   - `stop_perplexica.bat`

**`start_perplexica.bat`** (double-click to start):
```batch
@echo off
title LexClerk - Start Perplexica
color 0a
echo =============================================
echo     Starting Perplexica for LexClerk v1.2
echo     (Docker - One Click)
echo =============================================
echo.

docker start perplexica >nul 2>&1

if %errorlevel% neq 0 (
    echo [First-time setup] Creating and starting Perplexica container...
    docker run -d -p 3000:3000 -v perplexica-data:/home/perplexica/data --name perplexica itzcrazykns1337/perplexica:latest
    echo ✅ New container created and started!
) else (
    echo ✅ Perplexica was already created and has been started.
)

echo.
echo 🌐 Perplexica is now running at: http://localhost:3000
echo First time? Open the link above and finish the quick setup (add your API keys).
echo.
pause
```

**`stop_perplexica.bat`** (double-click to stop):
```batch
@echo off
title LexClerk - Stop Perplexica
color 0c
echo =============================================
echo     Stopping Perplexica
echo =============================================
echo.

docker stop perplexica

if %errorlevel% equ 0 (
    echo ✅ Perplexica stopped successfully.
) else (
    echo No running Perplexica container found.
)

echo.
pause
```

**Usage**:
- Double-click `start_perplexica.bat` → Perplexica starts (downloads image first time)
- Open browser → **http://localhost:3000** and complete the one-time setup
- To stop → Double-click `stop_perplexica.bat`

**Pro tip**: Keep `start_perplexica.bat` on your Desktop for instant access.

---

## 📁 Project Structure (Auto-Created)

```
LexClerk_Case_YourCaseName/
├── 00_Master_Overview/
├── 01_Evidence_By_Legal_Theory/
│   ├── RESPA_Violations/
│   ├── UDAAP_Abusive_Practices/
│   ├── CA_HBOR/
│   ├── Elder_Financial_Abuse/
│   └── README.md (living!)
├── 02_Agency_Interactions/
├── ingest/
├── Archive/
├── metadata.db
├── lexclerk.py
├── research_engine.py
├── llm_router.py
├── start_perplexica.bat
└── stop_perplexica.bat
```

## 🛠️ How to Run

```bash
# 1. Classic organization (no research overhead)
python lexclerk.py organize --source "/path/to/your/unorganized/documents" --case "TommyLoanDispute" --provider grok --research-provider none

# 2. Delta ingest
python lexclerk.py ingest --file "new_servicer_letter.pdf" --research-provider none

# 3. NEW: Real-time research
# With Perplexica (best citations)
python lexclerk.py research --research-provider perplexica --query "latest CFPB guidance on force-placed insurance 2026"

# With Grok tools (best reasoning)
python lexclerk.py research --research-provider grok --query "recent California court cases on Elder Financial Abuse in mortgage disputes"

# 4. Status
python lexclerk.py status
```

**Pro tips**
- Use `--research-provider perplexica` when preparing complaints or briefs (perfect citations).
- Use `--research-provider grok` for fast internal analysis.
- Add the research flag to any command — it only activates on the `research` command.

---

## 📊 Example Research Output (Perplexica)

```
🔍 Researching: latest CFPB guidance on force-placed insurance 2026
**Answer:**
The CFPB issued updated guidance in February 2026 requiring servicers to...
**Citations & Sources:**
• CFPB Consumer Financial Protection Bureau (consumerfinance.gov)
• Recent Bulletin 2026-03 (cfpb.gov)
• Courtlistener.com docket summary
```

---

## 🗺️ Roadmap

- **v2.0** (next) — Auto complaint drafting (CFPB/DFPI personas) + merit brief generator that uses the research engine
- **v3.0** — Timeline visualization + evidence export

---

## ⚖️ Disclaimer

LexClerk is an **AI research and organization tool**. It is **not** a substitute for licensed legal advice. Always consult a qualified attorney.

---

## 🤝 Contributing

Pull requests welcome! Especially welcome:
- New research backends
- Better legal prompts
- Export templates

---

**Made for Tommy’s Loan Dispute** ❤️  
*Now with Perplexica + Grok research — the smartest digital clerk on the planet.*

---
*Last updated: March 2026 • LexClerk v1.2*
```
