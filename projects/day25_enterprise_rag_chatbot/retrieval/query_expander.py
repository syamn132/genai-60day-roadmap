QUERY_EXPANSIONS = {
    "vacation": [
        "annual leave",
        "paid leave",
    ],
    "work from home": [
        "remote work",
        "remote working",
    ],
    "password": [
        "security password requirements",
        "authentication requirements",
    ],
    "contractor": [
        "contract employee",
        "contract worker",
    ],
    "carry forward": [
        "unused leave",
        "rollover leave",
    ],
}


def expand_query(
    query: str,
) -> list[str]:
    """
    Produce lightweight domain-aware query variants.

    This is intentionally rule-based so we can see
    exactly what expansion does before introducing
    LLM-based query rewriting later.
    """

    expanded_queries = [query]

    lower_query = query.lower()

    for keyword, alternatives in QUERY_EXPANSIONS.items():
        if keyword in lower_query:
            for alternative in alternatives:
                expanded_queries.append(
                    f"{query} {alternative}"
                )

    # Remove duplicates while preserving order.
    expanded_queries = list(
        dict.fromkeys(expanded_queries)
    )

    return expanded_queries