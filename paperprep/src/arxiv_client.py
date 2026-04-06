"""
Client for fetching paper metadata from the arXiv API.
"""

import re
import requests
import xml.etree.ElementTree as ET


ARXIV_API_URL = "http://export.arxiv.org/api/query"
ARXIV_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}


def fetch_paper(arxiv_url: str) -> dict:
    """
    Fetch metadata for an arXiv paper.

    Accepts a full arXiv URL (abs or pdf) or a bare paper ID.

    Returns a dict with keys: title, authors, abstract, published, arxiv_id, url.
    Raises ValueError if the input is invalid or the paper cannot be found.
    """
    paper_id = _extract_paper_id(arxiv_url)

    response = requests.get(ARXIV_API_URL, params={"id_list": paper_id}, timeout=10)
    response.raise_for_status()

    return _parse_response(response.text, paper_id)


def _extract_paper_id(arxiv_url: str) -> str:
    """Extract the arXiv paper ID from a URL or bare ID string."""
    # Match versioned or unversioned IDs in URLs or standalone
    match = re.search(r"(\d{4}\.\d{4,5}(?:v\d+)?)", arxiv_url)
    if not match:
        raise ValueError(
            f"Could not extract a valid arXiv ID from: {arxiv_url!r}\n"
            "Expected formats: 'https://arxiv.org/abs/2301.07041', "
            "'https://arxiv.org/pdf/2301.07041', or just '2301.07041'."
        )
    return match.group(1)


def _parse_response(xml_text: str, paper_id: str) -> dict:
    """Parse the arXiv API XML response and return a metadata dict."""
    root = ET.fromstring(xml_text)

    entry = root.find("atom:entry", ARXIV_NS)
    if entry is None:
        raise ValueError(f"No paper found for arXiv ID: {paper_id!r}")

    title = _get_text(entry, "atom:title")
    abstract = _get_text(entry, "atom:summary")
    published = _get_text(entry, "atom:published")

    authors = [
        _get_text(author, "atom:name")
        for author in entry.findall("atom:author", ARXIV_NS)
    ]

    # Prefer the abs URL from the feed over reconstructing it
    url = None
    for link in entry.findall("atom:link", ARXIV_NS):
        if link.attrib.get("rel") == "alternate":
            url = link.attrib.get("href")
            break
    if url is None:
        url = f"https://arxiv.org/abs/{paper_id}"

    arxiv_id = _get_text(entry, "arxiv:id", ARXIV_NS) or paper_id

    return {
        "title": title.strip() if title else None,
        "authors": authors,
        "abstract": abstract.strip() if abstract else None,
        "published": published,
        "arxiv_id": arxiv_id,
        "url": url,
    }


def _get_text(element: ET.Element, tag: str, ns: dict = ARXIV_NS) -> str | None:
    """Return the text content of a child element, or None if missing."""
    child = element.find(tag, ns)
    return child.text if child is not None else None
