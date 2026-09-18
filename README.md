# 🤖 Placement AI Co-Pilot

> An evolving GenAI-powered assistant designed to help students with placement preparation, DSA, technical interviews, resumes, and career guidance.

## 📌 Project Overview

Placement AI Co-Pilot is a GenAI-based student placement assistant that is being developed incrementally.

The project will evolve from a simple conversational AI chatbot into an advanced **Agentic AI system** with:

- Retrieval-Augmented Generation (RAG)
- LangGraph workflows
- Multi-Agent architecture
- Tool calling
- Human-in-the-Loop (HITL)
- MCP integrations
- Persistent memory
- External services and APIs

The project is being developed **phase by phase**, with each phase introducing a new capability.

---

# 🚀 Current Status

### Phase 1 — Basic GenAI Chatbot ✅

The current version provides a basic conversational AI assistant powered by **Google Gemini**.

### Current Features

- 🤖 Gemini-powered AI chatbot
- 💬 Interactive Streamlit chat interface
- 🧠 Conversation memory within the current session
- ➕ New Chat functionality
- 🔐 Environment-variable based API key management
- 💻 Simple and extensible project structure

---

# 🏗️ Current Architecture

```text
                 User
                   │
                   ▼
          ┌─────────────────┐
          │ Streamlit Chat UI│
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Conversation    │
          │ Memory          │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Google Gemini   │
          │ LLM             │
          └────────┬────────┘
                   │
                   ▼
              AI Response