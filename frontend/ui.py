"""
Multi-Agent AI Research System - Frontend (Gen Z Edition)
==========================================================
Streamlit UI that streams the 4-agent pipeline in real-time:
  Topic → Research → Draft → Fact-Check → Final Article
"""

import re
import sys
from pathlib import Path

import streamlit as st

# ── Path setup (allows importing backend from frontend/) 
sys.path.insert(0, str(Path(__file__).parent.parent / "backend" / "src"))
from main import stream_pipeline  # noqa: E402  (must come after sys.path)

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Research System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800&family=Inter:wght@400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp {
        background: linear-gradient(160deg, #1a1a1a 0%, #242424 40%, #1e1e1e 100%);
        min-height: 100vh;
    }

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #1a1a1a; }
    ::-webkit-scrollbar-thumb { background: linear-gradient(#a855f7, #06b6d4); border-radius: 6px; }

    /* ── Hero ── */
    .hero { text-align: center; padding: 2.5rem 1rem 1rem 1rem; }
    .hero-badge {
        display: inline-block;
        background: linear-gradient(90deg, #a855f7, #06b6d4);
        color: #fff; font-size: 0.72rem; font-weight: 700;
        letter-spacing: 0.18em; text-transform: uppercase;
        padding: 0.3rem 1rem; border-radius: 999px; margin-bottom: 1rem;
    }
    .hero h1 {
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(2rem, 5vw, 3.2rem); font-weight: 800;
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 40%, #06b6d4 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; line-height: 1.15; margin: 0 0 0.75rem 0;
    }
    .hero p { color: #94a3b8; font-size: 1.05rem; max-width: 580px; margin: 0 auto; line-height: 1.6; }

    /* ── Glow divider ── */
    .glow-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #a855f7, #06b6d4, transparent);
        border: none; margin: 1.5rem 0; opacity: 0.5;
    }

    /* ── Section labels ── */
    .section-heading {
        font-family: 'Space Grotesk', sans-serif; font-size: 0.78rem; font-weight: 700;
        letter-spacing: 0.16em; text-transform: uppercase; color: #64748b;
        margin: 1.6rem 0 0.8rem 0;
    }

    /* ── Input override ── */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.06) !important;
        border: 1.5px solid rgba(168,85,247,0.35) !important;
        border-radius: 14px !important; color: #181818 !important;
        font-size: 1rem !important; padding: 0.75rem 1rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #a855f7 !important;
        box-shadow: 0 0 0 3px rgba(168,85,247,0.2) !important;
    }
    .stTextInput > div > div > input::placeholder { color: #475569 !important; }

    /* ── Primary button ── */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #a855f7, #ec4899) !important;
        border: none !important; border-radius: 14px !important;
        color: #fff !important; font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.95rem !important; font-weight: 700 !important;
        padding: 0.75rem 1.5rem !important;
        box-shadow: 0 4px 20px rgba(168,85,247,0.35) !important;
        transition: transform 0.15s, box-shadow 0.15s !important;
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(168,85,247,0.5) !important;
    }

    /* ── Pipeline step cards ── */
    .step-card {
        display: flex; align-items: center; gap: 0.75rem;
        border-radius: 14px; padding: 0.8rem 1.1rem; margin-bottom: 0.55rem;
        background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
        color: #475569; font-size: 0.92rem; font-weight: 500;
    }
    .step-dot { width: 10px; height: 10px; border-radius: 50%; background: #334155; flex-shrink: 0; }
    .step-card.active {
        background: rgba(234,179,8,0.08); border-color: rgba(234,179,8,0.4);
        color: #fde047; box-shadow: 0 0 16px rgba(234,179,8,0.15);
    }
    .step-card.active .step-dot {
        background: #fde047; box-shadow: 0 0 8px #fde04780;
        animation: pulse-dot 1s infinite;
    }
    .step-card.done {
        background: rgba(34,197,94,0.08); border-color: rgba(34,197,94,0.35);
        color: #4ade80; box-shadow: 0 0 12px rgba(34,197,94,0.1);
    }
    .step-card.done .step-dot { background: #4ade80; box-shadow: 0 0 8px #4ade8080; }
    @keyframes pulse-dot {
        0%, 100% { transform: scale(1); opacity: 1; }
        50%       { transform: scale(1.5); opacity: 0.6; }
    }

    /* ── Expanders ── */
    .stExpander {
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important; margin-bottom: 0.6rem !important;
    }
    .stExpander summary { font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important; color: #cbd5e1 !important; }
    .stExpander summary:hover { color: #a855f7 !important; }

    /* ── Final article card ── */
    .final-card-wrapper {
        background: linear-gradient(135deg, rgba(168,85,247,0.12), rgba(6,182,212,0.08));
        border: 1px solid rgba(168,85,247,0.3); border-radius: 24px;
        padding: 2rem 2.5rem; margin-top: 1rem;
        box-shadow: 0 8px 48px rgba(168,85,247,0.15);
    }
    .final-badge {
        display: inline-block;
        background: linear-gradient(90deg, #a855f7, #06b6d4);
        color: #fff !important; font-family: 'Space Grotesk', sans-serif;
        font-size: 0.72rem; font-weight: 700; letter-spacing: 0.14em;
        text-transform: uppercase; padding: 0.3rem 0.9rem; border-radius: 999px;
        margin-bottom: 0.8rem;
    }
    .final-card-title {
        font-family: 'Space Grotesk', sans-serif; font-size: 1.5rem; font-weight: 800;
        background: linear-gradient(90deg, #a855f7, #06b6d4);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text; margin: 0 0 0.5rem 0;
    }
    .final-article-body { color: #e2e8f0 !important; font-size: 1.02rem; line-height: 1.85; }
    .final-article-body h1,
    .final-article-body h2,
    .final-article-body h3 {
        color: #f8fafc !important; font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 700 !important; margin-top: 1.4rem;
    }
    .final-article-body p      { color: #e2e8f0 !important; margin-bottom: 0.9rem; }
    .final-article-body li     { color: #cbd5e1 !important; margin-bottom: 0.35rem; }
    .final-article-body strong { color: #f1f5f9 !important; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: rgba(20,20,20,0.98) !important;
        border-right: 1px solid rgba(255,255,255,0.08) !important;
    }
    [data-testid="stSidebar"] * { color: #94a3b8; }
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #e2e8f0 !important; }

    .wf-chip {
        display: flex; align-items: flex-start; gap: 0.6rem;
        background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.07);
        border-radius: 12px; padding: 0.65rem 0.85rem; margin-bottom: 0.45rem;
        font-size: 0.88rem; color: #94a3b8;
    }
    .wf-chip-label { font-weight: 600; color: #cbd5e1; }

    .tech-pill {
        display: inline-block; background: rgba(168,85,247,0.12);
        border: 1px solid rgba(168,85,247,0.25); color: #c084fc !important;
        font-size: 0.78rem; font-weight: 600; padding: 0.25rem 0.7rem;
        border-radius: 999px; margin: 0.2rem 0.15rem;
    }

    /* ── Empty state ── */
    .empty-state { text-align: center; padding: 4rem 2rem; }
    .empty-state .big-icon { font-size: 4rem; margin-bottom: 1rem; }
    .empty-state h3 {
        font-family: 'Space Grotesk', sans-serif; font-size: 1.4rem;
        font-weight: 700; color: #475569; margin-bottom: 0.5rem;
    }
    .empty-state p { color: #334155; font-size: 0.95rem; }

    /* ── Progress bar ── */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #a855f7, #06b6d4) !important;
        border-radius: 999px !important;
    }
    .stProgress > div > div {
        background: rgba(255,255,255,0.06) !important; border-radius: 999px !important;
    }

    .stAlert { border-radius: 14px !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<div style="text-align:center;padding:1.2rem 0 0.8rem 0;">'
        '<span style="font-size:2.8rem;">🤖</span>'
        '<p style="font-family:Space Grotesk,sans-serif;font-size:1.1rem;font-weight:700;'
        'color:#e2e8f0;margin:0.4rem 0 0 0;">AI Research System</p>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

    st.markdown(
        '<p style="font-family:Space Grotesk,sans-serif;font-size:0.72rem;font-weight:700;'
        'letter-spacing:0.15em;text-transform:uppercase;color:#475569;margin-bottom:0.6rem;">'
        'Pipeline</p>',
        unsafe_allow_html=True,
    )
    for icon, label, desc in [
        ("🔍", "Research Agent",    "Gathers facts & insights"),
        ("✍️",  "Writer Agent",      "Drafts the full article"),
        ("✅", "Fact-Checker Agent", "Verifies every claim"),
        ("📝", "Reviewer Agent",     "Polishes to perfection"),
    ]:
        st.markdown(
            f'<div class="wf-chip">'
            f'<span style="font-size:1.1rem;flex-shrink:0;">{icon}</span>'
            f'<div><span class="wf-chip-label">{label}</span>'
            f'<br><span style="font-size:0.8rem;">{desc}</span></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
    st.markdown(
        '<p style="font-family:Space Grotesk,sans-serif;font-size:0.72rem;font-weight:700;'
        'letter-spacing:0.15em;text-transform:uppercase;color:#475569;margin-bottom:0.5rem;">'
        'Built With</p>',
        unsafe_allow_html=True,
    )
    for pill in ["LangGraph", "GPT-4o-mini", "Streamlit", "LangChain"]:
        st.markdown(f'<span class="tech-pill">⚡ {pill}</span>', unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="hero">
      <div class="hero-badge">✦ Powered by Multi-Agent AI ✦</div>
      <h1>Research. Write.<br>Verify. Publish.</h1>
      <p>Drop a topic. Four specialized AI agents collaborate in real-time to deliver a publication-ready article — automatically.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1], vertical_alignment="bottom")
with col_input:
    topic = st.text_input(
        "topic",
        placeholder="e.g.  How AI is reshaping creative industries in 2025",
        label_visibility="collapsed",
    )
with col_btn:
    run_btn = st.button("🚀 Run", use_container_width=True, type="primary")

st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

# ── Pipeline constants ────────────────────────────────────────────────────────
STEPS = [
    ("research",     "🔍", "Research Agent",      "Gathering deep research notes…"),
    ("writer",       "✍️",  "Writer Agent",         "Drafting a structured article…"),
    ("fact_checker", "✅", "Fact-Checker Agent",   "Cross-referencing every claim…"),
    ("reviewer",     "📝", "Reviewer Agent",       "Polishing to publication quality…"),
]
STEP_KEYS = [s[0] for s in STEPS]

# ── Session state ─────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = {}
if "finished" not in st.session_state:
    st.session_state.finished = False


# ── Helper: render final article card ────────────────────────────────────────
def render_final_article(text: str) -> None:
    lines = text.split("\n")
    html_lines = []
    for line in lines:
        if line.startswith("### "):
            html_lines.append(f"<h3>{line[4:]}</h3>")
        elif line.startswith("## "):
            html_lines.append(f"<h2>{line[3:]}</h2>")
        elif line.startswith("# "):
            html_lines.append(f"<h1>{line[2:]}</h1>")
        elif line.startswith("- ") or line.startswith("* "):
            html_lines.append(f"<li>{line[2:]}</li>")
        elif line.strip() == "":
            html_lines.append("<br>")
        else:
            converted = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", line)
            html_lines.append(f"<p>{converted}</p>")

    body_html = "\n".join(html_lines)
    st.markdown(
        f"""
        <div class="final-card-wrapper">
          <div><span class="final-badge">✦ Final Article</span></div>
          <p class="final-card-title">🏆 Publication-Ready Article</p>
          <hr style="border:none;border-top:1px solid rgba(168,85,247,0.25);margin:0.8rem 0 1.2rem 0;">
          <div class="final-article-body">{body_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("⚠️ Please enter a topic before running.")
        st.stop()

    st.session_state.results = {}
    st.session_state.finished = False

    st.markdown('<p class="section-heading">⚡ Live Pipeline Progress</p>', unsafe_allow_html=True)
    progress_bar = st.progress(0, text="Initialising agents…")

    step_placeholders = {}
    for node, icon, label, _ in STEPS:
        step_placeholders[node] = st.empty()
        step_placeholders[node].markdown(
            f'<div class="step-card">'
            f'<span class="step-dot"></span>'
            f'{icon} <strong>{label}</strong> — waiting…'
            f'</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)

    st.markdown('<p class="section-heading">📋 Agent Outputs</p>', unsafe_allow_html=True)
    result_containers = {
        "research":     st.expander("🔍  Research Notes",    expanded=False),
        "writer":       st.expander("✍️   Draft Article",     expanded=False),
        "fact_checker": st.expander("✅  Fact-Check Report", expanded=False),
    }
    st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
    final_placeholder = st.empty()

    completed = 0
    try:
        for node_name, node_state in stream_pipeline(topic):
            if node_name not in STEP_KEYS:
                continue

            completed += 1
            idx = STEP_KEYS.index(node_name)
            _, icon, label, _ = STEPS[idx]

            # Mark done
            step_placeholders[node_name].markdown(
                f'<div class="step-card done">'
                f'<span class="step-dot"></span>'
                f'✅ {icon} <strong>{label}</strong> — done!'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Mark next active
            if idx + 1 < len(STEPS):
                nn, ni, nl, nd = STEPS[idx + 1]
                step_placeholders[nn].markdown(
                    f'<div class="step-card active">'
                    f'<span class="step-dot"></span>'
                    f'🔄 {ni} <strong>{nl}</strong> — {nd}'
                    f'</div>',
                    unsafe_allow_html=True,
                )

            pct = int((completed / len(STEPS)) * 100)
            progress_bar.progress(pct, text=f"Agent {completed}/{len(STEPS)} complete…")

            st.session_state.results[node_name] = node_state

            if node_name == "research" and "research_notes" in node_state:
                with result_containers["research"]:
                    st.markdown(node_state["research_notes"])

            elif node_name == "writer" and "draft" in node_state:
                with result_containers["writer"]:
                    st.markdown(node_state["draft"])

            elif node_name == "fact_checker" and "fact_check_report" in node_state:
                with result_containers["fact_checker"]:
                    st.markdown(node_state["fact_check_report"])

            elif node_name == "reviewer" and "final_article" in node_state:
                with final_placeholder.container():
                    render_final_article(node_state["final_article"])

        progress_bar.progress(100, text="✅ All four agents completed!")
        st.session_state.finished = True
        st.success("🎉 Done! Scroll down to read your article.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
        st.stop()

# ── Persisted results ─────────────────────────────────────────────────────────
elif st.session_state.finished and st.session_state.results:
    results = st.session_state.results

    st.markdown('<p class="section-heading">📋 Agent Outputs — Last Run</p>', unsafe_allow_html=True)

    with st.expander("🔍  Research Notes", expanded=False):
        if "research" in results and "research_notes" in results["research"]:
            st.markdown(results["research"]["research_notes"])

    with st.expander("✍️   Draft Article", expanded=False):
        if "writer" in results and "draft" in results["writer"]:
            st.markdown(results["writer"]["draft"])

    with st.expander("✅  Fact-Check Report", expanded=False):
        if "fact_checker" in results and "fact_check_report" in results["fact_checker"]:
            st.markdown(results["fact_checker"]["fact_check_report"])

    if "reviewer" in results and "final_article" in results["reviewer"]:
        st.markdown('<hr class="glow-divider">', unsafe_allow_html=True)
        render_final_article(results["reviewer"]["final_article"])

# ── Empty state ───────────────────────────────────────────────────────────────
else:
    st.markdown(
        """
        <div class="empty-state">
          <div class="big-icon">✨</div>
          <h3>Your article starts here</h3>
          <p>Enter any topic above and hit <strong style="color:#a855f7;">Run</strong><br>
          to watch four AI agents collaborate live.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
