from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

VECTORSTORE_PATH = BASE_DIR / "vectorstore" / "tcs_faiss"


# --------------------------------------------------
# EMBEDDING MODEL
# --------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# LOAD FAISS DATABASE
# --------------------------------------------------

vectorstore = FAISS.load_local(
    str(VECTORSTORE_PATH),
    embeddings,
    allow_dangerous_deserialization=True
)


# --------------------------------------------------
# CREATE RETRIEVER
# --------------------------------------------------

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 3}
)


# --------------------------------------------------
# TEST RETRIEVAL
# --------------------------------------------------

if __name__ == "__main__":

    query = input("\n🔎 Ask a question: ")

    docs = retriever.invoke(query)

    print("\n" + "=" * 60)
    print("📚 RETRIEVED DOCUMENTS")
    print("=" * 60)

    for i, doc in enumerate(docs, start=1):

        print(f"\n--- Chunk {i} ---")

        print(doc.page_content)

        print("\nMetadata:")
        print(doc.metadata)