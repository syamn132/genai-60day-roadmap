import json

from config import (
    CANDIDATE_K,
    CHUNK_MAX_CHARS,
    DATA_DIR,
    FINAL_K,
)

from embeddings import EmbeddingModel

from evaluation.test_cases import (
    TEST_CASES,
)

from ingestion.chunker import (
    chunk_documents,
)

from ingestion.indexer import (
    build_faiss_index,
)

from ingestion.loader import (
    load_documents,
)

from retrieval.query_expander import (
    expand_query,
)

from retrieval.reranker import (
    Reranker,
)

from retrieval.retriever import (
    Retriever,
)

from rag.generator import (
    AnswerGenerator,
)

from app import (
    answer_question,
)


def answer_matches(
    answer: str,
    expected_groups: list[list[str]],
) -> bool:
    """
    Check whether an answer contains at least
    one acceptable value from every expected group.
    """

    if not expected_groups:
        return True

    answer_lower = answer.lower()

    for group in expected_groups:
        group_matched = any(
            option.lower() in answer_lower
            for option in group
        )

        if not group_matched:
            return False

    return True


def source_rank(
    results: list[dict],
    expected_source: str | None,
):
    """
    Return the rank of the expected source,
    or None when it does not appear.
    """

    if expected_source is None:
        return None

    for rank, result in enumerate(
        results,
        start=1,
    ):
        source = result[
            "metadata"
        ].get("source")

        if source == expected_source:
            return rank

    return None


def evaluate():
    print("=" * 75)
    print("DAY 25 — ENTERPRISE RAG CHATBOT")
    print("PART 6 — RAG EVALUATION")
    print("=" * 75)

    # --------------------------------------------------
    # Prepare index
    # --------------------------------------------------

    documents = load_documents(
        DATA_DIR
    )

    chunks = chunk_documents(
        documents,
        max_chars=CHUNK_MAX_CHARS,
    )

    print(
        f"\nDocuments loaded: {len(documents)}"
    )

    print(
        f"Chunks created: {len(chunks)}"
    )

    embedding_model = EmbeddingModel()

    build_faiss_index(
        chunks,
        embedding_model,
    )

    retriever = Retriever(
        embedding_model
    )

    reranker = Reranker()

    generator = AnswerGenerator()

    # --------------------------------------------------
    # Metric counters
    # --------------------------------------------------

    total = len(TEST_CASES)

    answerable_total = 0
    unanswerable_total = 0

    candidate_hits = 0
    rerank_hits = 0

    answer_correct = 0
    source_hits = 0
    status_correct = 0
    guardrail_correct = 0

    strict_passes = 0

    answerable_scores = []
    unanswerable_scores = []

    report = []

    # --------------------------------------------------
    # Run evaluation cases
    # --------------------------------------------------

    for number, case in enumerate(
        TEST_CASES,
        start=1,
    ):
        question = case["question"]

        expected_status = case[
            "expected_status"
        ]

        expected_source = case[
            "expected_source"
        ]

        expected_groups = case[
            "expected_answer_groups"
        ]

        print("\n")
        print("=" * 75)
        print(
            f"TEST {number}/{total}: "
            f"{case['id']}"
        )
        print("=" * 75)

        print("\nQuestion:")
        print(question)

        # ----------------------------------------------
        # Retrieval evaluation
        # ----------------------------------------------

        expanded_queries = expand_query(
            question
        )

        candidates = (
            retriever.multi_query_search(
                expanded_queries,
                top_k=CANDIDATE_K,
            )
        )

        candidate_rank = source_rank(
            candidates,
            expected_source,
        )

        # ----------------------------------------------
        # Reranking evaluation
        # ----------------------------------------------

        reranked = reranker.rerank(
            query=question,
            candidates=candidates,
            final_k=FINAL_K,
        )

        final_rank = source_rank(
            reranked,
            expected_source,
        )

        # ----------------------------------------------
        # End-to-end generation evaluation
        # ----------------------------------------------

        result = answer_question(
            query=question,
            retriever=retriever,
            reranker=reranker,
            embedding_model=embedding_model,
            generator=generator,
        )

        status_match = (
            result["status"]
            == expected_status
        )

        if status_match:
            status_correct += 1

        # ----------------------------------------------
        # Answerable cases
        # ----------------------------------------------

        if expected_status == "answered":
            answerable_total += 1

            candidate_hit = (
                candidate_rank is not None
            )

            rerank_hit = (
                final_rank is not None
            )

            answer_match = answer_matches(
                result["answer"],
                expected_groups,
            )

            source_hit = (
                expected_source
                in result["sources"]
            )

            if candidate_hit:
                candidate_hits += 1

            if rerank_hit:
                rerank_hits += 1

            if answer_match:
                answer_correct += 1

            if source_hit:
                source_hits += 1

            answerable_scores.append(
                result["evidence_score"]
            )

            strict_pass = all(
                [
                    candidate_hit,
                    rerank_hit,
                    answer_match,
                    source_hit,
                    status_match,
                ]
            )

        # ----------------------------------------------
        # Unanswerable cases
        # ----------------------------------------------

        else:
            unanswerable_total += 1

            candidate_hit = None
            rerank_hit = None
            answer_match = None
            source_hit = (
                len(result["sources"]) == 0
            )

            guardrail_pass = (
                result["status"]
                == "insufficient_evidence"
            )

            if guardrail_pass:
                guardrail_correct += 1

            unanswerable_scores.append(
                result["evidence_score"]
            )

            strict_pass = (
                guardrail_pass
                and source_hit
            )

        if strict_pass:
            strict_passes += 1

        # ----------------------------------------------
        # Display result
        # ----------------------------------------------

        print("\nExpected status:")
        print(expected_status)

        print("\nActual status:")
        print(result["status"])

        print("\nAnswer:")
        print(result["answer"])

        print("\nSources:")
        if result["sources"]:
            for source in result["sources"]:
                print(f"- {source}")
        else:
            print("- None")

        print(
            "\nEvidence score:",
            f"{result['evidence_score']:.4f}",
        )

        if expected_source:
            print(
                "\nExpected source:",
                expected_source,
            )

            print(
                "Candidate source rank:",
                candidate_rank,
            )

            print(
                "Final source rank:",
                final_rank,
            )

            print(
                "Answer keyword check:",
                "PASS" if answer_match else "FAIL",
            )

            print(
                "Source check:",
                "PASS" if source_hit else "FAIL",
            )

        print(
            "Status check:",
            "PASS" if status_match else "FAIL",
        )

        print(
            "\nSTRICT RESULT:",
            "PASS" if strict_pass else "FAIL",
        )

        report.append(
            {
                "id": case["id"],
                "question": question,
                "expected_status": expected_status,
                "actual_status": result["status"],
                "expected_source": expected_source,
                "candidate_source_rank": (
                    candidate_rank
                ),
                "final_source_rank": (
                    final_rank
                ),
                "answer": result["answer"],
                "sources": result["sources"],
                "evidence_score": (
                    result["evidence_score"]
                ),
                "strict_pass": strict_pass,
            }
        )

    # --------------------------------------------------
    # Metrics
    # --------------------------------------------------

    print("\n\n")
    print("=" * 75)
    print("EVALUATION SUMMARY")
    print("=" * 75)

    def percentage(
        value,
        denominator,
    ):
        if denominator == 0:
            return 0.0

        return (
            value
            / denominator
            * 100
        )

    candidate_hit_rate = percentage(
        candidate_hits,
        answerable_total,
    )

    rerank_hit_rate = percentage(
        rerank_hits,
        answerable_total,
    )

    answer_accuracy = percentage(
        answer_correct,
        answerable_total,
    )

    source_hit_rate = percentage(
        source_hits,
        answerable_total,
    )

    status_accuracy = percentage(
        status_correct,
        total,
    )

    guardrail_accuracy = percentage(
        guardrail_correct,
        unanswerable_total,
    )

    strict_pass_rate = percentage(
        strict_passes,
        total,
    )

    print(
        f"\nTotal tests: {total}"
    )

    print(
        f"Answerable: {answerable_total}"
    )

    print(
        f"Unanswerable: {unanswerable_total}"
    )

    print(
        "\nCandidate Hit Rate: "
        f"{candidate_hit_rate:.1f}%"
    )

    print(
        "Rerank Hit Rate: "
        f"{rerank_hit_rate:.1f}%"
    )

    print(
        "Answer Keyword Accuracy: "
        f"{answer_accuracy:.1f}%"
    )

    print(
        "Source Hit Rate: "
        f"{source_hit_rate:.1f}%"
    )

    print(
        "Status Accuracy: "
        f"{status_accuracy:.1f}%"
    )

    print(
        "No-Answer Guardrail Accuracy: "
        f"{guardrail_accuracy:.1f}%"
    )

    print(
        "Strict End-to-End Pass Rate: "
        f"{strict_pass_rate:.1f}%"
    )

    # --------------------------------------------------
    # Evidence-score analysis
    # --------------------------------------------------

    if answerable_scores:
        avg_answerable = (
            sum(answerable_scores)
            / len(answerable_scores)
        )

        print(
            "\nAverage answerable "
            "evidence score: "
            f"{avg_answerable:.4f}"
        )

        print(
            "Lowest answerable "
            "evidence score: "
            f"{min(answerable_scores):.4f}"
        )

    if unanswerable_scores:
        avg_unanswerable = (
            sum(unanswerable_scores)
            / len(unanswerable_scores)
        )

        print(
            "\nAverage unanswerable "
            "evidence score: "
            f"{avg_unanswerable:.4f}"
        )

        print(
            "Highest unanswerable "
            "evidence score: "
            f"{max(unanswerable_scores):.4f}"
        )

    # --------------------------------------------------
    # Save JSON report
    # --------------------------------------------------

    report_path = (
        DATA_DIR.parent
        / "evaluation"
        / "evaluation_report.json"
    )

    with report_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )

    print(
        f"\nDetailed report saved to:\n"
        f"{report_path}"
    )


if __name__ == "__main__":
    evaluate()