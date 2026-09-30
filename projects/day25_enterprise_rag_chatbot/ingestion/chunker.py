def split_into_paragraphs(text: str) -> list[str]:
    """
    Split document text into non-empty paragraphs.
    """

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    return paragraphs


def chunk_documents(
    documents: list[dict],
    max_chars: int = 500,
) -> list[dict]:
    """
    Convert loaded documents into smaller paragraph-aware chunks.

    Args:
        documents:
            List of loaded document dictionaries.

        max_chars:
            Approximate maximum size of each chunk in characters.

    Returns:
        List of chunk dictionaries with:
        - id
        - text
        - metadata
    """

    chunks = []

    for document in documents:
        paragraphs = split_into_paragraphs(
            document["text"]
        )

        current_chunk = []
        current_length = 0
        chunk_number = 1

        for paragraph in paragraphs:
            paragraph_length = len(paragraph)

            # +2 accounts approximately for "\n\n"
            separator_length = 2 if current_chunk else 0

            projected_length = (
                current_length
                + separator_length
                + paragraph_length
            )

            if current_chunk and projected_length > max_chars:
                chunk_text = "\n\n".join(current_chunk)

                source_name = document["metadata"]["source"]
                source_stem = source_name.rsplit(".", 1)[0]

                chunk_id = (
                    f"{source_stem}_chunk_{chunk_number:03d}"
                )

                chunks.append(
                    {
                        "id": chunk_id,
                        "text": chunk_text,
                        "metadata": {
                            **document["metadata"],
                            "chunk_number": chunk_number,
                        },
                    }
                )

                chunk_number += 1
                current_chunk = []
                current_length = 0

            if current_chunk:
                current_length += 2

            current_chunk.append(paragraph)
            current_length += paragraph_length

        # Save the final remaining chunk
        if current_chunk:
            chunk_text = "\n\n".join(current_chunk)

            source_name = document["metadata"]["source"]
            source_stem = source_name.rsplit(".", 1)[0]

            chunk_id = (
                f"{source_stem}_chunk_{chunk_number:03d}"
            )

            chunks.append(
                {
                    "id": chunk_id,
                    "text": chunk_text,
                    "metadata": {
                        **document["metadata"],
                        "chunk_number": chunk_number,
                    },
                }
            )

    return chunks