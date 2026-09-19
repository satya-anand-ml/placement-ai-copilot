from pathlib import Path
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from rag.retriever import retrieve_documents


# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

load_dotenv(BASE_DIR / ".env")


# ==================================================
# GEMINI
# ==================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)


# ==================================================
# RETRIEVE RELEVANT DOCUMENTS
# ==================================================

def get_relevant_documents(
    question: str,
    company: str | None = None
):
    """
    Retrieve relevant documents from the
    multi-company placement knowledge base.

    Parameters
    ----------
    question : str
        User's question.

    company : str | None
        Optional company filter.

    Returns
    -------
    list
        List containing:
        {
            "document": Document,
            "score": float
        }
    """

    results = retrieve_documents(
        question=question,
        company=company
    )

    relevant_docs = []

    for doc, score in results:

        relevant_docs.append(
            {
                "document": doc,
                "score": score
            }
        )

    return relevant_docs


# ==================================================
# CREATE RAG CONTEXT
# ==================================================

def build_context(
    relevant_docs
):
    """
    Convert retrieved documents into
    a context string for Gemini.
    """

    if not relevant_docs:
        return ""

    context_parts = []

    for item in relevant_docs:

        doc = item["document"]

        context_parts.append(
            doc.page_content
        )

    return "\n\n".join(
        context_parts
    )


# ==================================================
# BUILD SOURCE INFORMATION
# ==================================================

def get_sources(
    relevant_docs
):
    """
    Extract source information from
    retrieved documents.
    """

    sources = []

    for item in relevant_docs:

        doc = item["document"]
        score = item["score"]

        sources.append(
            {
                "company": doc.metadata.get(
                    "company",
                    "Unknown"
                ),
                "source_file": doc.metadata.get(
                    "source_file",
                    "Unknown"
                ),
                "source_path": doc.metadata.get(
                    "source_path",
                    "Unknown"
                ),
                "page": doc.metadata.get(
                    "page",
                    "Unknown"
                ),
                "score": score
            }
        )

    return sources


# ==================================================
# TEST RAG RETRIEVAL
# ==================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("🚀 PLACEMENT AI CO-PILOT — RAG CHAIN TEST")
    print("=" * 60)

    question = input(
        "\n🔎 Ask a question: "
    )

    company = input(
        "🏢 Company filter "
        "(optional, e.g. tcs): "
    ).strip()

    if company == "":
        company = None

    # ------------------------------------------------
    # RETRIEVE
    # ------------------------------------------------

    relevant_docs = get_relevant_documents(
        question,
        company
    )

    # ------------------------------------------------
    # CONTEXT
    # ------------------------------------------------

    context = build_context(
        relevant_docs
    )

    # ------------------------------------------------
    # DISPLAY
    # ------------------------------------------------

    print("\n" + "=" * 60)
    print("📚 RETRIEVED CONTEXT")
    print("=" * 60)

    if not context:

        print(
            "\n❌ No relevant context found."
        )

    else:

        print(context)

    # ------------------------------------------------
    # SOURCES
    # ------------------------------------------------

    print("\n" + "=" * 60)
    print("📌 SOURCES")
    print("=" * 60)

    sources = get_sources(
        relevant_docs
    )

    if not sources:

        print("\n❌ No sources found.")

    else:

        for i, source in enumerate(
            sources,
            start=1
        ):

            print(
                f"\nSource {i}"
            )

            print(
                f"Company : {source['company']}"
            )

            print(
                f"File    : {source['source_file']}"
            )

            print(
                f"Page    : {source['page']}"
            )

            print(
                f"Score   : {source['score']:.4f}"
            )