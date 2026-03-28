```markdown
# LexClerk v2.0 — Legal Analysis Agent

**Your AI Digital Clerk for Mortgage & Loan Disputes**  
*Now with switchable real-time research (Vane OR Perplexica OR Grok tools) + full `llm_router.py` integration*

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen.svg)
![Version](https://img.shields.io/badge/version-2.0-brightgreen.svg)

> ✅ **v2.0 is live!** Major upgrade: Added **Vane** (lighter, simpler Docker research engine with bundled SearxNG) alongside Perplexica and Grok tools.  
> Choose **Vane** (recommended for most users), **Perplexica** (feature-rich UI), or **Grok tools** (no extra server).  
> Everything from v1.1 is preserved and improved — classification, organization, deduplication, living READMEs, and SQLite tracking are unchanged and faster.

---

## ✨ Features

- **Multi-LLM Router Integration** — Instant switching between Grok (default), Gemini, or local (Llama 3.2) via `--provider`
- **🔬 Switchable Real-Time Research Engine** — New in v2.0!  
  - **Vane** → Simplest 1-command Docker setup + bundled SearxNG (recommended)  
  - **Perplexica** → Rich UI + strong official .gov sources  
  - **Grok tools** → Strongest reasoning + DuckDuckGo live search (zero extra setup)  
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

3. **Install Ollama** (for local models): https://ollama.com
4. **Install Docker Desktop** (for Vane or Perplexica)

---

## 🔬 Real-Time Legal Research (New in v2.0)

LexClerk now has a **fully switchable research backend** that integrates seamlessly with your existing `llm_router.py`.

### Why These Backends?
| Backend       | Best For                          | Setup Difficulty | Citations & Sources                  | Speed & Privacy          |
|---------------|-----------------------------------|------------------|--------------------------------------|--------------------------|
| **Vane/Perplexica**      | Rich UI + official .gov regs      | Very Easy (1 command) | Excellent + bundled SearxNG         | Fast, fully private     |
| **Grok tools**| Deep reasoning + quick lookups   | None             | Good (DuckDuckGo)                   | Fastest, no extra server|
| **None**      | Pure classification (v1.1 mode)  | None             | N/A                                 | Zero overhead           |

### Vane Setup (Recommended — Simplest)

Vane can be easily run using Docker. Simply run the following command:

```bash
docker run -d -p 3000:3000 -v vane-data:/home/vane/data --name vane itzcrazykns1337/vane:latest
```

This will pull and start the Vane container with the bundled SearxNG search engine.  
Once running, open your browser and navigate to **http://localhost:3000**.  
You can then configure your settings (API keys, models, etc.) directly in the setup screen.

**Note**: The image includes both Vane and SearxNG, so no additional setup is required. The `-v` flag creates persistent volumes for your data and uploaded files.

**Stop Vane**:
```bash
docker stop vane
```

### 🖥️ Local + Perplexica Setup (Full Ollama Connection Guide)

**This is the most important part** — Perplexica runs in Docker and needs a special trick to talk to your host Ollama.

#### Step 1: Pull the recommended models (in Terminal/Command Prompt)
```bash
ollama pull llama3.2          # Best for LexClerk classification + research
ollama pull nomic-embed-text  # Best small embedding model
```

#### Step 2: Start Perplexica
Double-click `start_perplexica.bat` (it will download the image the first time).

#### Step 3: Configure Ollama Connection in Perplexica UI
1. Open your browser → **http://localhost:3000**
2. Go to **Settings** → **Manage Connections** (or the Connections tab)
3. Edit or create a new **Ollama** connection:
   - **Connection Type**: Ollama
   - **Base URL**: `http://host.docker.internal:11434` ← **CRITICAL on Windows/Mac** (this is Docker’s special hostname to reach your host machine)
   - **API Key**: `dummy` (Ollama doesn’t need one, but Perplexica requires a value)
   - Click **Save & Test** — it should succeed and list your models
4. Refresh the page if models don’t appear immediately.

#### Step 4: Select Models
- **Chat Model**: `llama3.2 - llama3.2:latest` (or simply `llama3.2:latest`)
- **Embedding Model**: `nomic-embed-text` (recommended) or `Transformers - all-MiniLM-L6-v2`
- Save changes.

#### Step 5: Restart Perplexica (if needed)
- In Docker Desktop → restart the `perplexica` container  
- Or run in terminal: `docker restart perplexica`

**You’re done!** Perplexica is now fully connected to your local Llama 3.2 with zero cost and 100% privacy.

---

### Real-Time Legal Research Setup (Windows 10/11) — One-Click Batch Files

Download these two files into your LexClerk folder (already included in the repo):

**`start_perplexica.bat`** (double-click to start)  
**`stop_perplexica.bat`** (double-click to stop)

**Usage**:
- Double-click `start_perplexica.bat`
- Open **http://localhost:3000** and finish the quick one-time setup (now with the Ollama connection above)
- To stop → Double-click `stop_perplexica.bat`
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
├── start_perplexica.bat          # (for Perplexica users)
└── stop_perplexica.bat
```

---

## 🛠️ How to Run

```bash
# 1. Classic organization (no research overhead)
python lexclerk.py organize --source "/path/to/your/unorganized/documents" --case "LoanDispute" --provider grok --research-provider none

# 2. Delta ingest
python lexclerk.py ingest --file "new_servicer_letter.pdf" --research-provider none
python lexclerk.py ingest --file "new_servicer_letter.pdf"

# 3. Real-time research (Perplexica = best citations)
# Vane (recommended)
python lexclerk.py research --research-provider vane --query "latest CFPB guidance on force-placed insurance 2026"

# 4. Grok tools (best reasoning)
python lexclerk.py research --research-provider grok --query "..."

# 5. Full analysis + merit brief
python lexclerk.py analyze --provider grok --research-provider vane

# 6. Generate CFPB complaint (uses your entire case database + live research)
python lexclerk.py draft-complaint --agency CFPB

# 7. Generate DFPI complaint
python lexclerk.py draft-complaint --agency DFPI

# 8. Professional acceptance letter to a consumer law firm
python lexclerk.py draft-letter --firm "Smith Consumer Law Group"

# 9. Status
python lexclerk.py status
```

**Pro tips**
- Use `--research-provider vane` for complaints/briefs (perfect citations)
- Use `--research-provider grok` for pure speed with no Docker
- All drafts saved in `Archive/Drafts/` with timestamps
- Add the research flag to any command — it only activates on the `research` command.

---

## 📊 Example Research Output (Vane)

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

- **v3.0** — Timeline visualization + evidence export

---

## ⚖️ Disclaimer

LexClerk is an **AI research and organization tool**. It is **not** a substitute for licensed legal advice. Always consult a qualified attorney.

---

## 🤝 Contributing

Pull requests welcome! Especially:
- New research backends
- Better legal prompts
- Export templates

---
