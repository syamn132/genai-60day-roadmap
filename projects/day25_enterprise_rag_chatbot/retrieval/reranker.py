import torch

from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)

from config import (
    RERANKER_MODEL_NAME,
)


class Reranker:
    """
    Cross-encoder reranker.

    Scores query-document pairs jointly.
    """

    def __init__(self):
        print(
            f"Loading reranker: "
            f"{RERANKER_MODEL_NAME}"
        )

        self.tokenizer = (
            AutoTokenizer.from_pretrained(
                RERANKER_MODEL_NAME
            )
        )

        self.model = (
            AutoModelForSequenceClassification
            .from_pretrained(
                RERANKER_MODEL_NAME
            )
        )

        self.model.eval()

        self.device = torch.device("cpu")

        self.model.to(self.device)

    def rerank(
        self,
        query: str,
        candidates: list[dict],
        final_k: int = 3,
    ) -> list[dict]:
        """
        Score query + candidate text together
        and reorder the candidate set.
        """

        if not candidates:
            return []

        pairs = [
            (query, candidate["text"])
            for candidate in candidates
        ]

        queries = [
            pair[0]
            for pair in pairs
        ]

        documents = [
            pair[1]
            for pair in pairs
        ]

        encoded = self.tokenizer(
            queries,
            documents,
            padding=True,
            truncation=True,
            return_tensors="pt",
        )

        encoded = {
            key: value.to(self.device)
            for key, value in encoded.items()
        }

        with torch.no_grad():
            outputs = self.model(
                **encoded
            )

        scores = (
            outputs.logits
            .squeeze(-1)
            .cpu()
            .tolist()
        )

        if not isinstance(
            scores,
            list,
        ):
            scores = [scores]

        reranked = []

        for candidate, score in zip(
            candidates,
            scores,
        ):
            result = dict(candidate)

            result["retrieval_score"] = (
                candidate["score"]
            )

            result["rerank_score"] = (
                float(score)
            )

            reranked.append(result)

        reranked.sort(
            key=lambda item: item[
                "rerank_score"
            ],
            reverse=True,
        )

        reranked = reranked[
            :final_k
        ]

        for rank, result in enumerate(
            reranked,
            start=1,
        ):
            result["rank"] = rank

        return reranked