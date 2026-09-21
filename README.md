
````markdown
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

The project is intentionally being developed incrementally to understand and implement modern AI application architecture such as **RAG, Vector Databases, LangGraph, Persistent State, Memory, Tool Calling, Agentic AI, Multi-Agent Workflows, Human-in-the-Loop, and MCP**.

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
LangGraph + SQLite Persistence
      │
      ▼
Phase 5
Long-Term Memory
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
````

---

# 📌 Phase 1 — Gemini AI Chatbot

## 🎯 Goal

Build the basic conversational AI layer for placement preparation.

## 🛠️ What Was Built

* Streamlit chat interface
* Google Gemini 2.5 Flash integration
* Conversation context using Streamlit session state
* New Chat functionality
* Sidebar
* Placement-focused system prompt
* Streaming responses

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

* Data Structures & Algorithms
* Programming
* Technical Interviews
* Placement Preparation
* Resume Preparation
* Career Guidance
* Computer Science Subjects

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

* PDF ingestion
* PDF page loading
* Recursive text splitting
* HuggingFace embeddings
* Sentence Transformer embeddings
* FAISS vector database
* Similarity-based retrieval
* Relevance filtering
* Source document information
* Page information
* Similarity scores
* RAG-specific prompting rules
* Streaming RAG responses

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

The ingestion pipeline automatically scans all PDFs inside the `documents/` directory.

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

Example:

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

The retriever uses FAISS similarity search and converts the returned distance into a normalized score:

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

# 🧠 Phase 4 — LangGraph + Persistent State

## 🎯 Goal

Move the application from a direct Streamlit → Gemini flow to a **stateful graph-based workflow** using LangGraph.

Phase 4 introduced:

* LangGraph state
* Nodes
* Edges
* Conditional routing
* Thread IDs
* Persistent conversation checkpoints
* SQLite-backed LangGraph state
* Persistent chat history
* Chat switching
* Chat deletion

---

# 🔄 LangGraph Workflow

The current workflow is:

```text
User Query
    │
    ▼
LangGraph State
    │
    ▼
Question Classifier
    │
    ├───────────────┐
    │               │
    ▼               ▼
General Query   Company Query
    │               │
    ▼               ▼
General Node    Company/RAG Node
    │               │
    │               ▼
    │          FAISS Retrieval
    │               │
    │               ▼
    │          Relevant Context
    │               │
    └───────┬───────┘
            ▼
      Answer Generation
            │
            ▼
       Gemini 2.5 Flash
            │
            ▼
        Final Response
```

---

# 🧩 LangGraph State

The graph maintains a shared state containing:

```python
class PlacementState(TypedDict):
    messages: Annotated[list, add_messages]
    question: str
    company: str
    question_type: str
    context: str
    sources: list
    response: str
```

This allows different nodes to work with the same workflow state.

---

# 🔀 Conditional Routing

The graph separates general questions from company-specific questions.

```text
                  User Question
                       │
                       ▼
                 Classifier
                  /       \
                 /         \
                ▼           ▼
           General       Company
              │             │
              ▼             ▼
           Gemini          RAG
              │             │
              └──────┬──────┘
                     ▼
               Answer Node
```

This keeps the graph modular and makes it easier to add tools and agents later.

---

# 🧵 Thread-Based Conversation Memory

Each chat receives a unique `thread_id`.

Example:

```text
Chat 1
thread_id = abc
     │
     ├── User: My name is Satya
     └── User: What is my name?
             ↓
          Satya
```

A new chat gets a different thread:

```text
Chat 2
thread_id = xyz
     │
     └── Separate conversation state
```

This provides **conversation-level memory isolation**.

> Note: This is thread-level conversation memory. Cross-chat long-term user memory is planned for a later phase.

---

# 🗄️ SQLite Persistence

Phase 4 replaced temporary in-memory LangGraph checkpointing with a SQLite-backed checkpointer.

```text
LangGraph
    │
    ▼
SqliteSaver
    │
    ▼
database/langgraph_checkpoints.db
```

This allows LangGraph checkpoints to persist across application restarts.

The project also maintains a separate SQLite database for application-level chat history:

```text
database/
├── chat_history.db
└── langgraph_checkpoints.db
```

These databases have different responsibilities:

| Database                   | Purpose                                                  |
| -------------------------- | -------------------------------------------------------- |
| `chat_history.db`          | Chat list, titles, messages, chat switching and deletion |
| `langgraph_checkpoints.db` | LangGraph workflow state/checkpoints                     |

Database files are intentionally ignored by Git and are not committed to the repository.

---

# 💬 Persistent Chat History

The application now supports:

* New Chat
* Previous Chat History
* Opening an existing chat
* Persistent messages
* Automatic chat titles
* Chat deletion
* Unique thread IDs

Example:

```text
Sidebar
│
├── New Chat
│
├── Chat History
│   ├── Chat 1     🗑️
│   ├── Chat 2     🗑️
│   └── Chat 3     🗑️
│
└── Current Thread ID
```

Deleting a chat removes its application-level chat record and messages from `chat_history.db`.

---

# 🧪 Phase 4 Testing

### Same-thread memory

```text
User: My name is Satya.

User: What is my name?

AI: Satya
```

### Thread isolation

```text
Chat 1:
My name is Satya.
        ↓
New Chat
        ↓
What is my name?

→ The new chat has a separate conversation thread.
```

### Persistent state

LangGraph checkpoints are stored in:

```text
database/langgraph_checkpoints.db
```

### Chat history

Application-level messages are stored in:

```text
database/chat_history.db
```

### Delete

A chat can be deleted directly from the sidebar.

---

# 🏗️ Current Architecture

The architecture after **Phase 4** is now:

```text
                         ┌──────────────────┐
                         │       USER       │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │   Streamlit UI   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    Chat DB       │
                         │   chat_history   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │    LangGraph     │
                         │     State        │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │     Router       │
                         └────────┬─────────┘
                                  │
                     ┌────────────┴────────────┐
                     │                         │
                     ▼                         ▼
              General Query              Company Query
                     │                         │
                     ▼                         ▼
                  Gemini                  FAISS RAG
                                               │
                                               ▼
                                      Relevant Context
                                               │
                     ┌─────────────────────────┘
                     ▼
                Answer Generation
                     │
                     ▼
              Gemini 2.5 Flash
                     │
                     ▼
               Final Response

LangGraph State
      │
      ▼
SqliteSaver
      │
      ▼
langgraph_checkpoints.db
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

## LangGraph Memory

```text
Chat 1:
My name is Satya.

Chat 1:
What is my name?
→ Satya

New Chat:
What is my name?
→ Separate thread; long-term cross-chat memory is not implemented yet.
```

---

# 📁 Project Structure

```text
placement-ai-copilot/
│
├── app.py
├── chat_db.py
├── README.md
├── requirements.txt
├── .gitignore
├── .env
│
├── database/
│   ├── chat_history.db
│   └── langgraph_checkpoints.db
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
├── langgraph/
│   ├── basic_graph.py
│   └── placement_graph.py
│
├── rag/
│   ├── ingest.py
│   ├── retriever.py
│   └── rag_chain.py
│
└── vectorstore/
    └── placement_faiss/
```

> `.env`, SQLite databases, the Python virtual environment, FAISS vectorstore, and other local/generated files are excluded from Git according to `.gitignore`.

---

# 🛠️ Tech Stack

| Layer                | Technology                          |
| -------------------- | ----------------------------------- |
| Programming Language | Python                              |
| LLM                  | Google Gemini 2.5 Flash             |
| UI                   | Streamlit                           |
| LLM/RAG Framework    | LangChain                           |
| Graph Framework      | LangGraph                           |
| Checkpointing        | LangGraph SQLite Checkpointer       |
| Database             | SQLite                              |
| PDF Loader           | PyPDFLoader                         |
| Text Splitter        | RecursiveCharacterTextSplitter      |
| Embeddings           | HuggingFace / Sentence Transformers |
| Vector Database      | FAISS                               |
| Version Control      | Git & GitHub                        |

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

* Retrieved chunks
* Company
* Source document
* Page
* Similarity score
* Metadata

---

# 🧠 Test LangGraph Import

To verify that the graph loads without executing a Gemini request:

```powershell
python -c "from langgraph.placement_graph import graph; print('LangGraph loaded successfully')"
```

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

## ✅ Phase 4 — LangGraph + Persistent State

**Completed**

Implemented:

* Graph-based workflows
* Typed state
* Nodes
* Edges
* Conditional routing
* Query classification
* Thread IDs
* LangGraph checkpointing
* SQLite-backed checkpoint persistence
* Persistent chat history
* Chat switching
* Chat deletion

---

## 🚧 Phase 5 — Long-Term Memory

**Next**

Planned:

* Cross-chat user memory
* User profile memory
* Memory extraction
* Memory retrieval
* SQLite-based long-term memory
* Selective memory storage

Example target behavior:

```text
Chat 1
User: My name is Satya.
        ↓
Long-Term Memory
        ↓
Chat 2
User: What is my name?
        ↓
AI: Your name is Satya.
```

> Phase 4 currently provides thread-level conversation memory. Cross-chat long-term memory is a separate upcoming feature.

---

## Phase 6 — Tool Calling

Potential tools:

* Web Search
* Placement Information Tools
* Resume Utilities
* Coding Utilities
* External APIs

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
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      DSA Agent     RAG Agent    Resume Agent
          │            │            │
          └────────────┼────────────┘
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
                    Placement AI Co-Pilot
                             │
                             ▼
                         LangGraph
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
           Memory           RAG            Tools
              │              │              │
              ▼              ▼              ▼
           SQL DB        FAISS KB      External APIs
                             │
                             ▼
                     Company Knowledge
                       /      |       \
                     TCS   Infosys   Capgemini
                             │
                             ▼
                     Agentic Workflow
                             │
                  ┌──────────┴──────────┐
                  ▼                     ▼
              AI Agents               HITL
                  │                     │
                  └──────────┬──────────┘
                             ▼
                            MCP
                             │
                             ▼
                      External Systems
```

---

# 📌 Development Status

| Phase                                  | Status      |
| -------------------------------------- | ----------- |
| Phase 1 — Gemini Chatbot               | ✅ Completed |
| Phase 2 — RAG + FAISS                  | ✅ Completed |
| Phase 3 — Multi-Company RAG            | ✅ Completed |
| Phase 4 — LangGraph + Persistent State | ✅ Completed |
| Phase 5 — Long-Term Memory             | 🚧 Next     |
| Phase 6 — Tool Calling                 | 🔜 Planned  |
| Phase 7 — Agentic AI                   | 🔜 Planned  |
| Phase 8 — Multi-Agent System           | 🔜 Planned  |
| Phase 9 — Human-in-the-Loop            | 🔜 Planned  |
| Phase 10 — MCP                         | 🔜 Planned  |
| Phase 11 — Deployment                  | 🔜 Planned  |

---

# 👨‍💻 Author

**Satya Anand**

B.Tech — Computer Science & Engineering

GitHub:

[https://github.com/satya-anand-ml/placement-ai-copilot](https://github.com/satya-anand-ml/placement-ai-copilot)

---

## ⭐ Project Philosophy

> **Build it step-by-step. Understand every layer. Then make it agentic.**

This project is continuously evolving from a:

**Basic GenAI Chatbot → RAG System → Multi-Company Knowledge Assistant → LangGraph Workflow → Persistent AI Assistant → Agentic AI System**

```
```
