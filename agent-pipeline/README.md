# AI Pulse — Autonomous Newsletter Agent Pipeline
### WIBD Workshop: Agentic AI 101

A fully working **agentic pipeline** that researches, writes, and publishes a tech newsletter autonomously — with a live dashboard, real MCP integrations, and human-in-the-loop approval.

---

## 🏗️ Project Structure

```
agent-pipeline/
├── backend/               # Express + LangChain pipeline
│   └── src/
│       ├── server.js      # Entry point (port 3001)
│       ├── state.js       # Shared SSE state
│       ├── routes/
│       │   └── pipeline.js  # REST + SSE endpoints
│       └── pipeline/
│           ├── index.js          # Pipeline orchestrator (5 nodes)
│           ├── agents/
│           │   ├── writerAgent.js    # Gemini ↔ Gemma3 switchable
│           │   └── researchAgent.js  # Routes links to MCPs
│           ├── mcps/
│           │   └── mockMcps.js   # Real MCP stdio clients
│           └── hooks/
│               └── piiSanitizer.js  # Pre-generation hook
└── frontend/              # React + Vite dashboard (port 5173)
    └── src/
        ├── App.jsx        # Full dashboard (all-in-one)
        └── App.css        # Dark glassmorphism theme
```

---

## 🚀 Quick Start

### 1. Backend
```bash
cd backend
npm install
# Set your keys (optional — works without them in seed/fallback mode)
$env:GEMINI_API_KEY = "your_key"
$env:GITHUB_PERSONAL_ACCESS_TOKEN = "ghp_yourtoken"
$env:WHATSAPP_MCP_PATH = "C:/Users/yourname/whatsapp-mcp"  # optional, see below
npm run dev
# → http://localhost:3001
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

---

## 🔌 MCP Configuration

### Antigravity CLI (`.gemini/settings.json`) — already created for you

```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "npx",
      "args": ["-y", "@kimtaeyoon83/mcp-server-youtube-transcript"],
      "description": "NO auth — YouTube timedtext API"
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "env": { "PYTHONIOENCODING": "utf-8" },
      "description": "NO auth — fetches any public URL"
    },
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "description": "OAuth via VS Code GitHub Copilot — NO PAT needed in the IDE"
    }
  }
}
```

### GitHub — Two Contexts (important!)

| Context | How | Auth |
|---|---|---|
| **Antigravity CLI / VS Code** | Remote MCP `https://api.githubcopilot.com/mcp/` | ✅ OAuth (no PAT) via GitHub Copilot |
| **Node.js Pipeline** (publish step) | GitHub REST API via `fetch()` | ⚠️ `GITHUB_PERSONAL_ACCESS_TOKEN` env var |

The remote OAuth MCP is browser/IDE-bound — it cannot be called from a Node.js child process. The pipeline uses the REST API directly instead.

### All MCPs at a Glance

| MCP | Auth | Use in Pipeline |
|---|---|---|
| **WhatsApp MCP** | ⚡ QR code scan (once) | Fetch saved notes/links from personal WhatsApp |
| YouTube Transcript | ✅ None | Extract transcripts from YT links |
| Fetch (web) | ✅ None | Scrape articles, podcast show notes |
| GitHub (IDE) | ✅ OAuth, no PAT | Demo GitHub ops inside Antigravity |
| GitHub (pipeline) | ⚠️ PAT env var | Publish newsletter to GitHub Pages |

---

## 💬 WhatsApp MCP Bridge Setup (lharries/whatsapp-mcp)

The pipeline reads your saved WhatsApp messages/links using a local Go bridge. Without setup it falls back to seed data automatically.

### Prerequisites
- **Go** 1.21+ — [golang.org/dl](https://golang.org/dl)
- **uv** Python package manager — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Windows only**: CGO_ENABLED + MSYS2/GCC compiler

### Setup (all platforms)
```bash
# 1. Clone the repo (anywhere on your machine)
git clone https://github.com/lharries/whatsapp-mcp.git
cd whatsapp-mcp

# 2. Windows only — enable CGO (skip on Mac/Linux)
go env -w CGO_ENABLED=1
# Also install MSYS2 from https://www.msys2.org and add ucrt64\bin to PATH

# 3. Start the Go bridge (keep this terminal open!)
cd whatsapp-bridge
go run main.go
# → First run: scan QR code with WhatsApp mobile app
# → Subsequent runs: auto-reconnects (re-auth every ~20 days)
```

### Configure the pipeline
```powershell
# In backend .env or PowerShell before starting backend:
$env:WHATSAPP_MCP_PATH = "C:/Users/yourname/whatsapp-mcp"
```

### What it does
Once running, `fetchWhatsAppNotes(topic, days)` calls the `list_messages` MCP tool
to retrieve messages matching the topic keyword from the last N days. Any YouTube
or web links found in those messages are routed to the Research Agent automatically.

> **Workshop tip:** If you don't want to set up the bridge, the pipeline still works —
> it auto-falls-back to realistic seed data with real links that the Research Agent processes.

## 🦙 Switch to Local Gemma3 (Offline Demo)

```bash
# 1. Ensure Ollama is running with Gemma3
ollama run gemma3

# 2. Option A: Select in Dashboard UI → "Local Gemma3 (Ollama)"
# 3. Option B: Set env var before starting backend
$env:MODEL = "ollama"
npm run dev
```

---

## 🎓 Workshop Hands-On Exercises

| Exercise | File to Edit | Concept Covered |
|---|---|---|
| Change newsletter format | `writerAgent.js` → `WRITER_SYSTEM_PROMPT` | Prompt engineering |
| Add Reddit as a new source | `mockMcps.js` + `researchAgent.js` | New MCP tool |
| Enable SQLite memory | `pipeline/index.js` — add SqliteSaver | Agent memory |
| Add token cache | `writerAgent.js` — add InMemoryCache | Token caching |
| Create a new Skill | `.agents/skills/new_skill/SKILL.md` | Antigravity skills |
| Test PII hook | Send topic "my bank password" | Input guardrails |

---

## 📡 API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/pipeline/run` | Start a pipeline run |
| `GET` | `/api/pipeline/events/:runId` | SSE event stream |
| `POST` | `/api/pipeline/approve/:runId` | Approve/reject newsletter |
| `GET` | `/api/pipeline/newsletter/:runId` | Get newsletter markdown |
| `POST` | `/api/pipeline/cron` | Schedule recurring runs |
| `DELETE` | `/api/pipeline/cron` | Stop cron |
