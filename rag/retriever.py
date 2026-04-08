from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from scraper.config import CHROMA_DB_PATH, EMBEDDING_MODEL

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

vectorstore = Chroma(
    collection_name="legalfaq",
    embedding_function=embeddings,
    persist_directory=CHROMA_DB_PATH
)


def retrieve(query: str) -> list[dict]:
    results = vectorstore.similarity_search(query, k=5)

    final_results = []
    for r in results:
        item ={
            "text": r.page_content,
            "url": r.metadata.get("url"),
            "title": r.metadata.get("title")
        }
        final_results.append(item)
    return final_results