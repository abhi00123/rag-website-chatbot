RAG-Based Website Chatbot (Full-Stack, Local LLM)

--------------------------------------------------

PROJECT TITLE
-------------
RAG-Based Chatbot for Any Website URL


PROJECT OVERVIEW
----------------
This project implements a Retrieval-Augmented Generation (RAG) based chatbot
that can answer user questions using the content of any website provided as input.

The system crawls a website, extracts and processes readable text, builds a
semantic knowledge base using vector embeddings, retrieves relevant information
for user queries, and generates answers using a local Large Language Model (LLM)
via Ollama.

A Chatbot-style web interface is built using HTML, CSS, and JavaScript, with a
Flask backend connecting the frontend to the RAG pipeline.


KEY OBJECTIVES
--------------
- Accept any website URL as input
- Crawl website content (up to 2 levels deep)
- Support JavaScript-rendered websites using Selenium
- Build a vector-based knowledge base
- Perform semantic search for relevant content
- Generate grounded answers using retrieved context
- Provide a clean, interactive chat interface


WHAT IS RAG (RETRIEVAL-AUGMENTED GENERATION)?
--------------------------------------------
RAG is a technique that combines two steps:

1. Retrieval:
   Fetching relevant information from a knowledge base using semantic search

2. Generation:
   Using a language model to generate answers based only on retrieved data

This approach reduces hallucination and improves factual accuracy by grounding
responses in real website content.


SYSTEM ARCHITECTURE SUMMARY
---------------------------
High-level flow:

User
 -> Frontend UI (HTML, CSS, JavaScript)
 -> Flask Backend API
 -> RAG Pipeline
 -> Local LLM (Ollama)
 -> Answer returned to user

RAG Pipeline includes:
- Website crawling (static + Selenium fallback)
- Text cleaning and chunking
- Embedding generation
- Vector storage using FAISS
- Semantic retrieval
- LLM-based answer generation


COMPONENT BREAKDOWN
-------------------

1. Frontend (HTML, CSS, JavaScript)
- Chatbot-style user interface
- URL input for website crawling
- Chat input for questions
- Displays chat history
- Communicates with backend using REST APIs

2. Backend (Flask - Python)
- Acts as API layer
- Endpoints:
  - /build_kb : Crawls website and builds knowledge base
  - /ask      : Answers user questions using RAG
- Manages FAISS index and text chunks in memory

3. Website Crawling
- Static crawling using requests and BeautifulSoup
- Selenium fallback for JavaScript-rendered websites
- Extracts headings and paragraph text
- Ignores scripts, styles, images, and non-text content

4. Text Processing
- Cleans extracted website text
- Splits content into fixed-size chunks
- Prepares data for embedding generation

5. Embeddings
- Uses sentence-transformers
- Model: all-MiniLM-L6-v2
- Converts text chunks into vector representations

6. Vector Database (FAISS)
- In-memory vector store
- Enables fast semantic similarity search
- Retrieves top-K relevant chunks for each query

7. Local LLM (Ollama)
- Model used: Mistral
- Runs locally on CPU
- Generates answers strictly from retrieved context
- No external API or billing required


TECHNOLOGY STACK
----------------
Language      : Python
Backend       : Flask
Frontend      : HTML, CSS, JavaScript
Crawling      : requests, BeautifulSoup, Selenium
Embeddings    : sentence-transformers
Vector Store  : FAISS
LLM           : Ollama (Mistral)


PROJECT STRUCTURE
-----------------
rag_chatbot_web/
|
|-- backend/
|   |-- app.py
|   |-- crawler.py
|   |-- selenium_crawler.py
|   |-- text_processor.py
|   |-- embeddings.py
|   |-- rag_chatbot.py
|
|-- frontend/
|   |-- index.html
|   |-- style.css
|   |-- script.js
|
|-- README.txt


LIMITATIONS
-----------
- Knowledge base is stored in memory (not persistent)
- Large websites may increase crawling time
- Local LLM response speed depends on system resources
- Not deployed to cloud due to local LLM dependency


FUTURE ENHANCEMENTS
-------------------
- Persistent vector database (ChromaDB / Pinecone)
- Multi-user session support
- Streaming responses
- PDF and document ingestion
- Cloud deployment with hosted LLM
- Authentication and user history


EXAMPLE USE CASES
-----------------
- Ask questions about company websites
- Explore documentation and informational sites
- Build domain-specific chatbots from website data

PROJECT STATUS
--------------
- Fully working local system
- Hybrid crawler (static + JavaScript websites)
- Complete RAG pipeline
- Chatbot-style web UI
