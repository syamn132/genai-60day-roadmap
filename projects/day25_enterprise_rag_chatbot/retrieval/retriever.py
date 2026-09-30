import json

import faiss
import numpy as np

from config import (
    CHUNKS_PATH,
    FAISS_INDEX_PATH,
)


class Retriever:
    """
    Semantic retriever backed by FAISS.
    """

    def __init__(
        self,
        embedding_model,
    ):
        self.embedding_model = embedding_model

        if not FAISS_INDEX_PATH.exists():
            raise FileNotFoundError(
                "FAISS index does not exist. "
                "Build the index first."
            )

        if not CHUNKS_PATH.exists():
            raise FileNotFoundError(
                "Chunk mapping does not exist."
            )

        self.index = faiss.read_index(
            str(FAISS_INDEX_PATH)
        )

        with CHUNKS_PATH.open(
            "r",
            encoding="utf-8",
        ) as file:
            self.chunks = json.load(file)

    def search(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """
        Search a single query.
        """

        query_embedding = (
            self.embedding_model
            .encode([query])
        )

        query_embedding = np.ascontiguousarray(
            query_embedding,
            dtype="float32",
        )

        k = min(
            top_k,
            self.index.ntotal,
        )

        scores, indices = self.index.search(
            query_embedding,
            k,
        )

        results = []

        for rank, (
            score,
            index_position,
        ) in enumerate(
            zip(
                scores[0],
                indices[0],
            ),
            start=1,
        ):
            if index_position < 0:
                continue

            chunk = self.chunks[
                int(index_position)
            ]

            results.append(
                {
                    "rank": rank,
                    "score": float(score),
                    "index_position": int(
                        index_position
                    ),
                    "id": chunk["id"],
                    "text": chunk["text"],
                    "metadata": chunk["metadata"],
                }
            )

        return results

    def multi_query_search(
        self,
        queries: list[str],
        top_k: int = 5,
    ) -> list[dict]:
        """
        Retrieve results for multiple query variants
        and merge duplicates.

        For duplicate chunks, keep the highest
        semantic similarity score.
        """

        merged = {}

        for query in queries:
            results = self.search(
                query,
                top_k=top_k,
            )

            for result in results:
                chunk_id = result["id"]

                if (
                    chunk_id not in merged
                    or result["score"]
                    > merged[chunk_id]["score"]
                ):
                    merged[chunk_id] = result

        combined_results = list(
            merged.values()
        )

        combined_results.sort(
            key=lambda item: item["score"],
            reverse=True,
        )

        for rank, result in enumerate(
            combined_results,
            start=1,
        ):
            result["rank"] = rank

        return combined_results