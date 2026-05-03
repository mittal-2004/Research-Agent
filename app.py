import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Synthetix · Deep Research Engine",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Epilogue:ital,wght@0,300;0,400;0,500;0,700;0,800;1,700;1,800&family=Fira+Code:wght@300;400;500&display=swap');

:root {
    --bg:          #06080f;
    --bg2:         #0b0f1c;
    --bg3:         #101525;
    --bg4:         #141a2e;
    --border:      #1a2138;
    --border2:     #222d48;
    --text:        #c8d4f0;
    --text-dim:    #5a6a90;
    --text-muted:  #2e3d60;
    --violet:      #7c5cfc;
    --violet-glow: rgba(124,92,252,0.15);
    --violet-dim:  rgba(124,92,252,0.08);
    --sky:         #38bdf8;
    --crimson:     #f43f5e;
    --crimson-glow:rgba(244,63,94,0.1);
    --emerald:     #34d399;
    --gold:        #fbbf24;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; }

html, body, [class*="css"] {
    font-family: 'Epilogue', sans-serif;
    color: var(--text);
}

.stApp {
    background: var(--bg);
    background-image:
        radial-gradient(ellipse 70% 45% at 10% 0%, rgba(124,92,252,0.1) 0%, transparent 55%),
        radial-gradient(ellipse 50% 35% at 90% 100%, rgba(56,189,248,0.06) 0%, transparent 50%),
        url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none'%3E%3Cg fill='%23ffffff' fill-opacity='0.013'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 5rem; max-width: 1280px; }

/* ── TOPBAR ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 0 1.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 3.5rem;
}
.brand { display: flex; align-items: center; gap: 0.65rem; }
.brand-hex { font-size: 1.35rem; color: var(--violet); line-height: 1; }
.brand-name {
    font-family: 'Epilogue', sans-serif;
    font-size: 1.35rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    color: #e2eaff;
}
.brand-dot { color: var(--violet); }
.topbar-tag {
    font-family: 'Fira Code', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--text-dim);
    border: 1px solid var(--border2);
    padding: 0.22rem 0.65rem;
    border-radius: 4px;
}

/* ── HERO ── */
.hero { text-align: center; padding: 1rem 0 3rem; }
.hero-kicker {
    font-family: 'Fira Code', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--violet);
    margin-bottom: 1.1rem;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
}
.hero-kicker::before, .hero-kicker::after {
    content: '';
    display: inline-block;
    width: 28px; height: 1px;
    background: var(--violet);
    opacity: 0.5;
}
.hero h1 {
    font-family: 'Epilogue', sans-serif;
    font-size: clamp(2.8rem, 6vw, 4.8rem);
    font-weight: 800;
    font-style: italic;
    line-height: 1.05;
    letter-spacing: -0.04em;
    color: #e2eaff;
    margin-bottom: 1rem;
}
.hero h1 em {
    font-style: normal;
    color: var(--violet);
    text-shadow: 0 0 40px rgba(124,92,252,0.5);
}
.hero-desc {
    font-size: 1rem;
    font-weight: 300;
    color: var(--text-dim);
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.7;
}

/* ── DIVIDER ── */
.glow-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(124,92,252,0.4), rgba(56,189,248,0.2), transparent);
    margin: 1.5rem 0 2.5rem;
}

/* ── INPUT SHELL ── */
.input-shell {
    background: var(--bg2);
    border: 1px solid var(--border2);
    border-radius: 14px;
    padding: 1.8rem 2rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 0.5rem;
}
.input-shell::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--violet), var(--sky), transparent);
    border-radius: 14px 14px 0 0;
}
.input-shell-label {
    font-family: 'Fira Code', monospace;
    font-size: 0.64rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--violet);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.input-shell-label::before { content: '▸'; font-size: 0.7rem; }

/* Streamlit input overrides */
.stTextInput > label { display: none !important; }
.stTextInput > div > div > input {
    background: var(--bg3) !important;
    border: 1px solid var(--border2) !important;
    border-radius: 8px !important;
    color: #e2eaff !important;
    font-family: 'Epilogue', sans-serif !important;
    font-size: 1.02rem !important;
    font-weight: 400 !important;
    padding: 0.8rem 1rem !important;
    caret-color: var(--violet) !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
.stTextInput > div > div > input::placeholder { color: var(--text-muted) !important; }
.stTextInput > div > div > input:focus {
    border-color: var(--violet) !important;
    box-shadow: 0 0 0 3px var(--violet-glow) !important;
    outline: none !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #7c5cfc 0%, #5a3fe0 100%) !important;
    color: #fff !important;
    font-family: 'Epilogue', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.93rem !important;
    letter-spacing: 0.03em !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.8rem !important;
    width: 100% !important;
    cursor: pointer !important;
    box-shadow: 0 4px 24px rgba(124,92,252,0.3) !important;
    transition: transform 0.15s, box-shadow 0.2s !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(124,92,252,0.45) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Chips */
.chips-row {
    display: flex; flex-wrap: wrap;
    align-items: center; gap: 0.45rem;
    margin-top: 1rem;
}
.chips-label {
    font-family: 'Fira Code', monospace;
    font-size: 0.6rem; letter-spacing: 0.12em;
    color: var(--text-muted); text-transform: uppercase;
}
.chip {
    background: var(--bg4);
    border: 1px solid var(--border2);
    border-radius: 5px;
    padding: 0.22rem 0.6rem;
    font-size: 0.73rem;
    color: var(--text-dim);
    font-family: 'Epilogue', sans-serif;
}

/* ── PIPELINE ── */
.pipeline-heading {
    font-family: 'Fira Code', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 1.1rem;
    padding-left: 0.2rem;
}

.step-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 0.7rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s, background 0.3s;
}
.step-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 3px;
    background: var(--text-muted);
    opacity: 0.2;
    transition: background 0.3s, opacity 0.3s;
}
.step-card.active { border-color: rgba(124,92,252,0.4); background: var(--violet-dim); }
.step-card.active::before { background: var(--violet); opacity: 1; }
.step-card.done  { border-color: rgba(52,211,153,0.25); background: rgba(52,211,153,0.04); }
.step-card.done::before  { background: var(--emerald); opacity: 1; }

.step-inner { display: flex; align-items: center; gap: 0.75rem; }
.step-num {
    font-family: 'Fira Code', monospace;
    font-size: 0.62rem; font-weight: 500;
    color: var(--text-muted); letter-spacing: 0.1em; min-width: 24px;
}
.step-card.active .step-num { color: var(--violet); }
.step-card.done .step-num   { color: var(--emerald); }

.step-title {
    font-family: 'Epilogue', sans-serif;
    font-size: 0.9rem; font-weight: 600;
    color: #b0bfe0; flex: 1;
}
.step-card.active .step-title { color: #e2eaff; }
.step-card.done .step-title   { color: #90b0a0; }

.step-desc {
    font-size: 0.74rem; color: var(--text-muted);
    margin-top: 0.35rem; padding-left: 2.25rem; font-weight: 300;
}

.step-status {
    font-family: 'Fira Code', monospace;
    font-size: 0.6rem; letter-spacing: 0.1em;
    padding: 0.18rem 0.5rem; border-radius: 4px;
}
.s-wait { color: var(--text-muted); }
.s-run  { color: var(--violet); background: var(--violet-dim); animation: flicker 1.4s infinite; }
.s-done { color: var(--emerald); background: rgba(52,211,153,0.08); }

@keyframes flicker { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* ── STATUS BAR ── */
.status-bar {
    display: flex; align-items: center; gap: 0.7rem;
    background: var(--bg2);
    border: 1px solid var(--border2);
    border-left: 3px solid var(--violet);
    border-radius: 0 8px 8px 0;
    padding: 0.65rem 1.1rem;
    font-family: 'Fira Code', monospace;
    font-size: 0.72rem; color: var(--violet);
    margin: 1rem 0;
}
.status-bar.done { border-left-color: var(--emerald); color: var(--emerald); }
.pulse {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--violet); flex-shrink: 0;
    animation: pulse 1.1s infinite;
}
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:0.2;transform:scale(0.6)} }

/* ── RESULTS ── */
.results-heading {
    font-family: 'Epilogue', sans-serif;
    font-size: 1.25rem; font-weight: 700;
    letter-spacing: -0.02em; color: #e2eaff;
    margin: 2.5rem 0 1.25rem;
}

.raw-content {
    font-size: 0.84rem; line-height: 1.8;
    color: #7a8db0; white-space: pre-wrap;
    font-family: 'Epilogue', sans-serif; font-weight: 300;
    padding: 1.2rem;
    max-height: 280px; overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: var(--border2) transparent;
}

details summary {
    font-family: 'Fira Code', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    color: var(--text-dim) !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
}

/* Report shell */
.report-shell {
    background: var(--bg2);
    border: 1px solid var(--border2);
    border-radius: 14px;
    padding: 2rem 2.4rem;
    margin-bottom: 0.5rem;
    position: relative; overflow: hidden;
}
.report-shell::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--gold), #f97316, transparent);
}
.panel-label {
    font-family: 'Fira Code', monospace;
    font-size: 0.65rem; letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 1.2rem; padding-bottom: 0.8rem;
    display: flex; align-items: center; gap: 0.5rem;
}
.panel-label.gold {
    color: var(--gold);
    border-bottom: 1px solid rgba(251,191,36,0.15);
}
.panel-label.red {
    color: var(--crimson);
    border-bottom: 1px solid var(--crimson-glow);
}

/* Critic shell */
.critic-shell {
    background: var(--bg2);
    border: 1px solid var(--border2);
    border-radius: 14px;
    padding: 2rem 2.4rem;
    position: relative; overflow: hidden;
}
.critic-shell::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, var(--crimson), #fb7185, transparent);
}

/* Download btn */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid var(--border2) !important;
    color: var(--text-dim) !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    border-radius: 7px !important;
    padding: 0.5rem 1.2rem !important;
    margin-top: 1rem !important;
    transition: border-color 0.2s, color 0.2s !important;
}
.stDownloadButton > button:hover {
    border-color: var(--violet) !important;
    color: var(--violet) !important;
}

/* Misc */
.stAlert { background: var(--bg2) !important; border-color: var(--border2) !important; }
.stSpinner > div { border-top-color: var(--violet) !important; }

.site-footer {
    margin-top: 4rem; padding-top: 1.5rem;
    border-top: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between;
}
.footer-txt {
    font-family: 'Fira Code', monospace;
    font-size: 0.6rem; color: var(--text-muted);
    letter-spacing: 0.1em; text-transform: uppercase;
}

[data-testid="column"] { padding: 0 0.5rem !important; }
[data-testid="column"]:first-child { padding-left: 0 !important; }
[data-testid="column"]:last-child  { padding-right: 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── Step card helper ──────────────────────────────────────────────────────────
def step_card(num, title, desc, state):
    status_map = {
        "waiting": ("IDLE",    "s-wait", ""),
        "running": ("RUNNING", "s-run",  "active"),
        "done":    ("✓ DONE",  "s-done", "done"),
    }
    label, scls, ccls = status_map.get(state, ("", "", ""))
    st.markdown(f"""
    <div class="step-card {ccls}">
      <div class="step-inner">
        <span class="step-num">{num}</span>
        <span class="step-title">{title}</span>
        <span class="step-status {scls}">{label}</span>
      </div>
      <div class="step-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Session state init ────────────────────────────────────────────────────────
for k, v in [("results", {}), ("running", False), ("done", False)]:
    if k not in st.session_state:
        st.session_state[k] = v


# ── Topbar ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
  <div class="brand">
    <span class="brand-hex">⬡</span>
    <span class="brand-name">Synthetix<span class="brand-dot">.</span></span>
  </div>
  <span class="topbar-tag">Deep Research Engine</span>
</div>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-kicker">Multi-Agent AI System</div>
  <h1>Research at<br><em>machine speed.</em></h1>
  <p class="hero-desc">
    Four specialized agents collaborate — searching, scraping, writing, and critiquing —
    to deliver a polished research report in seconds.
  </p>
</div>
<div class="glow-divider"></div>
""", unsafe_allow_html=True)


# ── Two-column layout ─────────────────────────────────────────────────────────
col_left, col_gap, col_right = st.columns([5, 0.4, 4])

with col_left:
    st.markdown('<div class="input-shell"><div class="input-shell-label">Research Topic</div>', unsafe_allow_html=True)
    topic = st.text_input(
        "topic",
        placeholder="e.g. CRISPR gene editing breakthroughs 2025…",
        key="topic_input",
        label_visibility="collapsed",
    )
    run_btn = st.button("⬡  Run Synthetix Pipeline", use_container_width=True)
    st.markdown("""
    <div class="chips-row">
      <span class="chips-label">Try →</span>
      <span class="chip">LLM agents 2025</span>
      <span class="chip">Fusion energy</span>
      <span class="chip">Mars colonization</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="pipeline-heading">⬡ Pipeline Status</div>', unsafe_allow_html=True)

    r = st.session_state.results

    def get_state(step):
        steps = ["search", "reader", "writer", "critic"]
        if step in r:
            return "done"
        if st.session_state.running:
            for k in steps:
                if k not in r:
                    return "running" if k == step else "waiting"
        return "waiting"

    step_card("01", "Search Agent",  "Gathers recent web information",        get_state("search"))
    step_card("02", "Reader Agent",  "Scrapes & extracts primary content",    get_state("reader"))
    step_card("03", "Writer Chain",  "Drafts the full structured report",     get_state("writer"))
    step_card("04", "Critic Chain",  "Reviews, scores and flags weak areas",  get_state("critic"))


# ── Trigger run ───────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("Please enter a research topic.")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.rerun()


# ── Pipeline execution ────────────────────────────────────────────────────────
if st.session_state.running and not st.session_state.done:
    results = {}
    topic_val = st.session_state.topic_input

    st.markdown('<div class="status-bar"><span class="pulse"></span>Pipeline running — this may take a moment…</div>',
                unsafe_allow_html=True)

    with st.spinner(""):
        # Step 1 — Search
        sa = build_search_agent()
        sr = sa.invoke({"messages": [("user", f"Find recent, reliable and detailed information about: {topic_val}")]})
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

        # Step 2 — Reader
        ra = build_reader_agent()
        rr = ra.invoke({"messages": [("user",
            f"Based on the following search results about '{topic_val}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{results['search'][:800]}")]})
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

        # Step 3 — Writer
        combined = f"SEARCH RESULTS:\n{results['search']}\n\nDETAILED SCRAPED CONTENT:\n{results['reader']}"
        results["writer"] = writer_chain.invoke({"topic": topic_val, "research": combined})
        st.session_state.results = dict(results)

        # Step 4 — Critic
        results["critic"] = critic_chain.invoke({"report": results["writer"]})
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()


# ── Results display ───────────────────────────────────────────────────────────
r = st.session_state.results

if r:
    st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="results-heading">Output</div>', unsafe_allow_html=True)

    if st.session_state.done:
        st.markdown(
            '<div class="status-bar done">✓ &nbsp;All agents complete — report ready</div>',
            unsafe_allow_html=True,
        )

    # Raw collapsible outputs
    if "search" in r:
        with st.expander("▸ Search Agent · Raw Output"):
            st.markdown(f'<div class="raw-content">{r["search"]}</div>', unsafe_allow_html=True)

    if "reader" in r:
        with st.expander("▸ Reader Agent · Scraped Content"):
            st.markdown(f'<div class="raw-content">{r["reader"]}</div>', unsafe_allow_html=True)

    # Final report
    if "writer" in r:
        st.markdown("""
        <div class="report-shell">
          <div class="panel-label gold">⬡ Final Research Report</div>
        """, unsafe_allow_html=True)
        st.markdown(r["writer"])
        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button(
            label="⬇  Download Report (.md)",
            data=r["writer"],
            file_name=f"synthetix_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    # Critic
    if "critic" in r:
        st.markdown("""
        <div class="critic-shell">
          <div class="panel-label red">⬡ Critic Review</div>
        """, unsafe_allow_html=True)
        st.markdown(r["critic"])
        st.markdown("</div>", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="site-footer">
  <span class="footer-txt">⬡ Synthetix · Deep Research Engine</span>
  <span class="footer-txt">Search → Scrape → Write → Critique</span>
</div>
""", unsafe_allow_html=True)