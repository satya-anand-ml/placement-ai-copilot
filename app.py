import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Load environment variables
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
# LLM
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
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

Use previous messages when they are relevant to the user's current question.

If the user tells you their name or some useful information during the
conversation, remember it and use it naturally in later responses.

Do not claim to remember information that is not present in the
conversation history.

Give clear, practical and beginner-friendly answers.
"""


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

# Store current conversation
if "messages" not in st.session_state:
    st.session_state.messages = []


# Store chat history / conversations
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# --------------------------------------------------
# NEW CHAT FUNCTION
# --------------------------------------------------

def new_chat():

    # Save current conversation before starting new one
    if st.session_state.messages:

        st.session_state.chat_history.append(
            st.session_state.messages.copy()
        )

    # Clear current conversation
    st.session_state.messages = []


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🤖 Placement AI")

    st.divider()

    # New Chat Button
    if st.button(
        "➕ New Chat",
        use_container_width=True
    ):
        new_chat()
        st.rerun()

    st.divider()

    st.subheader("💬 Current Chat")

    if len(st.session_state.messages) == 0:

        st.caption("No messages yet.")

    else:

        for message in st.session_state.messages:

            if message["role"] == "user":

                st.write(
                    "👤 " + message["content"][:40]
                )

    st.divider()

    st.subheader("📚 Features")

    st.write("✅ AI Chatbot")
    st.write("✅ Conversation Memory")
    st.write("⏳ RAG")
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
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

user_input = st.chat_input(
    "Ask me anything..."
)


if user_input:

    # ----------------------------------------------
    # Display User Message
    # ----------------------------------------------

    with st.chat_message("user"):

        st.markdown(user_input)


    # ----------------------------------------------
    # Save User Message
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )


    # ----------------------------------------------
    # Convert History into LangChain Messages
    # ----------------------------------------------

    conversation = [
        SystemMessage(content=SYSTEM_PROMPT)
    ]


    for message in st.session_state.messages:

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
    # Get AI Response
    # ----------------------------------------------

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = llm.invoke(
                conversation
            )

            assistant_response = response.content

        st.markdown(assistant_response)


    # ----------------------------------------------
    # Save AI Response
    # ----------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )