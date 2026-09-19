import streamlit as st
from dotenv import load_dotenv

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

from rag.rag_chain import (
    retrieve_documents,
    build_context,
    llm
)


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Placement AI Co-Pilot",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# SYSTEM PROMPT
# --------------------------------------------------

SYSTEM_PROMPT = """
You are Placement AI Co-Pilot, a helpful AI assistant.

Your main purpose is to help students with:
- DSA
- Programming
- Technical interviews
- Placement preparation
- Resume preparation
- Career guidance
- Computer Science subjects

You have access to the conversation history.

Use previous messages when they are relevant to the user's
current question.

If the user tells you their name or useful information during
the conversation, remember it and use it naturally in later
responses.

Do not claim to remember information that is not present in
the conversation history.

Give clear, practical and beginner-friendly answers.


RAG RULES:

The current knowledge base contains information from the
TCS All India NQT 2026 reference document.

Follow these rules strictly:

1. If the user's question is about TCS or information covered
   by the knowledge base, use the provided Knowledge Base
   Context.

2. Never use TCS information to answer questions about another
   company such as Infosys, Accenture, Wipro, Cognizant,
   Capgemini, etc.

3. If the user asks about a company or topic that is not covered
   by the Knowledge Base Context, do not invent or provide
   unsupported company-specific information.

4. For unsupported knowledge-base questions, say:
   "I couldn't find this information in the provided knowledge base."

5. Do not use general knowledge to fill a missing company-specific
   answer.

6. For completely general questions such as DSA, programming,
   interview concepts, or computer science topics, you may answer
   normally using your general knowledge.

7. Never claim that information came from the knowledge base
   unless it is actually present in the provided context.
"""



# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


if "chat_history" not in st.session_state:

    st.session_state.chat_history = []


# --------------------------------------------------
# NEW CHAT
# --------------------------------------------------

def new_chat():

    if st.session_state.messages:

        st.session_state.chat_history.append(
            st.session_state.messages.copy()
        )

    st.session_state.messages = []


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🤖 Placement AI")

    st.divider()

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):

        new_chat()
        st.rerun()

    st.divider()

    st.subheader("💬 Current Chat")

    if not st.session_state.messages:

        st.caption("No messages yet.")

    else:

        for message in st.session_state.messages:

            if message["role"] == "user":

                st.write(
                    "👤 "
                    + message["content"][:40]
                )

    st.divider()

    st.subheader("📚 Features")

    st.write("✅ AI Chatbot")
    st.write("✅ Conversation Memory")
    st.write("✅ RAG + FAISS")
    st.write("✅ Source Information")
    st.write("⚡ Streaming Responses")
    st.write("⏳ LangGraph")
    st.write("⏳ Multi-Agent")
    st.write("⏳ HITL")
    st.write("⏳ MCP")


# --------------------------------------------------
# MAIN PAGE
# --------------------------------------------------

st.title("🤖 Placement AI Co-Pilot")

st.caption(
    "Your AI companion for placements, DSA, interviews, "
    "resume and career guidance."
)


# --------------------------------------------------
# DISPLAY CHAT
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(
            message["content"]
        )


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

user_input = st.chat_input(
    "Ask me anything..."
)


# --------------------------------------------------
# PROCESS QUESTION
# --------------------------------------------------

if user_input:

    # ----------------------------------------------
    # USER MESSAGE
    # ----------------------------------------------

    with st.chat_message("user"):

        st.markdown(user_input)


    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # ----------------------------------------------
    # RETRIEVE DOCUMENTS
    # ----------------------------------------------

    relevant_docs = retrieve_documents(
        user_input
    )


    # ----------------------------------------------
    # BUILD CONTEXT
    # ----------------------------------------------

    context = build_context(
        relevant_docs
    )


    # ----------------------------------------------
    # BUILD CONVERSATION
    # ----------------------------------------------

    conversation = [

        SystemMessage(
            content=(
                SYSTEM_PROMPT
                + "\n\n"
                + "================================\n"
                + "KNOWLEDGE BASE CONTEXT\n"
                + "================================\n"
                + (
                    context
                    if context
                    else
                    "No relevant information was found "
                    "in the knowledge base."
                )
            )
        )
    ]


    # ----------------------------------------------
    # PREVIOUS CONVERSATION
    # ----------------------------------------------

    for message in st.session_state.messages[:-1]:

        if message["role"] == "user":

            conversation.append(
                HumanMessage(
                    content=message["content"]
                )
            )

        elif message["role"] == "assistant":

            conversation.append(
                AIMessage(
                    content=message["content"]
                )
            )


    # ----------------------------------------------
    # CURRENT QUESTION
    # ----------------------------------------------

    conversation.append(
        HumanMessage(
            content=user_input
        )
    )


    # ----------------------------------------------
    # ASSISTANT RESPONSE
    # ----------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("🔎 Searching knowledge base..."):

            # --------------------------------------
            # STREAMING RESPONSE
            # --------------------------------------

            def generate_response():

                for chunk in llm.stream(
                    conversation
                ):

                    if chunk.content:

                        yield chunk.content


            assistant_response = st.write_stream(
                generate_response()
            )


        # ------------------------------------------
        # SOURCES
        # ------------------------------------------

        if relevant_docs:

            with st.expander(
                "📚 Sources used"
            ):

                for index, item in enumerate(
                    relevant_docs,
                    start=1
                ):

                    doc = item["document"]

                    score = item["score"]

                    source = doc.metadata.get(
                        "source",
                        "Unknown source"
                    )

                    page = doc.metadata.get(
                        "page_label",
                        doc.metadata.get(
                            "page",
                            "Unknown"
                        )
                    )

                    source_name = (
                        source.split("\\")[-1]
                    )

                    st.markdown(
                        f"""
**Source {index}**

📄 **Document:** `{source_name}`

📑 **Page:** `{page}`

🎯 **Relevance:** `{score:.2f}`
"""
                    )


    # ----------------------------------------------
    # SAVE RESPONSE
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )