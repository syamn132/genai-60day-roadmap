import torch
import torch.nn.functional as F

from transformers import AutoModel, AutoTokenizer

from config import EMBEDDING_MODEL_NAME


class EmbeddingModel:
    """
    Converts text into normalized dense vectors.

    Uses a Hugging Face transformer model and
    mean pooling over token embeddings.
    """

    def __init__(self):
        print(
            f"Loading embedding model: "
            f"{EMBEDDING_MODEL_NAME}"
        )

        self.tokenizer = AutoTokenizer.from_pretrained(
            EMBEDDING_MODEL_NAME
        )

        self.model = AutoModel.from_pretrained(
            EMBEDDING_MODEL_NAME
        )

        self.model.eval()

        self.device = torch.device("cpu")

        self.model.to(self.device)

    @staticmethod
    def _mean_pooling(
        model_output,
        attention_mask,
    ):
        """
        Mean-pool token embeddings while ignoring padding.
        """

        token_embeddings = model_output.last_hidden_state

        expanded_mask = (
            attention_mask
            .unsqueeze(-1)
            .expand(token_embeddings.size())
            .float()
        )

        summed_embeddings = torch.sum(
            token_embeddings * expanded_mask,
            dim=1,
        )

        summed_mask = torch.clamp(
            expanded_mask.sum(dim=1),
            min=1e-9,
        )

        return summed_embeddings / summed_mask

    def encode(
        self,
        texts: list[str],
        batch_size: int = 16,
    ):
        """
        Convert a list of texts into normalized vectors.
        """

        all_embeddings = []

        for start in range(
            0,
            len(texts),
            batch_size,
        ):
            batch = texts[
                start:start + batch_size
            ]

            encoded = self.tokenizer(
                batch,
                padding=True,
                truncation=True,
                return_tensors="pt",
            )

            encoded = {
                key: value.to(self.device)
                for key, value in encoded.items()
            }

            with torch.no_grad():
                model_output = self.model(
                    **encoded
                )

            embeddings = self._mean_pooling(
                model_output,
                encoded["attention_mask"],
            )

            embeddings = F.normalize(
                embeddings,
                p=2,
                dim=1,
            )

            all_embeddings.append(
                embeddings.cpu()
            )

        embeddings = torch.cat(
            all_embeddings,
            dim=0,
        )

        return (
            embeddings
            .numpy()
            .astype("float32")
        )