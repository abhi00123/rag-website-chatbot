from flask import Flask, request, jsonify
from flask_cors import CORS

from crawler import crawl_website
from selenium_crawler import crawl_with_selenium
from text_processor import chunk_text
from embeddings import create_faiss_index
from rag_chatbot import ask_question

app = Flask(__name__)
CORS(app)

# Global memory (simple)
INDEX = None
CHUNKS = None

@app.route("/build_kb", methods=["POST"])
def build_kb():
    global INDEX, CHUNKS

    data = request.json
    url = data.get("url")

    pages = crawl_website(url)
    all_text = " ".join(pages)

    if len(all_text.strip()) < 300:
        all_text = crawl_with_selenium(url)

    chunks = chunk_text(all_text)
    index, _ = create_faiss_index(chunks)

    if index is None:
        return jsonify({"status": "error", "message": "No content found"})

    INDEX = index
    CHUNKS = chunks

    return jsonify({"status": "success"})

@app.route("/ask", methods=["POST"])
def ask():
    global INDEX, CHUNKS

    if INDEX is None:
        return jsonify({"answer": "Knowledge base not built yet."})

    data = request.json
    question = data.get("question")

    answer = ask_question(question, INDEX, CHUNKS)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
