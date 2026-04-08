from bs4 import BeautifulSoup
import httpx
from urllib.parse import urljoin
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from config import CHROMA_DB_PATH, EMBEDDING_MODEL, CATEGORIES, HEADERS

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

vectorstore = Chroma(
    collection_name="legalfaq",
    embedding_function=embeddings,
    persist_directory=CHROMA_DB_PATH
)


def get_article_links(url_category: str) -> list[str]:
    base_url = "/".join(url_category.split("/")[:3])
    response = httpx.get(url_category, headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.select("ul.categoryitems.sectionitems a")
        return list(set(
            urljoin(base_url, a.get("href"))
            for a in links if a.get("href")
        ))

    return []


def scrape_article(url: str) -> dict:
    response = httpx.get(url, headers=HEADERS)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        titles = soup.select("h1")
        sections = soup.select("section.block-richtext")
        title = titles[0].get_text(strip=True) if titles else "No Title"
        full_text = " ".join(s.get_text(separator=" ", strip=True) for s in sections)
        return {"title": title, "text": full_text, "url": url}

    return {"title": "Error", "text": "", "url": url}


def chunk_text(text: str):
    chunk_size = 200
    overlap = 30
    words = text.split()
    for i in range(0, len(words), chunk_size - overlap):
        yield " ".join(words[i: i + chunk_size])


def save_to_chroma(article: dict):
    texts_to_add = []
    metadatas_to_add = []
    for chunk in chunk_text(article["text"]):
        texts_to_add.append(chunk)
        metadatas_to_add.append({"url": article["url"], "title": article["title"]})
    if texts_to_add:
        vectorstore.add_texts(texts=texts_to_add, metadatas=metadatas_to_add)


def run_scraper():
    for cat in CATEGORIES:
        links = get_article_links(cat)
        print(f"Found {len(links)} links in {cat}")
        for url in links:
            article = scrape_article(url)
            print(f"Scraped: {article['title']}")
            save_to_chroma(article)


if __name__ == "__main__":
    run_scraper()
    # print(vectorstore._collection.count())
    # results = vectorstore.similarity_search("accommodation recognition payment", k=3)
    # for r in results:
    #     print(r.metadata["title"])
    #     print(r.page_content[:200])
    #     print("---")