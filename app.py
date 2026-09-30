import os
import streamlit as st

from utils.pdf_reader import load_documents
from utils.chunker import chunk_text
from utils.embedding import (
    create_embeddings,
    create_question_embedding
)
from utils.search import semantic_search
from utils.groq_helper import get_answer


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Company Knowledge Assistant",
    page_icon="📚"
)


# --------------------------------------------------
# Application Title
# --------------------------------------------------

st.title("📚 AI-Powered Company Knowledge Assistant")


# --------------------------------------------------
# Documents Folder
# --------------------------------------------------

DOCUMENT_FOLDER = "documents"

os.makedirs(DOCUMENT_FOLDER, exist_ok=True)


# --------------------------------------------------
# Session State
# --------------------------------------------------

if "chunks" not in st.session_state:
    st.session_state["chunks"] = []

if "embeddings" not in st.session_state:
    st.session_state["embeddings"] = None


# --------------------------------------------------
# Document Upload
# --------------------------------------------------

uploaded_files = st.file_uploader(
    "Upload Company Documents",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True
)


# --------------------------------------------------
# Save Uploaded Files
# --------------------------------------------------

if uploaded_files:

    for uploaded_file in uploaded_files:

        file_path = os.path.join(
            DOCUMENT_FOLDER,
            uploaded_file.name
        )

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    st.success("Documents uploaded successfully!")

    st.subheader("Uploaded Documents")

    for uploaded_file in uploaded_files:
        st.write(f"📄 {uploaded_file.name}")


# --------------------------------------------------
# Process Documents
# --------------------------------------------------

if st.button("Process Documents"):
    with st.spinner("Processing documents..."):
        df = load_documents(DOCUMENT_FOLDER)

        if df.empty:
            st.warning("No documents available.")

        else:
            # Remove documents where text extraction failed
            valid_documents = df[
                ~df["content"].astype(str).str.startswith("ERROR:")
            ]

            failed_documents = df[
                df["content"].astype(str).str.startswith("ERROR:")
            ]

            if not failed_documents.empty:
                st.warning("Some documents could not be processed:")

                for _, row in failed_documents.iterrows():
                    st.write(f"⚠️ {row['file_name']}")

            df = valid_documents

            if df.empty:
                st.error("No text could be extracted from the uploaded documents.")

            else:
                all_chunks = []

                for _, row in df.iterrows():
                    chunks = chunk_text(row["content"])

                    for chunk in chunks:
                        all_chunks.append({
                            "file_name": row["file_name"],
                            "chunk": chunk
                        })

                if not all_chunks:
                    st.error("No text could be extracted from the uploaded documents.")

                else:
                    embeddings = create_embeddings(all_chunks)

                    st.session_state["chunks"] = all_chunks
                    st.session_state["embeddings"] = embeddings

                    st.success("Documents processed successfully!")

                    st.write(f"📄 Documents processed: {len(df)}")
                    st.write(f"🧩 Chunks created: {len(all_chunks)}")


# --------------------------------------------------
# Ask Question
# --------------------------------------------------

st.divider()


# Question section
col1, col2 = st.columns(2)

with col1:
    st.subheader("Ask a Question")

with col2:
    if st.button("🗑️ Clear Chat"):
        st.session_state["question"] = ""
        st.rerun()

question = st.text_input(
    "Enter your question:",
    key="question"
)


# --------------------------------------------------
# Search
# --------------------------------------------------

if st.button("Search"):

    if not st.session_state["chunks"]:
        st.warning("Please upload and process documents first.")

    elif not question.strip():
        st.warning("Please enter a question.")

    else:

        with st.spinner("Searching documents..."):

            question_embedding = create_question_embedding(question)

            results = semantic_search(
                question_embedding,
                st.session_state["embeddings"],
                st.session_state["chunks"],
                top_k=3
            )

        # Check whether search returned results
        if not results:
            st.warning(
                "I could not find relevant information in the uploaded documents."
            )

        # Check relevance threshold
        elif results[0]["score"] < 0.30:

            st.warning(
                "I could not find relevant information in the uploaded documents."
            )

        else:

            # Build context from retrieved chunks
            context = "\n\n".join(
                [
                    f"Source: {result['file_name']}\n{result['chunk']}"
                    for result in results
                ]
            )

            # Generate answer using Groq
            with st.spinner("Generating answer..."):
                answer = get_answer(question, context)

            st.subheader("Answer")
            st.write(answer)

            st.subheader("Sources")

            for result in results:
                st.write(f"📄 **{result['file_name']}**")
                st.write(
                    f"Similarity Score: {result['score']:.4f}"
                )