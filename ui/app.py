import os

import httpx
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000/ask")

st.set_page_config(
    page_title="LegalFaq For Ukranian refugees in Ireland",
    layout="wide"
)

st.title("🇮🇪 LegalFAQ — Irish Immigration Assistant")
st.markdown("Ask questions about visas, housing, social welfare, and more. Powered by Citizens Information.")

query = st.text_input("Your question")
if st.button("Ask"):
    if query:
        response = httpx.post(API_URL, json={"text": query})
        data = response.json()
        answer = data.get("answer", "No answer received.")
        sources = data.get("sources", [])

        source_links = "\n".join(
            [f"📍 [{s['title']}]({s['url']})" for s in sources if s['url'] != "#"]
        )

        full_response = f"{answer}\n\n*Sources:*\n{source_links}" if source_links else answer
        st.markdown(full_response)