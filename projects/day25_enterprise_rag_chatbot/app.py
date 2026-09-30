import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"


from config import (
    CANDIDATE_K,
    CHUNKS_PATH,
    COMPRESSION_TOP_SENTENCES,
    FAISS_INDEX_PATH,
    FINAL_K,
    SOURCE_LIMIT,
)

from embeddings import EmbeddingModel

from rag.compressor import (
    compress_results,
)

from rag.context_builder import (
    build_context,
    build_source_list,
)

from rag.generator import (
    AnswerGenerator,
)

from rag.guardrails import (
    has_sufficient_evidence,
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


NO_ANSWER_MESSAGE = (
    "I couldn't find enough information "
    "in the available company documents "
    "to answer that question."
)


INVALID_GENERATED_ANSWERS = {
    "",
    ".",
    "1",
    "1.",
    "2",
    "2.",
}


def answer_question(
    query: str,
    retriever: Retriever,
    reranker: Reranker,
    embedding_model: EmbeddingModel,
    generator: AnswerGenerator,
) -> dict:
    """
    Run the complete online RAG query pipeline.
    """

    # --------------------------------------------------
    # 1. Query expansion
    # --------------------------------------------------

    expanded_queries = expand_query(
        query
    )

    # --------------------------------------------------
    # 2. Semantic candidate retrieval
    # --------------------------------------------------

    candidates = (
        retriever.multi_query_search(
            expanded_queries,
            top_k=CANDIDATE_K,
        )
    )

    # --------------------------------------------------
    # 3. Reranking
    # --------------------------------------------------

    reranked = reranker.rerank(
        query=query,
        candidates=candidates,
        final_k=FINAL_K,
    )

    # --------------------------------------------------
    # 4. Evidence guardrail
    # --------------------------------------------------

    sufficient, evidence_score = (
        has_sufficient_evidence(
            reranked
        )
    )

    if not sufficient:
        return {
            "answer": NO_ANSWER_MESSAGE,
            "sources": [],
            "evidence_score": evidence_score,
            "status": "insufficient_evidence",
        }

    # --------------------------------------------------
    # 5. Contextual compression
    # --------------------------------------------------

    compressed = compress_results(
        query=query,
        results=reranked,
        embedding_model=embedding_model,
        top_sentences=(
            COMPRESSION_TOP_SENTENCES
        ),
    )

    # --------------------------------------------------
    # 6. Context construction
    # --------------------------------------------------

    context = build_context(
        compressed
    )

    # --------------------------------------------------
    # 7. Grounded generation
    # --------------------------------------------------

    answer = generator.generate(
        question=query,
        context=context,
    )

    cleaned_answer = answer.strip()

    # --------------------------------------------------
    # 8. Output / abstention guardrail
    # --------------------------------------------------

    if (
        cleaned_answer in INVALID_GENERATED_ANSWERS
        or "INSUFFICIENT_EVIDENCE"
        in cleaned_answer.upper()
    ):
        return {
            "answer": NO_ANSWER_MESSAGE,
            "sources": [],
            "evidence_score": evidence_score,
            "status": "insufficient_evidence",
        }

    # --------------------------------------------------
    # 9. Deterministic source attribution
    # --------------------------------------------------

    sources = build_source_list(
        compressed,
        max_sources=SOURCE_LIMIT,
    )

    return {
        "answer": cleaned_answer,
        "sources": sources,
        "evidence_score": evidence_score,
        "status": "answered",
    }


def main():
    print("=" * 70)
    print("ENTERPRISE RAG CHATBOT")
    print("=" * 70)

    # --------------------------------------------------
    # Verify offline index exists
    # --------------------------------------------------

    if (
        not FAISS_INDEX_PATH.exists()
        or not CHUNKS_PATH.exists()
    ):
        print(
            "\nRAG index has not been built."
        )

        print(
            "Run this command first:"
        )

        print(
            "\npython build_index.py"
        )

        return

    # --------------------------------------------------
    # Load runtime models
    # --------------------------------------------------

    embedding_model = EmbeddingModel()

    retriever = Retriever(
        embedding_model
    )

    reranker = Reranker()

    generator = AnswerGenerator()

    # --------------------------------------------------
    # Interactive chatbot
    # --------------------------------------------------

    print("\n")
    print("=" * 70)
    print("CHATBOT READY")
    print("=" * 70)

    print(
        "\nAsk a question about the "
        "company documents."
    )

    print(
        "Type 'exit' to stop."
    )

    while True:
        query = input(
            "\nYou: "
        ).strip()

        if query.lower() in {
            "exit",
            "quit",
        }:
            print(
                "\nChatbot stopped."
            )

            break

        if not query:
            continue

        result = answer_question(
            query=query,
            retriever=retriever,
            reranker=reranker,
            embedding_model=embedding_model,
            generator=generator,
        )

        print("\nAssistant:")
        print(
            result["answer"]
        )

        if result["sources"]:
            print("\nSources:")

            for source in result["sources"]:
                print(
                    f"- {source}"
                )

        print(
            "\nEvidence score:",
            f"{result['evidence_score']:.4f}",
        )

        print(
            "Status:",
            result["status"],
        )


if __name__ == "__main__":
    main()