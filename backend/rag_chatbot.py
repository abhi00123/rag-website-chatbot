import numpy as np
from sentence_transformers import SentenceTransformer
import ollama

model = SentenceTransformer("all-MiniLM-L6-v2")

def ask_question(question, index, chunks, top_k=5):
    # Embed the question
    question_embedding = model.encode([question])

    # Search FAISS
    distances, indices = index.search(np.array(question_embedding), top_k)
    retrieved_chunks = [chunks[i] for i in indices[0]]

    context = "\n".join(retrieved_chunks)

    prompt = f"""
    You are a helpful assistant.
    Answer the question using the context below.
    Even if the information is brief, summarize it clearly.
    Do NOT add outside knowledge.

    Context:
    {context}

    Question:
    {question}
    """


    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response["message"]["content"]
