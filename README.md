# 📚 AI-Powered Company Knowledge Assistant

An AI-powered document-based knowledge assistant that allows users to upload company documents and ask natural-language questions. The system retrieves relevant information from the uploaded documents and uses a Large Language Model (LLM) to generate context-aware answers.

## 🚀 Features

- Upload PDF, DOCX, and TXT documents
- Extract text from uploaded documents
- Store document information using Pandas
- Split documents into smaller chunks
- Generate embeddings using Sentence Transformers
- Perform semantic search using cosine similarity
- Retrieve the top 3 relevant document chunks
- Generate answers using Groq LLM
- Answer questions using retrieved document context
- Display source documents and similarity scores
- Handle questions where relevant information is not available
- Handle invalid or empty documents
- Streamlit-based user interface

## 🏗️ Architecture

```text
User
 │
 ▼
Streamlit UI
 │
 ▼
Upload Documents
 │
 ▼
Document Text Extraction
 │
 ▼
Text Chunking
 │
 ▼
Sentence Transformer Embeddings
 │
 ▼
Semantic Search
 │
 ▼
Top 3 Relevant Chunks
 │
 ▼
Groq LLM
 │
 ▼
Answer + Source Documents