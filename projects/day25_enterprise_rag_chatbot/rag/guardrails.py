from config import MIN_EVIDENCE_SCORE


def has_sufficient_evidence(
    results: list[dict],
) -> tuple[bool, float]:
    """
    Basic retrieval-confidence guardrail.

    Uses the highest original semantic retrieval
    score among final results.

    IMPORTANT:
    The score is not a probability.
    The threshold must be calibrated using
    evaluation data.
    """

    if not results:
        return False, 0.0

    scores = []

    for result in results:
        score = result.get(
            "retrieval_score",
            result.get("score", 0.0),
        )

        scores.append(
            float(score)
        )

    best_score = max(scores)

    sufficient = (
        best_score >= MIN_EVIDENCE_SCORE
    )

    return sufficient, best_score