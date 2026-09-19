from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DOCUMENTS_PATH = BASE_DIR / "documents"

VECTORSTORE_PATH = BASE_DIR / "vectorstore" / "placement_faiss"


# --------------------------------------------------
# 1. FIND COMPANY DOCUMENTS
# --------------------------------------------------

print("=" * 60)
print("🚀 PLACEMENT AI CO-PILOT — RAG INGESTION")
print("=" * 60)

print("\n📂 Scanning company documents...")

all_documents = []

pdf_files = list(
    DOCUMENTS_PATH.rglob("*.pdf")
)

if not pdf_files:

    print("❌ No PDF files found inside documents/")

    raise SystemExit


print(f"📄 Found {len(pdf_files)} PDF file(s)")


# --------------------------------------------------
# 2. LOAD ALL PDFs
# --------------------------------------------------

for pdf_path in pdf_files:

    # ----------------------------------------------
    # Company name from folder name
    # ----------------------------------------------

    company = pdf_path.parent.name.lower()

    print("\n" + "-" * 60)

    print(f"🏢 Company : {company}")
    print(f"📄 PDF     : {pdf_path.name}")

    # ----------------------------------------------
    # Load PDF
    # ----------------------------------------------

    loader = PyPDFLoader(
        str(pdf_path)
    )

    documents = loader.load()

    print(
        f"✅ Loaded {len(documents)} page(s)"
    )


    # ----------------------------------------------
    # Add metadata
    # ----------------------------------------------

    for document in documents:

        document.metadata["company"] = company

        document.metadata["source_file"] = (
            pdf_path.name
        )

        document.metadata["source_path"] = (
            str(pdf_path.relative_to(BASE_DIR))
        )


    all_documents.extend(
        documents
    )


# --------------------------------------------------
# 3. SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)

print(
    f"📚 Total pages loaded: {len(all_documents)}"
)


# --------------------------------------------------
# 4. SPLIT DOCUMENTS
# --------------------------------------------------

print("\n✂️ Splitting documents into chunks...")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

chunks = text_splitter.split_documents(
    all_documents
)

print(
    f"✅ Created {len(chunks)} chunks"
)


# --------------------------------------------------
# 5. CREATE EMBEDDINGS
# --------------------------------------------------

print("\n🧠 Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("✅ Embedding model loaded")


# --------------------------------------------------
# 6. CREATE FAISS DATABASE
# --------------------------------------------------

print("\n🗄️ Creating FAISS vector database...")

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)


# --------------------------------------------------
# 7. SAVE VECTOR DATABASE
# --------------------------------------------------

VECTORSTORE_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

vectorstore.save_local(
    str(VECTORSTORE_PATH)
)


# --------------------------------------------------
# 8. FINAL SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)

print(
    "✅ MULTI-COMPANY FAISS DATABASE CREATED!"
)

print(
    f"📁 Saved at: {VECTORSTORE_PATH}"
)

print(
    f"📄 Total pages: {len(all_documents)}"
)

print(
    f"🧩 Total chunks: {len(chunks)}"
)

print("=" * 60)