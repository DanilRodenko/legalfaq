import os
from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

# Импортируем нашу функцию поиска и константы
from rag.retriever import retrieve
# Предполагаем, что ты создал этот файл для констант
from scraper.config import GROQ_MODEL

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
app = FastAPI()


class QuestionRequest(BaseModel):
    text: str


@app.post("/ask")
async def ask(question: QuestionRequest):
    chunks = retrieve(question.text)

    context_list = []
    sources = []

    for doc in chunks:
        context_list.append(doc["text"])
        sources.append({
            "title": doc.get("title", "No Title"),
            "url": doc.get("url", "#")
        })

    context = "\n\n".join(context_list)

    PROMPT = f"""
    You are a professional Immigration and Legal Assistant specializing in Irish law. Your primary role is to help immigrants navigate the Irish system using verified information from Citizens Information (citizensinformation.ie).

    CORE OPERATING GUIDELINES:
    1. DATA INTEGRITY: Answer ONLY using the information provided in the "CONTEXT" section below.
    2. NO DATA POLICY: If the context does not contain the answer, state that you don't have this information.
    3. MULTILINGUAL SUPPORT: Respond in the same language the user used (English, Russian, or Ukrainian).
    4. LEGAL DISCLAIMER: Include a brief disclaimer that this is not official legal advice.
    5. FORMATTING: Use headings and bullet points.

    CONTEXT FROM KNOWLEDGE BASE:
    {context}

    QUESTION: {question.text}

    ANSWER:
    """

    chat_completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": PROMPT}],
        temperature=0.2  # Низкая температура для точности
    )

    answer = chat_completion.choices[0].message.content

    return {
        "answer": answer,
        "sources": sources
    }