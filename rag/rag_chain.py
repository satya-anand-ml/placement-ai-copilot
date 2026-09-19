from pathlib import Path
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

VECTORSTORE_PATH = (
    BASE_DIR
    / "vectorstore"
    / "tcs_faiss"
)


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

load_dotenv(BASE_DIR / ".env")


# --------------------------------------------------
# EMBEDDINGS
# --------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# LOAD FAISS VECTOR DATABASE
# --------------------------------------------------

vectorstore = FAISS.load_local(
    str(VECTORSTORE_PATH),
    embeddings,
    allow_dangerous_deserialization=True
)


# --------------------------------------------------
# GEMINI
# --------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)


# --------------------------------------------------
# RETRIEVAL SETTINGS
# --------------------------------------------------

TOP_K = 4

RELEVANCE_THRESHOLD = 0.35



# --------------------------------------------------
# RETRIEVE RELEVANT DOCUMENTS
# --------------------------------------------------

def retrieve_documents(question: str):

    results = vectorstore.similarity_search_with_relevance_scores(
        question,
        k=TOP_K
    )

    relevant_docs = []

    for doc, score in results:

        if score >= RELEVANCE_THRESHOLD:

            relevant_docs.append(
                {
                    "document": doc,
                    "score": score
                }
            )

    return relevant_docs


# --------------------------------------------------
# CREATE CONTEXT
# --------------------------------------------------

def build_context(relevant_docs):

    if not relevant_docs:
        return ""

    context_parts = []

    for item in relevant_docs:

        doc = item["document"]

        context_parts.append(
            doc.page_content
        )

    return "\n\n".join(context_parts)