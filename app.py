import streamlit as st
from dotenv import load_dotenv

from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage
)

from rag.rag_chain import (
    get_relevant_documents,
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

The knowledge base contains company-specific placement
reference documents.

1. For company-specific questions, use the provided
   Knowledge Base Context when relevant information is available.

2. Never use information from one company to answer a question
   about another company.

3. If a company-specific question is asked but the required
   information is not present in the Knowledge Base Context,
   say:

   "I couldn't find this information in the provided
   knowledge base."

4. Do not invent company-specific information.

5. Do not use general knowledge to fill a missing
   company-specific answer.

6. For completely general questions such as:
   - DSA
   - Programming
   - Binary Search
   - Dynamic Programming
   - OOP
   - DBMS
   - OS
   - Computer Science concepts

   answer normally using your general knowledge.

7. For general questions, do not claim that the answer
   came from the knowledge base.

8. Use retrieved company information only when it is actually
   present in the Knowledge Base Context.
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
    # COMPANY DETECTION
    # ----------------------------------------------

    company = None

    company_keywords = {
        "tcs": "tcs",
        "infosys": "infosys",
        "accenture": "accenture",
        "capgemini": "capgemini",
        "cognizant": "cognizant",
        "wipro": "wipro",
        "deloitte": "deloitte",
        "hcl": "hcltech",
        "hcltech": "hcltech",
        "ltimindtree": "ltimindtree",
        "tech mahindra": "techmahindra",
        "techmahindra": "techmahindra"
    }

    user_input_lower = user_input.lower()

    for keyword, company_name in company_keywords.items():

        if keyword in user_input_lower:

            company = company_name
            break


    # ----------------------------------------------
    # RETRIEVE DOCUMENTS
    # ----------------------------------------------

    # IMPORTANT:
    # RAG is used ONLY for company-specific questions.
    #
    # General questions like:
    # "What is Binary Search?"
    # "Explain OOP"
    # "What is DP?"
    #
    # will NOT search the company knowledge base.

    if company:

        relevant_docs = get_relevant_documents(
            question=user_input,
            company=company
        )

    else:

        relevant_docs = []


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
                    "No relevant company-specific "
                    "information was found in the "
                    "knowledge base."
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

        with st.spinner(
            "🔎 Searching knowledge base..."
            if company
            else
            "🤖 Thinking..."
        ):

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

                    company_name = doc.metadata.get(
                        "company",
                        "Unknown"
                    )

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

🏢 **Company:** `{company_name}`

📄 **Document:** `{source_name}`

📑 **Page:** `{page}`

🎯 **Similarity:** `{score:.2f}`
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