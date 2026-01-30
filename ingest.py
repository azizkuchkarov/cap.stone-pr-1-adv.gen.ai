import os
from rag.config import settings
from rag.loaders import load_documents
from rag.chunking import chunk_documents
from rag.vectorstore import FAISSStore

def main():
    os.makedirs(settings.PROCESSED_DIR, exist_ok=True)

    print(f"Loading documents from: {settings.RAW_DATA_DIR}")
    pages = load_documents(settings.RAW_DATA_DIR)
    if not pages:
        raise RuntimeError("No documents found in data/raw. Add PDFs/TXT/MD files first.")

    print(f"Loaded {len(pages)} page/text items. Chunking...")
    chunks = chunk_documents(pages, chunk_size=900, overlap=150)
    print(f"Created {len(chunks)} chunks.")

    store = FAISSStore(settings.EMBED_MODEL)
    print("Building FAISS index...")
    store.build(chunks)

    print("Saving...")
    store.save(settings.FAISS_INDEX_PATH, settings.DOCSTORE_PATH)
    print("Done.")
    print(f"Saved index to: {settings.FAISS_INDEX_PATH}")
    print(f"Saved docstore to: {settings.DOCSTORE_PATH}")

if __name__ == "__main__":
    main()
