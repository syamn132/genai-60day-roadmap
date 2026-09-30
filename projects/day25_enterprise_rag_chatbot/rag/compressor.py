import re

import numpy as np


def split_sentences(
    text: str,
) -> list[str]:
    """
    Lightweight sentence splitter.
    """

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip(),
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def compress_text(
    query: str,
    text: str,
    embedding_model,
    top_sentences: int = 2,
) -> str:
    """
    Extract the sentences most semantically
    related to the query.

    This is extractive compression.
    """

    sentences = split_sentences(
        text
    )

    if len(sentences) <= top_sentences:
        return text

    query_vector = (
        embedding_model
        .encode([query])[0]
    )

    sentence_vectors = (
        embedding_model
        .encode(sentences)
    )

    scores = np.dot(
        sentence_vectors,
        query_vector,
    )

    ranked_indices = np.argsort(
        scores
    )[::-1]

    selected_indices = ranked_indices[
        :top_sentences
    ]

    # Restore original document order
    selected_indices = sorted(
        selected_indices.tolist()
    )

    selected_sentences = [
        sentences[index]
        for index in selected_indices
    ]

    return " ".join(
        selected_sentences
    )


def compress_results(
    query: str,
    results: list[dict],
    embedding_model,
    top_sentences: int = 2,
) -> list[dict]:
    """
    Compress each retrieved chunk while
    preserving metadata and scores.
    """

    compressed = []

    for result in results:
        new_result = dict(result)

        new_result["original_text"] = (
            result["text"]
        )

        new_result["text"] = compress_text(
            query=query,
            text=result["text"],
            embedding_model=embedding_model,
            top_sentences=top_sentences,
        )

        compressed.append(
            new_result
        )

    return compressed