import sys
import os

# Allow running from the paperprep/ directory: make `src` importable
sys.path.insert(0, os.path.dirname(__file__))

from dotenv import load_dotenv
import streamlit as st

from src.arxiv_client import fetch_paper
from src.claude_client import analyze_paper

load_dotenv()

# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="PaperPrep",
    page_icon="📖",
    layout="wide",
)

# ── Header ───────────────────────────────────────────────────────────────────

st.title("PaperPrep")
st.markdown("**Understand any arXiv paper before you read it**")
st.divider()

# ── Input ────────────────────────────────────────────────────────────────────

arxiv_url = st.text_input(
    "arXiv URL or paper ID",
    placeholder="e.g. https://arxiv.org/abs/2301.07041  or  2301.07041",
)
analyze_clicked = st.button("Analyze Paper", type="primary")

# ── Analysis ─────────────────────────────────────────────────────────────────

if analyze_clicked:
    if not arxiv_url.strip():
        st.error("Please enter an arXiv URL or paper ID before clicking Analyze.")
        st.stop()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        st.error(
            "ANTHROPIC_API_KEY is not set. "
            "Copy .env.example to .env and add your key."
        )
        st.stop()

    try:
        with st.spinner("Fetching paper from arXiv…"):
            paper = fetch_paper(arxiv_url)

        with st.spinner("Analyzing with Claude…"):
            analysis = analyze_paper(paper)

    except ValueError as exc:
        st.error(f"Could not fetch paper: {exc}")
        st.stop()
    except RuntimeError as exc:
        st.error(f"Analysis failed: {exc}")
        st.stop()
    except Exception as exc:
        st.error(f"Unexpected error: {exc}")
        st.stop()

    st.divider()

    # ── Section A: Paper info ─────────────────────────────────────────────────

    authors_str = ", ".join(paper["authors"]) if paper["authors"] else "Unknown"
    year = paper["published"][:4] if paper.get("published") else ""

    st.subheader(paper["title"] or "Untitled")
    st.markdown(
        f"**Authors:** {authors_str}"
        + (f"&nbsp;&nbsp;·&nbsp;&nbsp;**Published:** {year}" if year else "")
        + f"&nbsp;&nbsp;·&nbsp;&nbsp;[View on arXiv ↗]({paper['url']})"
    )

    st.divider()

    # ── Sections B, C, D in two columns ──────────────────────────────────────

    left, right = st.columns([1, 2], gap="large")

    with left:
        # ── Section B: Difficulty score ───────────────────────────────────────

        score = int(analysis["difficulty_score"])
        label = analysis["difficulty_label"]
        rationale = analysis["difficulty_rationale"]

        # Choose badge colour based on score
        if score <= 3:
            badge_colour = "#2e7d32"   # green
        elif score <= 6:
            badge_colour = "#f57c00"   # amber
        else:
            badge_colour = "#c62828"   # red

        st.markdown("#### Difficulty")
        st.markdown(
            f"<span style='font-size:2.4rem; font-weight:700;'>{score} / 10</span>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<span style='"
            f"background:{badge_colour}; color:#fff; "
            f"padding:3px 12px; border-radius:999px; font-size:0.85rem; font-weight:600;"
            f"'>{label}</span>",
            unsafe_allow_html=True,
        )
        st.markdown("")   # spacer
        st.caption(rationale)

        st.markdown("---")

        # ── Section C: Prerequisites ──────────────────────────────────────────

        st.markdown("#### Prerequisites")
        pills_html = " ".join(
            f"<span style='"
            f"display:inline-block; margin:3px 4px 3px 0; padding:4px 12px; "
            f"background:#e8eaf6; color:#1a237e; border-radius:999px; "
            f"font-size:0.82rem; font-weight:500;"
            f"'>{prereq}</span>"
            for prereq in analysis["prerequisites"]
        )
        st.markdown(pills_html, unsafe_allow_html=True)

    with right:
        # ── Section D: Plain-English summary ──────────────────────────────────

        st.markdown("#### Plain-English Summary")
        st.info(analysis["summary"])

    # ── Footer ────────────────────────────────────────────────────────────────

    st.divider()
    st.markdown(
        "<div style='text-align:center; color:#888; font-size:0.8rem;'>"
        "Built with Claude API + arXiv"
        "</div>",
        unsafe_allow_html=True,
    )
