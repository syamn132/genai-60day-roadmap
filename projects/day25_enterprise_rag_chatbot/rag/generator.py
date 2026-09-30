import torch

from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)

from config import (
    GENERATOR_MODEL_NAME,
    MAX_NEW_TOKENS,
)


class AnswerGenerator:
    """
    Local grounded answer generator using FLAN-T5.
    """

    def __init__(self):
        print(
            f"Loading generator: "
            f"{GENERATOR_MODEL_NAME}"
        )

        self.tokenizer = (
            AutoTokenizer.from_pretrained(
                GENERATOR_MODEL_NAME
            )
        )

        self.model = (
            AutoModelForSeq2SeqLM
            .from_pretrained(
                GENERATOR_MODEL_NAME
            )
        )

        self.device = torch.device(
            "cpu"
        )

        self.model.to(
            self.device
        )

        self.model.eval()

    def build_prompt(
    self,
    question: str,
    context: str,
    ) -> str:
        """
        Construct a concise grounded RAG prompt.
        """

        return f"""
Answer the question using only the provided evidence.

Important rules:
- Give a direct factual answer.
- For a yes/no question, begin with Yes or No.
- Never answer with a list number such as "1." or "2.".
- Do not use outside knowledge.
- Do not invent missing information.
- If the evidence does not contain the answer,
  output exactly: INSUFFICIENT_EVIDENCE

Evidence:
{context}

Question:
{question}

Direct answer:
""".strip()

    def generate(
        self,
        question: str,
        context: str,
    ) -> str:
        """
        Generate a grounded answer.
        """

        prompt = self.build_prompt(
            question=question,
            context=context,
        )

        encoded = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
        )

        encoded = {
            key: value.to(self.device)
            for key, value in encoded.items()
        }

        with torch.no_grad():
            output_ids = self.model.generate(
                **encoded,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=False,
                num_beams=3,
                early_stopping=True,
            )

        answer = self.tokenizer.decode(
            output_ids[0],
            skip_special_tokens=True,
        )

        return answer.strip()