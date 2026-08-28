# ⬡ Synthetix — Multi-Agent Deep Research Engine

Synthetix turns a single topic into a polished, structured research report. Four specialized AI agents work in sequence — searching the web, scraping the most relevant source, drafting a report, and critiquing it — all orchestrated with LangChain and powered by Mistral LLM.

**🔗 Live Demo:** [research-agent-jkbt2zpsrckyad8eeeqsqd.streamlit.app](https://research-agent-jkbt2zpsrckyad8eeeqsqd.streamlit.app/)

---

## How It Works

Synthetix runs a 4-step agentic pipeline for every query:

```
Topic Input
    │
    ▼
1. Search Agent   →  Queries the web via Tavily API, returns top results (titles, URLs, snippets)
    │
    ▼
2. Reader Agent   →  Picks the most relevant URL and scrapes its full content with BeautifulSoup
    │
    ▼
3. Writer Chain   →  Synthesizes search + scraped content into a structured report
    │                 (Introduction, Key Findings, Conclusion, Sources)
    ▼
4. Critic Chain   →  Reviews the report, scores it out of 10, and flags strengths/weaknesses
    │
    ▼
Final Report + Critique (downloadable as .md)
```

The Search and Reader steps are true **agents** — built with LangChain's `create_agent`, they decide autonomously how to use their tools (`web_search`, `scrape_url`) rather than following a fixed script. The Writer and Critic steps are **LCEL chains** — deterministic prompt → LLM → parser pipelines, since their job is generation/evaluation rather than tool-driven decision-making.

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | Mistral (`mistral-small-2506`) via `langchain-mistralai` |
| Agent Framework | LangChain (`create_agent`) |
| Chains | LangChain Expression Language (LCEL) |
| Web Search | Tavily API |
| Web Scraping | Requests + BeautifulSoup |
| Frontend | Streamlit (custom dark-themed UI, live pipeline status tracking) |
| Config | python-dotenv |

---

## Project Structure

```
synthetix/
├── app.py            # Streamlit frontend — UI, session state, pipeline trigger
├── pipeline.py        # CLI entry point — runs the full pipeline end-to-end
├── agents.py          # Agent + chain definitions (search agent, reader agent, writer chain, critic chain)
├── create_tools.py    # LangChain tools — web_search (Tavily), scrape_url (BeautifulSoup)
├── requirements.txt
└── .env                # TAVILY_API_KEY, MISTRAL_API_KEY (not committed)
```

---

## Features

- 🔍 **Autonomous web search** — real-time results via Tavily, no hardcoded sources
- 📄 **Automatic content extraction** — agent scrapes the most relevant page for deeper context
- ✍️ **Structured report generation** — consistent Introduction / Key Findings / Conclusion / Sources format
- 🧠 **Self-critique loop** — a dedicated critic agent scores and reviews the report for quality
- 📊 **Live pipeline visualization** — Streamlit UI shows each agent's status in real time (idle → running → done)
- ⬇️ **One-click export** — download the final report as a Markdown file

---

## Running Locally

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd synthetix
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** — create a `.env` file:
   ```
   TAVILY_API_KEY=your_tavily_api_key
   MISTRAL_API_KEY=your_mistral_api_key
   ```

4. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

   Or run the pipeline from the command line:
   ```bash
   python pipeline.py
   ```

---

## Example

**Input:** `LLM agents 2025`

**Output:** A structured report covering recent developments, key findings backed by scraped source content, a list of cited URLs, and an automated critic review scoring the report's depth and accuracy.

---

## Roadmap / Possible Improvements

- Expand the Search Agent to scrape and synthesize **multiple** sources instead of one
- Add a feedback loop where the Critic's suggestions automatically trigger a Writer revision pass
- Support PDF export alongside Markdown
- Add source-level citation links inline within the report body

---

## License

MIT
