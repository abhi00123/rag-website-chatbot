import streamlit as st
from crawler import crawl_website
from text_processor import chunk_text
from embeddings import create_faiss_index
from rag_chatbot import ask_question

st.set_page_config(page_title="Trippy Web-Chatbot", layout="wide")

st.title("Trippy Web-Chatbot")

if "index" not in st.session_state:
    st.session_state.index = None
    st.session_state.chunks = None

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Website Setup")
    url = st.text_input("Enter Website URL")

    if st.button("Build Knowledge Base", use_container_width=True):
        if not url:
            st.error("Please enter a website URL")
        else:
            with st.spinner("Building knowledge base, please wait..."):
                pages = crawl_website(url)
                combined_text = " ".join(pages).strip()

                if not combined_text or len(combined_text) < 500:
                    st.error(
                        "This website blocks automated access from cloud servers. "
                        "Try another site or run the app locally for this URL."
                    )
                    st.session_state.index = None
                    st.session_state.chunks = None
                else:
                    chunks = chunk_text(combined_text, chunk_size=800)
                    index, _ = create_faiss_index(chunks)

                    st.session_state.index = index
                    st.session_state.chunks = chunks
                    st.session_state.messages = []

                    st.success("Knowledge base built successfully")

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []

st.subheader("Chat")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask something about the website")

if question:
    if st.session_state.index is None:
        st.error("Please build the knowledge base first")
    else:
        st.session_state.messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                answer = ask_question(
                    question,
                    st.session_state.index,
                    st.session_state.chunks
                )
                st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
