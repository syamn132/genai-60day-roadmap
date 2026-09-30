def build_context(
    results: list[dict],
) -> str:
    """
    Convert retrieved/compressed results into
    structured context for the generator.
    """

    if not results:
        return ""

    context_parts = []

    for source_number, result in enumerate(
        results,
        start=1,
    ):
        metadata = result["metadata"]

        source = metadata.get(
            "source",
            "unknown",
        )

        department = metadata.get(
            "department",
            "unknown",
        )

        chunk_id = result.get(
            "id",
            "unknown",
        )

        text = result["text"]

        context_part = (
            f"[Source {source_number}]\n"
            f"Document: {source}\n"
            f"Department: {department}\n"
            f"Chunk ID: {chunk_id}\n"
            f"Evidence:\n{text}"
        )

        context_parts.append(
            context_part
        )

    return "\n\n".join(
        context_parts
    )

def build_source_list(
    results: list[dict],
    max_sources: int = 1,
) -> list[str]:
    """
    Return unique source documents in ranked order.

    Only the strongest sources are exposed
    to the user.
    """

    sources = []

    for result in results:
        source = result[
            "metadata"
        ].get(
            "source",
            "unknown",
        )

        if source not in sources:
            sources.append(
                source
            )

        if len(sources) >= max_sources:
            break

    return sources