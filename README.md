# PaperPrep

![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-ff4b4b)

**Understand any arXiv paper before you read it.**

PaperPrep is a Streamlit web app that takes any arXiv paper URL and uses the Claude API to instantly generate a plain-English summary, a difficulty score, and a list of prerequisite concepts — so you can quickly decide whether a paper is worth your time and know exactly what background knowledge you'll need before diving in.

---

## Screenshot

> _Screenshot coming soon — deploy the app and add one here._

---

## How It Works

1. **Fetch** — PaperPrep extracts the paper ID from any arXiv URL format and calls the arXiv API to retrieve the title, authors, and abstract.
2. **Analyze** — The paper metadata is sent to Claude (Haiku) with a structured prompt asking for a difficulty score, prerequisite concepts, and a plain-English summary.
3. **Display** — Results are rendered in a clean Streamlit UI: a difficulty badge, prerequisite pills, and a summary callout — all in seconds.

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | [Streamlit](https://streamlit.io) |
| AI | [Anthropic Claude API](https://www.anthropic.com) (`claude-haiku-4-5`) |
| Paper data | [arXiv API](https://arxiv.org/help/api) |
| Language | Python 3.10+ |

---

## Local Installation

### Prerequisites

- Python 3.10 or higher
- An [Anthropic API key](https://console.anthropic.com)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/ArmanSam17/paperprep.git
cd paperprep

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r paperprep/requirements.txt

# 4. Set up your API key
cp paperprep/.env.example paperprep/.env
```

Open `paperprep/.env` and replace `your_key_here` with your Anthropic API key:

```
ANTHROPIC_API_KEY=sk-ant-...
```

```bash
# 5. Run the app
cd paperprep
streamlit run app.py
```

The app will open at `http://localhost:8501`.

---

## Deploying to Streamlit Community Cloud

1. **Push this repo to GitHub** (must be public for the free Streamlit Cloud tier).

2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.

3. Click **New app** and select this repository and the `main` branch.

4. Set the **Main file path** to: `paperprep/app.py`

5. Click **Advanced settings** and add your API key in the **Secrets** box:

   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```

6. Click **Deploy**. Streamlit Cloud will install dependencies from `paperprep/requirements.txt` and launch the app automatically.

---

## Project Structure

```
paperprep/
├── app.py                  # Streamlit UI
├── src/
│   ├── arxiv_client.py     # Fetches paper metadata from the arXiv API
│   ├── claude_client.py    # Sends prompts to Claude and parses responses
│   └── prompt_builder.py   # Builds structured prompts for Claude
├── .env.example            # Environment variable template
├── requirements.txt        # Python dependencies
└── README.md
```

---

## License

This project is licensed under the [MIT License](LICENSE).
