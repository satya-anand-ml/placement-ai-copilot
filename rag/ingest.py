from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# --------------------------------------------------
# PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_PATH = BASE_DIR / "documents" / "TCS_All_India_NQT_2026_RAG_Reference.pdf"

VECTORSTORE_PATH = BASE_DIR / "vectorstore" / "tcs_faiss"


# --------------------------------------------------
# 1. LOAD PDF
# --------------------------------------------------

print("📄 Loading PDF...")

loader = PyPDFLoader(str(PDF_PATH))

documents = loader.load()

print(f"✅ Loaded {len(documents)} pages")


# --------------------------------------------------
# 2. SPLIT DOCUMENT INTO CHUNKS
# --------------------------------------------------

print("✂️ Splitting document into chunks...")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
)

chunks = text_splitter.split_documents(documents)

print(f"✅ Created {len(chunks)} chunks")


# --------------------------------------------------
# 3. CREATE EMBEDDINGS
# --------------------------------------------------

print("🧠 Creating embeddings...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("✅ Embedding model loaded")


# --------------------------------------------------
# 4. CREATE FAISS VECTOR DATABASE
# --------------------------------------------------

print("🗄️ Creating FAISS vector database...")

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)


# --------------------------------------------------
# 5. SAVE VECTOR DATABASE
# --------------------------------------------------

VECTORSTORE_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

vectorstore.save_local(
    str(VECTORSTORE_PATH)
)

print("✅ FAISS vector database created successfully!")

print(f"📁 Saved at: {VECTORSTORE_PATH}")