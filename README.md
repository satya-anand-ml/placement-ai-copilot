# 🤖 Placement AI Co-Pilot

An AI-powered placement preparation assistant built using **Python, Streamlit, LangChain, Google Gemini, and RAG**.

The project is being developed step-by-step to evolve from a basic AI chatbot into an **Agentic AI-powered Placement Co-Pilot**.

---

## 🚀 Features

### Phase 1 — AI Chatbot
- 🤖 Google Gemini 2.5 Flash
- 💬 Streamlit chat interface
- 🧠 Conversation memory
- ➕ New Chat functionality

### Phase 2 — RAG
- 📄 PDF document ingestion
- ✂️ Text chunking
- 🧠 HuggingFace embeddings
- 🗄️ FAISS vector database
- 🔎 Similarity-based retrieval
- 🎯 Relevance filtering
- 📚 Source document & page information
- ⚡ Streaming AI responses
- 🛡️ Knowledge-base based answers

---

## 🧠 RAG Pipeline

```text
PDF Document
     ↓
PDF Loader
     ↓
Text Splitting
     ↓
HuggingFace Embeddings
     ↓
FAISS Vector Database
     ↓
Similarity Retrieval
     ↓
Relevant Context
     ↓
Google Gemini 2.5 Flash
     ↓
Streaming Response