from config import (
    CHUNK_MAX_CHARS,
    DATA_DIR,
)

from embeddings import EmbeddingModel

from ingestion.chunker import (
    chunk_documents,
)

from ingestion.indexer import (
    build_faiss_index,
)

from ingestion.loader import (
    load_documents,
)


def main():
    print("=" * 70)
    print("ENTERPRISE RAG — INDEX BUILD")
    print("=" * 70)

    # --------------------------------------------------
    # Load documents
    # --------------------------------------------------

    documents = load_documents(
        DATA_DIR
    )

    print(
        f"\nDocuments loaded: "
        f"{len(documents)}"
    )

    # --------------------------------------------------
    # Chunk documents
    # --------------------------------------------------

    chunks = chunk_documents(
        documents,
        max_chars=CHUNK_MAX_CHARS,
    )

    print(
        f"Chunks created: "
        f"{len(chunks)}"
    )

    # --------------------------------------------------
    # Load embedding model
    # --------------------------------------------------

    embedding_model = EmbeddingModel()

    # --------------------------------------------------
    # Build and persist vector index
    # --------------------------------------------------

    build_faiss_index(
        chunks,
        embedding_model,
    )

    print("\n")
    print("=" * 70)
    print("INDEX BUILD COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()