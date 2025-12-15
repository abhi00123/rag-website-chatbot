import os
import requests
import numpy as np
import streamlit as st
from sentence_transformers import SentenceTransformer

API_KEY = st.secrets["OPENROUTER_API_KEY"]
MODEL = "openai/gpt-4o-mini"

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def ask_question(question, index, chunks, top_k=10):
    q_embedding = embedder.encode([question])
    _, indices = index.search(np.array(q_embedding), top_k)

    context_chunks = [chunks[i] for i in indices[0] if i < len(chunks)]
    context = "\n".join(context_chunks)

    if not context.strip():
        return "I do not have enough information to answer this question."

    prompt = f"""
Answer the question using only the website content below.
Summarize clearly and concisely.
Do not use outside knowledge.

Website Content:
{context}

Question:
{question}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        },
        timeout=30
    )

    response.raise_for_status()

    return response.json()["choices"][0]["message"]["content"]
