# LegalFAQ

AI-powered legal FAQ assistant for Ukrainian refugees and immigrants in Ireland.

## What it does

Users ask legal questions in English or Russian. The system retrieves relevant chunks from Irish legal sources (citizensinformation.ie) and generates answers using an LLM with source references.

## Architecture
```
Streamlit UI  ←→
                   FastAPI  →  RAG Pipeline  →  Groq LLM
Telegram Bot  ←→
```

## Tech Stack

- **LLM:** Groq (Llama 3.3 70B)
- **Embeddings:** sentence-transformers (all-MiniLM-L6-v2)
- **Vector DB:** ChromaDB
- **Scraping:** httpx + BeautifulSoup4
- **Scheduler:** APScheduler
- **Backend:** FastAPI
- **UI:** Streamlit
- **Bot:** python-telegram-bot
- **Deploy:** Docker + Docker Compose

## Project Structure
```
legalfaq/
├── scraper/        # Web scraping + ChromaDB indexing
├── rag/            # Retriever
├── api/            # FastAPI backend
├── bot/            # Telegram bot
├── ui/             # Streamlit app
└── data/           # ChromaDB storage (gitignored)
```

## Setup

1. Clone the repo
2. Create `.env` with `GROQ_API_KEY` and `TELEGRAM_BOT_TOKEN`
3. Install dependencies: `pip install -r requirements.txt`
4. Run scraper: `python scraper/scraper.py`
5. Start API: `uvicorn api.main:app --reload`
6. Start UI: `streamlit run ui/app.py`
7. Start bot: `python bot/telegram_bot.py`

## Data Sources

citizensinformation.ie — Irish legal information

## Disclaimer
This tool provides general legal information only and does not constitute legal advice.
