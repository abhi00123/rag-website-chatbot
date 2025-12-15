import os
import requests
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openai/gpt-4o-mini"

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def ask_question(question, index, chunks, top_k=10):
    q_embedding = embedder.encode([question])
    _, indices = index.search(np.array(q_embedding), top_k)

    context = "\n".join([chunks[i] for i in indices[0]])

    prompt = f"""
Answer the question using the website content below.
Summarize clearly.
Do not mention missing information unless context is empty.

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
        }
    )

    return response.json()["choices"][0]["message"]["content"]
