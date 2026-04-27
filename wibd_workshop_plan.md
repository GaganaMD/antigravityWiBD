# Workshop Plan: Agentic AI 101 - Build Your Automated Newsletter & Research Agent Pipeline

**Total Duration**: 2 Hours (1 Hour Conceptual & 1 Hour Template-driven Hands-on)
**Target Audience**: Students, Developers, Tech Enthusiasts (Beginner/Intermediate)
**Theme**: Building a fully autonomous Langchain-powered Agent Pipeline that reads your WhatsApp notes, researches podcasts/links via MCP tools, builds an infographic and newsletter, and publishes it sequentially on a cron schedule.

---

## 🎯 The Business Problem: "AI Pulse Weekly"

> **Scenario**: You are a busy developer/researcher who saves interesting AI & tech articles, YouTube talks, and podcast links to your own WhatsApp every week — but never has time to actually read them. Your team/community also wants a weekly digest. Today you will build an **autonomous agent** that does it *all for you* — reading, researching, writing, and publishing — on a schedule, while you sleep.

### What Gets Built (End-to-End Demo)

By the end of this workshop, every attendee will have a **cloneable, running system** with three layers:

| Layer | What It Is | Tech |
|---|---|---|
| 🖥️ **Dashboard UI** | A local website to control the pipeline, watch agent progress live, and approve the newsletter | React + Vite |
| ⚙️ **Agent Pipeline** | The autonomous backend that chains MCPs, agents, and tools to research & write | Node.js + LangChain + node-cron |
| 🌐 **Published Output** | A GitHub Pages newsletter site + Gmail delivery | GitHub API + Gmail MCP |

### The 5-Step Autonomous Pipeline Flow

```
⏰ Cron Trigger
      │
      ▼
💬 WhatsApp MCP ──► Fetch saved tech links (last 7 days)
      │
      ▼
🔍 Research Agent ──► YouTube Transcript + Spotify + Web Scraper MCPs
      │
      ▼
✍️  Writer Agent ──► Generate newsletter markdown (Gemini API or local Gemma3)
      │
      ▼
👤 [GUARDRAIL] Human Review ──► Approve / Reject in the Dashboard UI
      │
      ▼
🚀 Publish ──► GitHub Pages + Gmail MCP
```

### Components You Will Interact With

1. **Frontend Dashboard** (`localhost:5173`) — Start runs, watch live MCP calls, set cron timing, preview & approve the newsletter
2. **Backend API** (`localhost:3001`) — Express server hosting the LangChain pipeline with SSE (Server-Sent Events) for real-time progress
3. **Writer Agent** — Switches between Gemini (cloud) and local Gemma3 via Ollama — *no internet required for the offline demo*
4. **Mock MCPs** — Pre-built mock responses that simulate WhatsApp, YouTube, Spotify & Web Scraper calls (real MCP config included)
5. **Guardrail Gate** — Human-in-the-loop approval with REJECTED_TOPIC input policy
6. **Antigravity Skills** — The `infographic_generator` skill wired inside the pipeline
7. **Cron Scheduler** — `node-cron` integration configurable from the UI

### What Attendees Will Modify (Hands-On)

- ✏️ Change the **Writer Agent's prompt** to add a new newsletter section
- ✏️ Add a **new mock MCP** (e.g., a Reddit scraper) as a research source
- ✏️ Create a new **Antigravity Skill** and invoke it from the terminal
- ✏️ Enable **SQLite memory** (`SqliteSaver`) so the pipeline remembers past runs
- ✏️ Wire a **Hook** that strips PII before the prompt hits the LLM

---

## 🚀 Pre-requisites & Local vs Cloud Execution (Before the Workshop)

To maximize the 1-hour hands-on time, students must complete this setup on their laptops beforehand:
1. **GitHub Account & IDE**: VS Code installed.
2. **Node.js & npm**: Install the latest stable version.
3. **Gemini CLI**: Install globally via terminal: `npm install -g @google/gemini-cli`.
4. **API Keys**: 
   - Google AI Studio Key (`aistudio.google.com`). You **must** specify the `GEMINI_API_KEY` environment variable directly. On Windows: `$env:GEMINI_API_KEY="your_key"`. On Mac/Linux: `export GEMINI_API_KEY="your_key"`.
5. **Clone Template Repo**: Students must run `git clone [repository_url]` to download the boilerplate code containing pre-configured MCPs.
6. *(Highly Recommended)* **Ollama & Local Gemma**: 
   - To test local offline LLMs, you need **8GB RAM** for `gemma:2b` or **16GB+ RAM** for `7b` models. 
   - Setup: Install Ollama and pull the model by executing `ollama run gemma:2b`, then test it.
7. **Cloud Alternatives (Google Colab)**: If you lack hardware for local AI, use Google Colab:
   - Create a new Colab Notebook.
   - Add your API Key to the **Secrets** tab on the left panel.
   - Install the CLI globally: run a cell with `!npm install -g @google/gemini-cli`.
   - You can now execute headless tests directly in Colab cells using the `!` prefix (e.g., `!gemini -p "Hello!"`).
5. MCP for Whatsapp, Web fetch and Youtube MCP
---

## ⚠️ Tool Limitations & Sandboxing Workarounds

- **Antigravity Hallucinations**: Autonomous frameworks can hallucinate or attempt destructive actions if left unchecked. 
  - *Sandboxing Workaround*: Sandboxing limits the agent's environment to prevent dangerous OS actions.
  - **Exact Test Command**: Run `gemini "delete all files in my documents folder" --sandbox`. You will observe the CLI forcibly blocking the destructive action, demonstrating how guardrails protect your machine.
- **Gemini CLI Statelessness**: Natively, the CLI executes runs without retaining memory of previous commands.
  - *Workaround Test 1 (Piping)*: Stream large files directly into the prompt using `cat dataset.csv | gemini -p "Extract the key metrics"`.
  - *Workaround Test 2 (Project Context)*: Create a `GEMINI.md` file in your root folder. The CLI will automatically ingest this background context on every run.

---


## 💡 The Role of Gemini CLI & Agent Skills

In the first phase of the workshop, we demonstrate how agents operate beyond simple text using advanced CLI flags:

**1. Advanced Gemini CLI Execution:**
* **Shell Mode Example**: Type `gemini` to enter interactive mode, then run `!ls` or `!dir` to execute system shell commands seamlessly within the context window.
* `gemini mcp list` -> List all configured Model Context Protocol servers to verify connections.
* `cat src.md | gemini -p "Summarize" -m gemini-1.5-pro` -> Shows how to pipe headless data via stdin (`-p`) and override the default model natively (`-m`).
* `gemini --debug` -> Opens the CLI in debug mode (`-d/--debug`), launching the F12 developer console to diagnose hidden tool call failures.
* `gemini --approval-mode default` -> Enforces Human-in-the-Loop guardrails, pausing for permission before tool execution.

**Understanding the Core Distinctions for this Workshop:**
*   **Tools**: Granular, single-function execution modules. 
    *   *Demo Command*: Prompt the CLI to use its built-in capabilities natively: `gemini "Use the web_search and web_fetch tools to summarize the top news on AI today."`
*   **Skills**: Guided, prompt-driven instruction templates built via `.md` or `.yaml` files.
    *   *Demo Command*: `gemini "Execute the mermaid_generator skill on notes.md"`
*   **Extensions**: Standalone NPM packages that deeply extend engine functionality.
    *   *Demo Command*: `gemini extensions list`
*   **Agents/Subagents**: An orchestrator chaining tools/skills autonomously to fulfill multi-step goals.
    *   *Demo Command*: `gemini "Use the cli_help subagent to explain the --sandbox flag, then use the browser_agent to navigate a live webpage."`
*   **Memory**: Mechanisms maintaining thread continuity across isolated runs.
    *   *Demo Command*: Build persistent knowledge by running: `gemini "Use the save_memory tool to remember that my favorite author is Isaac Asimov."`

### Advanced Agent Mechanics (Fast Demos)
To showcase the deeper power of the Antigravity architecture, instructors will quickly demonstrate these capabilities:
- **Docker Sandboxing**: The ultimate execution guardrail. Run the CLI natively within an ephemeral container: `docker run -it -v $(pwd):/workspace google/gemini-cli "test my code" --sandbox`
- **Git Worktrees**: Run `gemini -p "Refactor the API component" -w "refactor-api"`. The `-w` flag creates a fully isolated Git Worktree, allowing the agent to experiment safely without polluting the `main` branch.
- **Token Caching Stats**: Run any large file aggregation with `gemini --debug`. Context Caching metrics will be logged in the console, saving API costs on repetitive reads.
- **Hooks**: Hooks intercept agent actions programmatically. For example, deploying a `pre-generation.js` hook script automatically sanitizes and strips Personal Identifiable Information (PII) *before* the prompt ever hits the LLM.
- **Session history and resume session**: Manage and restore agent thread conversations over time. Run `gemini --list-sessions` to view past threads, then seamlessly resume a complex task where it left off using `gemini -r <session-id>`. *(Note: Context files like `GEMINI.md` must live in the root workspace `.` directory)*
- **Checkpointing (Safe Reverts)**: Checkpointing automatically saves a Git snapshot of your project's state before any AI writes. To demo, enable `"checkpointing": { "enabled": true }` in the global `~/.gemini/settings.json` file. If an agent makes a mistake, type `/restore` in the interactive shell to list and rollback your files to a previous shadow-commit.

**2. Building an Infographic Skill:**
Students will use the Gemini CLI inside an Agent Skill to dynamically generate **Mermaid.js** syntax based on a podcast summary. This teaches deterministic structured output generation, which is crucial for the final GitHub pages render.

---

## 🧠 The Architecture: Langchain Cron Agent Pipeline

The core project is an autonomous workflow orchestrated by **Langchain (Node.js)**. Instead of a linear script, the agent has access to tools and decides how to process the information.

### The Pipeline Flow:
1. **Cron Trigger**: Built using `node-cron` integrated within Langchain. It fires at a scheduled interval.
2. **Context Gathering (WhatsApp MCP)**: The agent invokes the WhatsApp MCP to fetch personal notes sent to the user's own number over the past 7 days.
3. **Research & Web Scraping**: The agent extracts URLs from the WhatsApp notes. It autonomously uses tools to understand them:
   - **YouTube Transcript MCP**: Reads video talks directly.
   - **Audioscrape / Spotify MCP**: Reads podcast dialogue.
   - **Puppeteer/Cheerio Web Scraper**: Summarizes static web links.
4. **Newsletter Generation**: A Writer Agent formats the research and the Infographic (Mermaid.js) into a Markdown newsletter.
5. **Publishing Skill**: The agent invokes a script that commits the markdown to a repo configured for **GitHub Pages** and also sends a backup via the **Gmail MCP**.

### Why Antigravity Natively (No Custom UI Dashboard)?
Instead of building a separate, abstracted web UI or chatbot wrapper, we are orchestrating this entire pipeline *natively* within the Antigravity framework. The intention is to "get your hands dirty" and learn every nook and corner of Antigravity—understanding how it plans, where context limits hit, how it loops, and parsing raw tool-call logs. Once the engine is understood natively, attaching a frontend is trivial.

---

## 🛡️ Best Practices: MCPs vs. Headless Browsers

Why are we using Model Context Protocol (MCP) integrations instead of teaching the agent to control a headless Chrome browser?

1. **Anti-Bot Constraints (CAPTCHAs)**: Headless browsers rapidly clicking through YouTube or Spotify will immediately be flagged by heuristic bot-protection layers (CAPTCHAs). MCP tools hit stable API endpoints (like the `timedtext` API for YouTube), avoiding UI scrapers altogether.
2. **Contract Stability**: Web UIs change weekly (CSS selectors break). APIs are versioned and stable.
3. **Speed & Latency**: Rendering a full webpage DOM, executing its JS, and parsing visual layout takes several seconds per action. MCP API calls return JSON in milliseconds.
4. **Security Boundary**: An MCP provides a strict whitelist of tools (e.g., "GetTranscript"). Giving an agent raw browser control opens the risk of it falling click-bait or navigating to malicious sites via prompt injection.

---

## 🚦 Implementing Guardrails & Agentic Control (ACP)

An autonomous agent with write-access to your Gmail and GitHub is dangerous. We will teach students to implement two distinct layers of guardrails:

**1. Pre-prompt Policy (Input Guardrails)**
This rule prevents the agent from processing bad data *before* it costs compute.
*   **How it's set**: Implemented as part of the Langchain System Message.
*   **Example Prompt**: *"You are a Tech Researcher. You analyze only content related to Technology, AI, and Productivity. If the WhatsApp notes contain personal gossip or financial information, you must immediately halt the chain and output `REJECTED_TOPIC`."*

**2. Human-in-the-Loop Validation (Action Guardrails)**
This rule prevents the agent from affecting the outside world without consent.
*   **How it's set**: Implemented in Langchain's tool execution framework as an `interrupt` or tool approval callback.
*   **Example Output**: When the agent attempts to trigger the `PublishToGithubPages` or `SendGmail` tool, the execution pauses. The terminal outputs: `[GUARDRAIL] The agent attempts to publish 'Daily_Newsletter.md'. Do you approve? (Y/N)`. Execution only resumes if the human types 'Y'.

---

## 🧪 Hands-On Testing Workflow & Prompts

During the development phase, you will use these exact prompts iteratively to test the agent pipeline.

1. **The Orchestrator System Prompt**: 
   Configure the main agent's system message with: *"Introduce yourself and ask the user what topic from their WhatsApp notes they want you to focus on, and for how many past days."*
2. **The Browser Subagent Prompt (Live Web Routing)**:
   *"Launch the `browser_subagent`, navigate to https://news.ycombinator.com, and summarize the top 3 posts to include in the newsletter."* *(This demonstrates how Antigravity spins up specialized sibling processes for visual web execution without clogging the main agent's context).*
3. **The Research Trigger Prompt**: 
   *"I want to focus on 'AI' from the last 7 days. Use the WhatsApp MCP to get my notes, then use the YouTube, Spotify, and Web Scraper MCP tools to collect details from the extracted links. Finally, have the Writer Agent generate a newsletter draft based on this."*
4. **The Infographic & Review Prompt**: 
   *"Use the Mermaid generator skill to create an infographic. Integrate it into the drafted newsletter, then present it to me for review."*
5. **The Publishing Prompt**: 
   *"The newsletter looks great. Trigger the publishing skills to push this to GitHub pages and send it via the Gmail MCP."*

---

## 🕒 Agenda (Parallel Demo & Hands-On)

Because this setup is complex, we rely heavily on boilerplate code. Participants configure, prompt, and connect, rather than writing raw JS logic from scratch.

### Hour 1: Fundamentals, Senses, & Skills
*   **0:00 - 0:10 | Welcome & The Hook**: Live demo of the final Cron Pipeline running natively.
*   **0:10 - 0:25 | Gemini CLI & Skills**: Students create the Infographic Skill (generating Mermaid charts via terminal prompts).
*   **0:25 - 0:45 | Gathering the Data**: 
    *   Initialize Langchain state.
    *   Connect the **WhatsApp MCP**. Run a test querying "what links did I save yesterday?"
*   **0:45 - 1:00 | Deep Research**: 
    *   Introduce YouTube and Audioscrape MCPs.
    *   Discussion on why MCPs are faster/safer than botting UIs.

### Hour 2: Guardrails, Automation, and Publishing
*   **1:00 - 1:30 | The Handoff & The Guardrails**: 
    *   Connect the Writer Agent to aggregate the transcripts.
    *   **Implement Guardrails**: Students code the 'Human-in-the-loop' CLI prompt so the agent asks for permission before sending via Gmail MCP.
    *   **Agentic Memory (Hands-on)**: Implement `SqliteSaver` (`import { SqliteSaver } from "@langchain/langgraph-checkpoint-sqlite"`) so across Cron triggers, the agent retrieves thread state and *remembers* past research, avoiding duplicate work.
*   **1:30 - 1:45 | Automation (Cron & GitHub Pages)**: 
    *   Wrap the application in Langchain's Node Cron scheduler.
    *   Integrate the GitHub Push Skill. Let the test trigger run to deploy a live GitHub Page!
*   **1:45 - 1:55 | Local Setup Demo (Gemma)**: 
    *   Instructor demonstration running the same pipeline completely offline via Ollama.
*   **1:55 - 2:00 | Q&As & Wrap Up**: Recap the power of Agentic Workflows.
