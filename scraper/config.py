CITIZEN_INFORMATION_URL = "https://www.citizensinformation.ie/en/"
REVENUE_URL = "https://www.revenue.ie"
GOV_URL = "https://www.gov.ie"

#DB PATH
CHROMA_DB_PATH = "../data/chroma_db"

# MODEL
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CATEGORIES = [
    f"{CITIZEN_INFORMATION_URL}moving-country/ukrainian-refugees-in-ireland/",
    f"{CITIZEN_INFORMATION_URL}moving-country/irish-citizenship/",
    f"{CITIZEN_INFORMATION_URL}moving-country/visas-for-ireland/",
    f"{CITIZEN_INFORMATION_URL}social-welfare/social-welfare-payments-and-work/",
    f"{CITIZEN_INFORMATION_URL}social-welfare/extra-social-welfare-benefits/",


]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xhtml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

GROQ_MODEL = "llama-3.3-70b-versatile"