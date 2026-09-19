# 🤖 Placement AI Co-Pilot

> An AI-powered placement preparation assistant evolving from a simple Gemini chatbot into an Agentic AI system.

**Placement AI Co-Pilot** is a phase-by-phase GenAI project designed to help students with:

- DSA
- Programming
- Technical Interviews
- Placement Preparation
- Company-specific hiring information
- Resume Preparation
- Career Guidance
- Computer Science Subjects

The project is intentionally being developed incrementally to understand and implement modern AI application architecture such as **RAG, Vector Databases, LangGraph, Memory, Tool Calling, Agentic AI, Multi-Agent Workflows, Human-in-the-Loop, and MCP**.

---

# 🚀 Project Evolution

```text
Phase 1
Gemini AI Chatbot
      │
      ▼
Phase 2
RAG + FAISS
      │
      ▼
Phase 3
Multi-Company RAG
      │
      ▼
Phase 4
LangGraph + Persistent State
      │
      ▼
Tool Calling
      │
      ▼
Agentic AI
      │
      ▼
Multi-Agent System
      │
      ▼
Human-in-the-Loop
      │
      ▼
MCP
      │
      ▼
Deployment
```

---

# 📌 Phase 1 — Gemini AI Chatbot

## 🎯 Goal

Build the basic conversational AI layer for placement preparation.

## 🛠️ What Was Built

- Streamlit chat interface
- Google Gemini 2.5 Flash integration
- Conversation context using Streamlit session state
- New Chat functionality
- Sidebar
- Placement-focused system prompt
- Streaming responses

## 🏗️ Architecture

```text
User
  │
  ▼
Streamlit UI
  │
  ▼
Conversation History
  │
  ▼
Gemini 2.5 Flash
  │
  ▼
AI Response
  │
  ▼
Streamlit UI
```

## 📚 Supported Areas

The chatbot can help with:

- Data Structures & Algorithms
- Programming
- Technical Interviews
- Placement Preparation
- Resume Preparation
- Career Guidance
- Computer Science Subjects

---

# 📚 Phase 2 — Retrieval-Augmented Generation (RAG)

## 🎯 Goal

Enable the chatbot to answer company-specific placement questions using information retrieved from reference documents.

The first implementation used a TCS placement reference document.

## 🔄 RAG Pipeline

```text
PDF Document
     │
     ▼
PyPDFLoader
     │
     ▼
Recursive Text Splitting
     │
     ▼
HuggingFace Embeddings
     │
     ▼
FAISS Vector Database
     │
     ▼
Retriever
     │
     ▼
Relevant Context
     │
     ▼
Gemini 2.5 Flash
     │
     ▼
Final Answer
```

## 🛠️ What Was Built

- PDF ingestion
- PDF page loading
- Recursive text splitting
- HuggingFace embeddings
- Sentence Transformer embeddings
- FAISS vector database
- Similarity-based retrieval
- Relevance filtering
- Source document information
- Page information
- Similarity scores
- RAG-specific prompting rules
- Streaming RAG responses

## 💡 Example

```text
User:
What is the minimum percentage required for TCS?

        ↓

FAISS retrieves relevant TCS chunks

        ↓

Gemini receives retrieved context

        ↓

Answer + source information
```

---

# 🏢 Phase 3 — Multi-Company RAG

## 🎯 Goal

Extend the RAG system from a single company to a shared **multi-company placement knowledge base**.

Instead of maintaining a separate vector database for every company, all company documents are stored in a common FAISS database with company metadata.

---

# 📂 Company Document Structure

```text
documents/
│
├── tcs/
│   └── TCS_All_India_NQT_2026_RAG_Reference.pdf
│
├── infosys/
│   └── Infosys_2026_Campus_Hiring_RAG_Reference_UNOFFICIAL.pdf
│
├── capgemini/
│   └── Capgemini_Exceller_2027_RAG_Reference_UNOFFICIAL.pdf
│
└── accenture/
```

More companies can be added later using the same structure.

---

# 🔄 Multi-Company Ingestion

The ingestion pipeline was upgraded from loading one fixed PDF to automatically scanning all PDFs inside the `documents/` directory.

```text
documents/
     │
     ▼
Find all PDF files
     │
     ▼
Detect company from folder name
     │
     ▼
Load PDF pages
     │
     ▼
Add company metadata
     │
     ▼
Split into chunks
     │
     ▼
Generate embeddings
     │
     ▼
Create shared FAISS database
```

Each document chunk receives metadata such as:

```python
{
    "company": "infosys",
    "source_file": "...",
    "source_path": "...",
    "page": 0
}
```

This allows the system to perform company-specific retrieval.

---

# 🔎 Company-Specific Retrieval

The retriever supports an optional company filter.

For example:

```text
Question:
What is the academic eligibility criteria for Infosys?

Company:
infosys
```

The retrieval process becomes:

```text
Question
   │
   ▼
Company = Infosys
   │
   ▼
FAISS Retrieval
   │
   ▼
Relevant Infosys Chunks
```

The same architecture works for:

```text
TCS
Infosys
Capgemini
Future Companies
```

---

# 🎯 Relevance Filtering

The retriever uses FAISS similarity search and converts the returned distance into a simple normalized score:

```python
similarity_score = 1 / (1 + distance)
```

Current configuration:

```python
TOP_K = 4
RELEVANCE_THRESHOLD = 0.30
```

Only sufficiently relevant chunks are passed into the RAG context.

This helps reduce irrelevant retrieved information.

---

# 🧠 General Questions vs Company Questions

A major improvement in Phase 3 was separating general questions from company-specific questions.

## General Question

Example:

```text
What is Binary Search?
```

Flow:

```text
User
  │
  ▼
No Company Detected
  │
  ▼
Gemini
  │
  ▼
Answer
```

Company documents are not unnecessarily retrieved.

---

## Company-Specific Question

Example:

```text
What is the academic eligibility criteria for Infosys?
```

Flow:

```text
User
  │
  ▼
Company Detection
  │
  ▼
Infosys Filter
  │
  ▼
FAISS Retrieval
  │
  ▼
Relevant Context
  │
  ▼
Gemini
  │
  ▼
Answer + Sources
```

---

# 🛡️ RAG Rules

The current system follows these rules for company-specific questions:

1. Use the provided knowledge base when relevant company information is available.
2. Do not use information from one company to answer a question about another company.
3. Do not invent missing company-specific information.
4. If required company information is unavailable, state that it was not found in the knowledge base.
5. General DSA, programming, and Computer Science questions can use general knowledge.
6. General questions should not incorrectly display company-specific RAG sources.

---

# 📖 Source Information

For retrieved company-specific answers, the application can display:

```text
🏢 Company
📄 Document
📑 Page
🎯 Similarity Score
```

Example:

```text
Company: infosys
Document: Infosys_2026_Campus_Hiring_RAG_Reference_UNOFFICIAL.pdf
Page: 1
Similarity: 0.61
```

This makes the RAG pipeline more transparent and helps verify the retrieved context.

---

# 🧩 Current Architecture

This is the architecture actually implemented at the end of **Phase 3**.

```text
                         ┌──────────────┐
                         │     USER     │
                         └──────┬───────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Streamlit UI   │
                       └────────┬─────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │    User Query    │
                       └────────┬─────────┘
                                │
                                ▼
                     ┌───────────────────────┐
                     │  Company Detection    │
                     └──────────┬────────────┘
                                │
                  ┌─────────────┴─────────────┐
                  │                           │
                  ▼                           ▼
            General Query              Company Query
                  │                           │
                  ▼                           ▼
               Gemini                 Company Filter
                                              │
                                              ▼
                                       FAISS Retriever
                                              │
                                              ▼
                                       Relevant Chunks
                                              │
                                              ▼
                                       Context Builder
                                              │
                  └───────────────────────────┘
                                │
                                ▼
                       Gemini 2.5 Flash
                                │
                                ▼
                       Streaming Response
                                │
                                ▼
                          Streamlit UI
```

---

# 🗄️ Current RAG Architecture

A single shared FAISS database is used for the company knowledge base.

```text
             TCS PDF
                │
          Infosys PDF
                │
        Capgemini PDF
                │
                ▼
        ┌─────────────────┐
        │  PDF Ingestion  │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Text Chunking   │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ HuggingFace     │
        │ Embeddings      │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Shared FAISS DB │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Company Metadata│
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ Relevant Docs   │
        └────────┬────────┘
                 │
                 ▼
              Gemini
```

This architecture makes adding new companies straightforward.

---

# 🧪 Testing

The system has been tested with both general and company-specific queries.

## TCS

```text
What is the minimum percentage required for TCS?
```

## Infosys

```text
What is the academic eligibility criteria for Infosys?
```

## Capgemini

```text
Tell me the syllabus of Capgemini.
```

## General DSA

```text
What is Binary Search?
```

The application distinguishes between general questions and company-specific RAG queries.

---

# 📁 Project Structure

```text
placement-ai-copilot/
│
├── app.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env
│
├── documents/
│   ├── tcs/
│   │   └── TCS_All_India_NQT_2026_RAG_Reference.pdf
│   │
│   ├── infosys/
│   │   └── Infosys_2026_Campus_Hiring_RAG_Reference_UNOFFICIAL.pdf
│   │
│   ├── capgemini/
│   │   └── Capgemini_Exceller_2027_RAG_Reference_UNOFFICIAL.pdf
│   │
│   └── accenture/
│
├── rag/
│   ├── ingest.py
│   ├── retriever.py
│   └── rag_chain.py
│
└── vectorstore/
    └── placement_faiss/
```

---

# 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Programming Language | Python |
| LLM | Google Gemini 2.5 Flash |
| UI | Streamlit |
| Framework | LangChain |
| PDF Loader | PyPDFLoader |
| Text Splitter | RecursiveCharacterTextSplitter |
| Embeddings | HuggingFace / Sentence Transformers |
| Vector Database | FAISS |
| Version Control | Git & GitHub |

---

# ⚙️ Setup

## 1. Clone the Repository

```bash
git clone https://github.com/satya-anand-ml/placement-ai-copilot.git
```

## 2. Navigate to the Project

```bash
cd placement-ai-copilot
```

## 3. Create Virtual Environment

```bash
python -m venv place
```

## 4. Activate Virtual Environment

Windows PowerShell:

```powershell
place\Scripts\activate
```

## 5. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

# 🔑 Environment Setup

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

> Never commit the `.env` file to GitHub.

---

# 📚 Build the Knowledge Base

Whenever company PDFs are added or changed:

```powershell
python rag/ingest.py
```

This rebuilds:

```text
vectorstore/placement_faiss/
```

---

# 🔍 Test the Retriever

Run:

```powershell
python rag/retriever.py
```

Example:

```text
Ask a question:
What is the academic eligibility criteria for Infosys?

Company filter:
infosys
```

The retriever displays:

- Retrieved chunks
- Company
- Source document
- Page
- Similarity score
- Metadata

---

# ▶️ Run the Application

Start Streamlit:

```powershell
streamlit run app.py
```

The application will open in your browser.

---

# 🗺️ Roadmap

The project will continue evolving through the following phases.

---

## Phase 4 — LangGraph

**Next Major Phase**

Planned concepts:

- Graph-based workflows
- State
- Nodes
- Edges
- Conditional Edges
- Query Routing
- Thread IDs
- Checkpointing
- Persistent Conversation State

Expected architecture:

```text
User
 ↓
LangGraph
 ↓
State
 ↓
Nodes
 ↓
Conditional Routing
 ↓
RAG / LLM / Tools
 ↓
Final Response
```

---

## Phase 5 — Persistent Memory

Planned:

- SQLite / SQL chat storage
- Persistent chat history
- Conversation threads
- Long-term user memory
- User-specific information

Example:

```text
Chat 1
User: My name is Satya.
        ↓
Persistent Memory
        ↓
Chat 2
User: What is my name?
        ↓
AI: Your name is Satya.
```

---

## Phase 6 — Tool Calling

Potential tools:

- Web Search
- Placement Information Tools
- Resume Utilities
- Coding Utilities
- External APIs

---

## Phase 7 — Agentic AI

Move from a fixed workflow toward an AI system capable of deciding which action, tool, or knowledge source should be used.

```text
User
  ↓
Agent
  ↓
Decide / Route
  ├── RAG
  ├── LLM
  └── Tool
  ↓
Result
  ↓
Final Response
```

---

## Phase 8 — Multi-Agent System

Potential specialized agents:

```text
                 Placement AI
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
    DSA Agent      RAG Agent    Resume Agent
        │             │             │
        └─────────────┼─────────────┘
                      ▼
                Final Response
```

---

## Phase 9 — Human-in-the-Loop

Add human approval and intervention to selected workflows.

---

## Phase 10 — MCP

Explore **Model Context Protocol (MCP)** for connecting the AI system with external tools and services.

---

## Phase 11 — Deployment

Deploy the complete system for real-world use.

---

# 🎯 Long-Term Vision

The long-term goal is to evolve Placement AI Co-Pilot into a complete **Agentic AI Placement Assistant**.

```text
                           USER
                             │
                             ▼
                    Placement AI
                      Co-Pilot
                             │
                             ▼
                         LangGraph
                             │
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
          Memory            RAG             Tools
             │               │               │
             ▼               ▼               ▼
           SQL DB        FAISS KB       External APIs
                             │
                             ▼
                    Company Knowledge
                    /      |       \
                  TCS   Infosys   Capgemini
                             │
                             ▼
                     Agentic Workflow
                             │
                   ┌─────────┴─────────┐
                   ▼                   ▼
               AI Agents             HITL
                   │                   │
                   └─────────┬─────────┘
                             ▼
                            MCP
                             │
                             ▼
                      External Systems
```

---

# 📌 Development Status

| Phase | Status |
|---|---|
| Phase 1 — Gemini Chatbot | ✅ Completed |
| Phase 2 — RAG + FAISS | ✅ Completed |
| Phase 3 — Multi-Company RAG | ✅ Completed |
| Phase 4 — LangGraph | 🔜 Next |
| Phase 5 — Persistent Memory | 🔜 Planned |
| Phase 6 — Tool Calling | 🔜 Planned |
| Phase 7 — Agentic AI | 🔜 Planned |
| Phase 8 — Multi-Agent System | 🔜 Planned |
| Phase 9 — Human-in-the-Loop | 🔜 Planned |
| Phase 10 — MCP | 🔜 Planned |
| Phase 11 — Deployment | 🔜 Planned |

---

# 👨‍💻 Author

**Satya Anand**

B.Tech — Computer Science & Engineering

GitHub:

https://github.com/satya-anand-ml/placement-ai-copilot

---

## ⭐ Project Philosophy

> **Build it step-by-step. Understand every layer. Then make it agentic.**

This project is continuously evolving from a:

**Basic GenAI Chatbot → RAG System → Multi-Company Knowledge Assistant → LangGraph Workflow → Agentic AI System**