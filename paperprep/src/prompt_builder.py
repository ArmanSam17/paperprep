"""
Builds structured prompts for Claude to analyze arXiv papers.
"""


def build_analysis_prompt(paper: dict) -> str:
    """
    Build a prompt instructing Claude to analyze an arXiv paper.

    Takes the dict returned by fetch_paper and returns a prompt string
    that instructs Claude to respond with a single valid JSON object.
    """
    authors = ", ".join(paper.get("authors", [])) or "Unknown"
    title = paper.get("title") or "Unknown"
    abstract = paper.get("abstract") or "No abstract available."

    return f"""You are an expert at evaluating academic papers and communicating complex research clearly.

Analyze the following arXiv paper and respond with ONLY a valid JSON object — no markdown, no code fences, no commentary before or after.

Paper title: {title}
Authors: {authors}
Abstract:
{abstract}

Return a JSON object with exactly these fields:

{{
  "difficulty_score": <integer from 1 to 10, where 1 = accessible to anyone with no background and 10 = requires deep PhD-level specialization>,
  "difficulty_label": <one of exactly: "Beginner", "Intermediate", "Advanced", "Expert">,
  "difficulty_rationale": <1–2 sentences explaining why this difficulty score was assigned>,
  "prerequisites": <a list of 4 to 7 strings, each naming a concept or topic the reader should already understand>,
  "summary": <a plain-English paragraph of 4–6 sentences explaining what this paper is about, written for a smart non-specialist with no assumed domain knowledge>
}}

Respond with ONLY the JSON object. Do not include any other text."""
