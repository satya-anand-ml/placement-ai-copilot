import streamlit as st

from langchain_core.messages import HumanMessage

from langgraph.placement_graph import graph

from chat_db import (
    init_db,
    create_chat,
    save_message,
    get_chats,
    get_chat_messages,
    delete_chat
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Placement AI Co-Pilot",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

init_db()


# ============================================================
# SESSION STATE
# ============================================================

if "thread_id" not in st.session_state:

    st.session_state.thread_id = create_chat()


if "messages" not in st.session_state:

    st.session_state.messages = []


# ============================================================
# NEW CHAT
# ============================================================

def new_chat():

    # Clear current UI messages
    st.session_state.messages = []

    # Create new SQLite chat + new thread
    st.session_state.thread_id = create_chat()


# ============================================================
# LOAD EXISTING CHAT
# ============================================================

def load_chat(thread_id):

    # Change current thread
    st.session_state.thread_id = thread_id

    # Load messages from SQLite
    saved_messages = get_chat_messages(
        thread_id
    )

    # Load them into Streamlit UI
    st.session_state.messages = saved_messages


# ============================================================
# DELETE EXISTING CHAT
# ============================================================

def remove_chat(thread_id):

    # Delete chat and its messages
    delete_chat(
        thread_id
    )

    # If currently opened chat was deleted
    if thread_id == st.session_state.thread_id:

        # Create a fresh chat
        st.session_state.thread_id = create_chat()

        # Clear UI messages
        st.session_state.messages = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 Placement AI")

    st.divider()


    # ========================================================
    # NEW CHAT BUTTON
    # ========================================================

    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):

        new_chat()

        st.rerun()


    st.divider()


    # ========================================================
    # CHAT HISTORY
    # ========================================================

    st.subheader("🗂️ Chat History")

    chats = get_chats(
        limit=20
    )


    if not chats:

        st.caption(
            "No previous chats."
        )

    else:

        for chat in chats:

            thread_id = chat["thread_id"]

            chat_title = chat["title"]


            if len(chat_title) > 30:

                chat_title = (
                    chat_title[:30]
                    + "..."
                )


            # ------------------------------------------------
            # Check current chat
            # ------------------------------------------------

            is_current_chat = (
                thread_id
                ==
                st.session_state.thread_id
            )


            # ------------------------------------------------
            # Chat + Delete buttons
            # ------------------------------------------------

            col1, col2 = st.columns(
                [5, 1]
            )


            # ------------------------------------------------
            # OPEN CHAT
            # ------------------------------------------------

            with col1:

                button_label = (
                    "🟢 "
                    if is_current_chat
                    else "💬 "
                ) + chat_title


                if st.button(
                    button_label,
                    key=f"chat_{thread_id}",
                    use_container_width=True
                ):

                    load_chat(
                        thread_id
                    )

                    st.rerun()


            # ------------------------------------------------
            # DELETE CHAT
            # ------------------------------------------------

            with col2:

                if st.button(
                    "🗑️",
                    key=f"delete_{thread_id}",
                    help="Delete this chat"
                ):

                    remove_chat(
                        thread_id
                    )

                    st.rerun()


    st.divider()


    # ========================================================
    # CURRENT CHAT
    # ========================================================

    st.subheader("💬 Current Chat")


    if not st.session_state.messages:

        st.caption(
            "No messages yet."
        )

    else:

        for message in (
            st.session_state.messages
        ):

            if message["role"] == "user":

                st.write(
                    "👤 "
                    + message["content"][:40]
                )


    st.divider()


    # ========================================================
    # THREAD ID
    # ========================================================

    st.subheader("🧵 Current Thread")

    st.code(
        st.session_state.thread_id
    )


    st.divider()


    # ========================================================
    # FEATURES
    # ========================================================

    st.subheader("📚 Features")

    st.write("✅ AI Chatbot")
    st.write("✅ Conversation Memory")
    st.write("✅ RAG + FAISS")
    st.write("✅ Multi-Company RAG")
    st.write("✅ Source Information")
    st.write("⚡ LangGraph")
    st.write("✅ Thread ID")
    st.write("✅ SQLite Checkpoint")
    st.write("✅ Persistent Chat History")
    st.write("⏳ Multi-Agent")
    st.write("⏳ HITL")
    st.write("⏳ MCP")


# ============================================================
# MAIN PAGE
# ============================================================

st.title(
    "🤖 Placement AI Co-Pilot"
)

st.caption(
    "Your AI companion for placements, DSA, interviews, "
    "resume and career guidance."
)


# ============================================================
# DISPLAY CURRENT CHAT
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# USER INPUT
# ============================================================

user_input = st.chat_input(
    "Ask me anything..."
)


# ============================================================
# PROCESS QUESTION
# ============================================================

if user_input:


    # ========================================================
    # USER MESSAGE
    # ========================================================

    with st.chat_message("user"):

        st.markdown(
            user_input
        )


    # ========================================================
    # SAVE USER MESSAGE TO UI
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # ========================================================
    # SAVE USER MESSAGE TO SQLITE
    # ========================================================

    save_message(
        st.session_state.thread_id,
        "user",
        user_input
    )


    # ========================================================
    # LANGGRAPH STATE
    # ========================================================

    initial_state = {

        "messages": [

            HumanMessage(
                content=user_input
            )

        ],

        "question": user_input,

        "company": "",

        "question_type": "",

        "context": "",

        "sources": [],

        "response": ""
    }


    # ========================================================
    # LANGGRAPH CONFIG
    # ========================================================

    config = {

        "configurable": {

            "thread_id":
                st.session_state.thread_id

        }

    }


    # ========================================================
    # RUN LANGGRAPH
    # ========================================================

    with st.chat_message("assistant"):

        with st.spinner(
            "🤖 Placement AI is thinking..."
        ):

            result = graph.invoke(
                initial_state,
                config=config
            )


        # ====================================================
        # GET RESPONSE
        # ====================================================

        assistant_response = result[
            "response"
        ]


        # ====================================================
        # DISPLAY RESPONSE
        # ====================================================

        st.markdown(
            assistant_response
        )


        # ====================================================
        # SOURCES
        # ====================================================

        sources = result.get(
            "sources",
            []
        )


        if sources:

            with st.expander(
                "📚 Sources used"
            ):

                for index, source in enumerate(
                    sources,
                    start=1
                ):

                    company_name = source.get(
                        "company",
                        "Unknown"
                    )

                    source_file = source.get(
                        "source_file",
                        "Unknown"
                    )

                    page = source.get(
                        "page",
                        "Unknown"
                    )

                    score = source.get(
                        "score",
                        0
                    )


                    st.markdown(
                        f"""
**Source {index}**

🏢 **Company:** `{company_name}`

📄 **Document:** `{source_file}`

📑 **Page:** `{page}`

🎯 **Similarity:** `{score:.2f}`
"""
                    )


        # ====================================================
        # LANGGRAPH EXECUTION
        # ====================================================

        with st.expander(
            "🔎 LangGraph Execution"
        ):

            company = result.get(
                "company",
                ""
            )

            question_type = result.get(
                "question_type",
                ""
            )

            context = result.get(
                "context",
                ""
            )


            st.write(
                "🧵 Thread ID:",
                st.session_state.thread_id
            )


            st.write(
                "🏢 Company:",
                company
                if company
                else
                "None"
            )


            st.write(
                "📌 Question Type:",
                question_type
            )


            if context:

                st.write(
                    "📚 RAG Context Retrieved: ✅"
                )

            else:

                st.write(
                    "📚 RAG Context Retrieved: ❌"
                )


    # ========================================================
    # SAVE ASSISTANT MESSAGE TO UI
    # ========================================================

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )


    # ========================================================
    # SAVE ASSISTANT MESSAGE TO SQLITE
    # ========================================================

    save_message(
        st.session_state.thread_id,
        "assistant",
        assistant_response
    )