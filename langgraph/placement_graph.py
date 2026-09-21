from typing import TypedDict, Annotated
from pathlib import Path

from dotenv import load_dotenv

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from langgraph.graph.message import add_messages

import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import (
    HumanMessage,
    AIMessage
)

from rag.retriever import retrieve_documents


# ============================================================
# 1. ENVIRONMENT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(
    BASE_DIR / ".env"
)


# ============================================================
# 2. GEMINI LLM
# ============================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)


# ============================================================
# 3. GRAPH STATE
# ============================================================

class PlacementState(TypedDict):

    # Conversation memory
    messages: Annotated[
        list,
        add_messages
    ]

    # Current question
    question: str

    # Detected company
    company: str

    # general / company
    question_type: str

    # RAG context
    context: str

    # RAG source information
    sources: list

    # Final answer
    response: str


# ============================================================
# 4. CLASSIFIER NODE
# ============================================================

def classify_question(state: PlacementState):

    question = state["question"].lower()

    print("\n🔎 Classifying question...")
    print(
        f"Question: {state['question']}"
    )

    company_keywords = {

        "tcs": "tcs",

        "infosys": "infosys",

        "capgemini": "capgemini",

        "accenture": "accenture",

        "cognizant": "cognizant",

        "wipro": "wipro",

        "deloitte": "deloitte",

        "hcl": "hcltech",

        "hcltech": "hcltech",

        "ltimindtree": "ltimindtree",

        "tech mahindra": "techmahindra",

        "techmahindra": "techmahindra"
    }

    detected_company = ""

    for keyword, company_name in company_keywords.items():

        if keyword in question:

            detected_company = company_name

            break

    if detected_company:

        question_type = "company"

    else:

        question_type = "general"

    print(
        f"🏢 Company: "
        f"{detected_company if detected_company else 'None'}"
    )

    print(
        f"📌 Question Type: "
        f"{question_type}"
    )

    return {

        "company": detected_company,

        "question_type": question_type
    }


# ============================================================
# 5. GENERAL NODE
# ============================================================

def general_node(state: PlacementState):

    print("\n🤖 General Question Node")

    return {

        "context": "",

        "sources": []
    }


# ============================================================
# 6. COMPANY RAG NODE
# ============================================================

def company_node(state: PlacementState):

    question = state["question"]

    company = state["company"]

    print("\n🏢 Company RAG Node")

    print(
        f"Company detected: {company}"
    )

    print(
        "\n🔎 Searching FAISS knowledge base..."
    )

    results = retrieve_documents(
        question=question,
        company=company
    )

    # --------------------------------------------------------
    # No relevant documents
    # --------------------------------------------------------

    if not results:

        print(
            "❌ No relevant documents found."
        )

        return {

            "context": "",

            "sources": []
        }


    # --------------------------------------------------------
    # Prepare context + sources
    # --------------------------------------------------------

    context_parts = []

    sources = []


    for index, (doc, score) in enumerate(
        results,
        start=1
    ):

        company_name = doc.metadata.get(
            "company",
            "Unknown"
        )

        source_file = doc.metadata.get(
            "source_file",
            "Unknown"
        )

        source_path = doc.metadata.get(
            "source_path",
            "Unknown"
        )

        page = doc.metadata.get(
            "page",
            "Unknown"
        )


        print(
            f"\n📚 Retrieved Chunk {index}"
        )

        print(
            f"Company: {company_name}"
        )

        print(
            f"Source: {source_file}"
        )

        print(
            f"Page: {page}"
        )

        print(
            f"Score: {score:.4f}"
        )


        # Context

        context_parts.append(
            doc.page_content
        )


        # Source metadata

        sources.append(
            {

                "company": company_name,

                "source_file": source_file,

                "source_path": source_path,

                "page": page,

                "score": score
            }
        )


    context = "\n\n".join(
        context_parts
    )


    return {

        "context": context,

        "sources": sources
    }


# ============================================================
# 7. ROUTER
# ============================================================

def route_question(state: PlacementState):

    if state["question_type"] == "company":

        return "company"

    return "general"


# ============================================================
# 8. BUILD CONVERSATION HISTORY
# ============================================================

def build_conversation_history(
    messages
):

    if not messages:

        return "No previous conversation."


    history_parts = []


    for message in messages:

        if isinstance(
            message,
            HumanMessage
        ):

            role = "User"

        elif isinstance(
            message,
            AIMessage
        ):

            role = "Assistant"

        else:

            continue


        history_parts.append(
            f"{role}: {message.content}"
        )


    return "\n".join(
        history_parts
    )


# ============================================================
# 9. GEMINI RESPONSE NODE
# ============================================================

def generate_answer(
    state: PlacementState
):

    question = state["question"]

    question_type = state["question_type"]

    company = state["company"]

    context = state["context"]

    messages = state["messages"]


    print("\n🤖 Gemini Node")

    print(
        "Generating final answer..."
    )


    # ========================================================
    # CONVERSATION HISTORY
    # ========================================================

    conversation_history = (
        build_conversation_history(
            messages
        )
    )


    # ========================================================
    # COMPANY-SPECIFIC QUESTION
    # ========================================================

    if question_type == "company":


        # ----------------------------------------------------
        # No RAG context
        # ----------------------------------------------------

        if not context:

            response_text = (
                "I couldn't find this information "
                "in the provided knowledge base."
            )

            return {

                "response": response_text,

                "messages": [
                    AIMessage(
                        content=response_text
                    )
                ]
            }


        # ----------------------------------------------------
        # Company RAG prompt
        # ----------------------------------------------------

        prompt = f"""
You are Placement AI Co-Pilot.

Answer the user's company-specific placement
question using ONLY the provided knowledge base
context.

Company:
{company}

Knowledge Base Context:
{context}

Conversation History:
{conversation_history}

Current User Question:
{question}

Rules:

1. Use only the provided knowledge base context
   for company-specific information.

2. Do not invent or assume company-specific
   information.

3. Never use information from another company.

4. If the context does not contain enough
   information to answer the question, say:

"I couldn't find this information in the
provided knowledge base."

5. Give a clear and concise answer.

6. Use previous conversation only when it is
   relevant to the current question.

7. Do not mention that you are an AI unless
   necessary.

8. Do not add unrelated information.
"""


    # ========================================================
    # GENERAL QUESTION
    # ========================================================

    else:

        prompt = f"""
You are Placement AI Co-Pilot.

You help students with:

- DSA
- Programming
- Technical interviews
- Placement preparation
- Resume preparation
- Career guidance
- Computer Science subjects

Conversation History:
{conversation_history}

Current User Question:
{question}

Give a clear, practical and
beginner-friendly answer.

Use the previous conversation when it is
relevant to the current question.

For example, if the user previously told you
their name and later asks "What is my name?",
use the conversation history to answer.

Do not use company-specific information
because this is a general question.

Do not invent information that is not present
in the conversation history or current question.
"""


    # ========================================================
    # CALL GEMINI
    # ========================================================

    response = llm.invoke(
        [
            HumanMessage(
                content=prompt
            )
        ]
    )


    response_text = response.content


    # ========================================================
    # RETURN RESPONSE + MEMORY MESSAGE
    # ========================================================

    return {

        "response": response_text,

        "messages": [
            AIMessage(
                content=response_text
            )
        ]
    }


# ============================================================
# 10. CREATE GRAPH
# ============================================================

graph_builder = StateGraph(
    PlacementState
)


# ============================================================
# 11. ADD NODES
# ============================================================

graph_builder.add_node(
    "classifier",
    classify_question
)

graph_builder.add_node(
    "general",
    general_node
)

graph_builder.add_node(
    "company",
    company_node
)

graph_builder.add_node(
    "generate",
    generate_answer
)


# ============================================================
# 12. START → CLASSIFIER
# ============================================================

graph_builder.add_edge(
    START,
    "classifier"
)


# ============================================================
# 13. CONDITIONAL ROUTING
# ============================================================

graph_builder.add_conditional_edges(

    "classifier",

    route_question,

    {
        "general": "general",

        "company": "company"
    }
)


# ============================================================
# 14. GENERAL / COMPANY → GEMINI
# ============================================================

graph_builder.add_edge(
    "general",
    "generate"
)

graph_builder.add_edge(
    "company",
    "generate"
)


# ============================================================
# 15. GEMINI → END
# ============================================================

graph_builder.add_edge(
    "generate",
    END
)


# ============================================================
# 16. SQLITE CHECKPOINTER
# ============================================================

DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

CHECKPOINT_DB_PATH = DATABASE_DIR / "langgraph_checkpoints.db"

connection = sqlite3.connect(
    CHECKPOINT_DB_PATH,
    check_same_thread=False
)

checkpointer = SqliteSaver(
    connection
)


# ============================================================
# 17. COMPILE GRAPH
# ============================================================

graph = graph_builder.compile(
    checkpointer=checkpointer
)


