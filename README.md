```md

# Link - https://trippy-chatbot.streamlit.app/

# RAG-Based Website Chatbot

## Overview

This project implements a Retrieval-Augmented Generation (RAG) based chatbot that answers user questions using the content of any website provided as input.

The system crawls a website, extracts readable text, builds a semantic knowledge base using vector embeddings, and generates answers grounded strictly in the retrieved website content. The application is built with Streamlit and is deployable on Streamlit Cloud.

---

## Features

- Accepts any public website URL
- Crawls website content up to two levels deep
- Handles JavaScript-blocked and cloud-restricted websites gracefully
- Builds a vector-based knowledge base using FAISS
- Performs semantic search to retrieve relevant context
- Generates responses using an LLM via OpenRouter API
- Interactive chat-style user interface
- Deployed and accessible via Streamlit Cloud

---

## What is Retrieval-Augmented Generation (RAG)

Retrieval-Augmented Generation is a technique that combines information retrieval with language generation.

1. Retrieval  
   Relevant content is fetched from a knowledge base using semantic similarity search.

2. Generation  
   A language model generates an answer strictly based on the retrieved content.

This approach reduces hallucination and ensures responses are grounded in real data.

---

## System Architecture

High-level workflow:

User  
→ Streamlit UI  
→ Website Crawler  
→ Text Processing  
→ Embedding Generation  
→ FAISS Vector Store  
→ Semantic Retrieval  
→ LLM (OpenRouter)  
→ Answer to User

---

## Technology Stack

- Language: Python
- UI: Streamlit
- Web Crawling: requests, BeautifulSoup
- Text Processing: Custom chunking logic
- Embeddings: sentence-transformers (all-MiniLM-L6-v2)
- Vector Store: FAISS (CPU)
- LLM Provider: OpenRouter API
- Deployment: Streamlit Cloud

---

## Project Structure

```

rag-website-chatbot/
│
├── app.py
├── crawler.py
├── text_processor.py
├── embeddings.py
├── rag_chatbot.py
├── requirements.txt
├── README.md
└── .gitignore

```

---

## How It Works

1. User enters a website URL
2. The crawler fetches HTML pages within defined limits
3. Visible text is extracted and cleaned
4. Text is split into chunks
5. Embeddings are generated for each chunk
6. Chunks are stored in a FAISS index
7. User queries are embedded and matched semantically
8. Relevant content is passed to the LLM
9. The model generates a response using only retrieved context

---

## Error Handling

- Invalid URLs are handled gracefully
- Websites blocking automated access are detected
- Knowledge base is not built when content is unavailable
- The chatbot avoids generating answers when context is insufficient

---

## Limitations

- Some enterprise websites block cloud-based crawlers
- Knowledge base is stored in memory (non-persistent)
- Performance depends on website size and network latency
- JavaScript-heavy websites may not be fully crawlable on Streamlit Cloud

---

## Example Use Cases

- Understanding company websites
- Exploring documentation portals
- Creating domain-specific chatbots from public websites
- Educational demonstrations of RAG systems

---

## Deployment

The application is deployed using Streamlit Cloud.

Secrets such as API keys are managed securely using Streamlit Secrets.

---

## Future Enhancements

- Persistent vector storage
- Support for document uploads (PDF, DOCX)
- Streaming responses
- Multi-user session handling
- Advanced crawling strategies
- Cloud-hosted embedding services

---
