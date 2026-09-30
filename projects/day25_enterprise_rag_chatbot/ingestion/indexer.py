import json

import faiss
import numpy as np

from config import (
    CHUNKS_PATH,
    FAISS_INDEX_PATH,
    STORAGE_DIR,
)


def build_faiss_index(
    chunks: list[dict],
    embedding_model,
):
    """
    Generate embeddings for chunks and build
    a FAISS inner-product index.
    """

    if not chunks:
        raise ValueError(
            "Cannot build index: no chunks provided."
        )

    STORAGE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print(
        f"\nGenerating embeddings for "
        f"{len(texts)} chunks..."
    )

    embeddings = embedding_model.encode(
        texts
    )

    print(
        "Embedding matrix shape:",
        embeddings.shape,
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        np.ascontiguousarray(
            embeddings,
            dtype="float32",
        )
    )

    print(
        "Vectors stored in FAISS:",
        index.ntotal,
    )

    faiss.write_index(
        index,
        str(FAISS_INDEX_PATH),
    )

    with CHUNKS_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            chunks,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"FAISS index saved to: "
        f"{FAISS_INDEX_PATH}"
    )

    print(
        f"Chunk mapping saved to: "
        f"{CHUNKS_PATH}"
    )

    return index