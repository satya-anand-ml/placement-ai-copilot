from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# ==================================================
# PATHS
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

VECTORSTORE_PATH = (
    BASE_DIR
    / "vectorstore"
    / "placement_faiss"
)


# ==================================================
# CONFIGURATION
# ==================================================

TOP_K = 4

# Custom similarity threshold
# Score will always be between 0 and 1
RELEVANCE_THRESHOLD = 0.30


# ==================================================
# EMBEDDING MODEL
# ==================================================

print("🧠 Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("✅ Embedding model loaded")


# ==================================================
# LOAD FAISS DATABASE
# ==================================================

print("🗄️ Loading placement FAISS database...")

vectorstore = FAISS.load_local(
    str(VECTORSTORE_PATH),
    embeddings,
    allow_dangerous_deserialization=True
)

print("✅ FAISS database loaded")


# ==================================================
# RETRIEVE DOCUMENTS
# ==================================================

def retrieve_documents(
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
        Example:
            "tcs"
            "infosys"
            "accenture"

    Returns
    -------
    list
        List of:
        (Document, similarity_score)
    """

    # ------------------------------------------------
    # NORMALIZE COMPANY NAME
    # ------------------------------------------------

    if company:
        company = company.strip().lower()

    # ------------------------------------------------
    # FAISS SEARCH
    # ------------------------------------------------

    if company:

        results = vectorstore.similarity_search_with_score(
            question,
            k=TOP_K,
            filter={
                "company": company
            }
        )

    else:

        results = vectorstore.similarity_search_with_score(
            question,
            k=TOP_K
        )

    # ------------------------------------------------
    # DISTANCE → SIMILARITY SCORE
    # ------------------------------------------------

    processed_results = []

    for doc, distance in results:

        # FAISS returns L2 distance.
        #
        # Convert it into a simple 0–1 score:
        #
        # smaller distance = better match
        # higher score = better match

        similarity_score = (
            1 / (1 + float(distance))
        )

        # ------------------------------------------------
        # RELEVANCE FILTER
        # ------------------------------------------------

        if similarity_score >= RELEVANCE_THRESHOLD:

            processed_results.append(
                (
                    doc,
                    similarity_score
                )
            )

    return processed_results


# ==================================================
# TEST RETRIEVAL
# ==================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("🚀 PLACEMENT AI CO-PILOT — RETRIEVER TEST")
    print("=" * 60)

    # ------------------------------------------------
    # USER QUERY
    # ------------------------------------------------

    query = input(
        "\n🔎 Ask a question: "
    )

    # ------------------------------------------------
    # OPTIONAL COMPANY FILTER
    # ------------------------------------------------

    company_input = input(
        "🏢 Company filter "
        "(optional, e.g. tcs): "
    ).strip()

    if company_input == "":
        company_input = None

    # ------------------------------------------------
    # RETRIEVE
    # ------------------------------------------------

    results = retrieve_documents(
        query,
        company_input
    )

    # ------------------------------------------------
    # DISPLAY RESULTS
    # ------------------------------------------------

    print("\n" + "=" * 60)
    print("📚 RETRIEVED DOCUMENTS")
    print("=" * 60)

    if not results:

        print(
            "\n❌ No sufficiently relevant "
            "documents found."
        )

    else:

        for i, (doc, score) in enumerate(
            results,
            start=1
        ):

            print(
                f"\n--- Chunk {i} ---"
            )

            print(
                f"Similarity Score: {score:.4f}"
            )

            print(
                f"Company: "
                f"{doc.metadata.get('company', 'unknown')}"
            )

            print(
                f"Source: "
                f"{doc.metadata.get('source_file', 'unknown')}"
            )

            print(
                f"Page: "
                f"{doc.metadata.get('page', 'unknown')}"
            )

            print("\nContent:")

            print(
                doc.page_content
            )

            print("\nMetadata:")

            print(
                doc.metadata
            )