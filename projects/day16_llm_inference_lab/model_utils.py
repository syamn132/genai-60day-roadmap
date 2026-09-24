import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_NAME = "distilgpt2"


def load_model():
    print("Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    print("Loading model...")
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

    model.eval()

    print("Model loaded successfully!")

    return tokenizer, model


def inspect_prompt(prompt, tokenizer):
    encoded = tokenizer(
        prompt,
        return_tensors="pt"
    )

    token_ids = encoded["input_ids"][0]

    tokens = tokenizer.convert_ids_to_tokens(
        token_ids.tolist()
    )

    print("\n==============================")
    print("PROMPT INSPECTION")
    print("==============================")

    print(f"\nPrompt:\n{prompt}")

    print("\nTokens:")
    print(tokens)

    print("\nToken IDs:")
    print(token_ids.tolist())

    print("\nToken count:")
    print(len(token_ids))

    print("\nTokenizer context limit:")
    print(tokenizer.model_max_length)

def inspect_next_token_predictions(prompt, tokenizer, model, top_k=10):
    encoded = tokenizer(
        prompt,
        return_tensors="pt"
    )

    print("\n==============================")
    print("NEXT TOKEN PREDICTIONS")
    print("==============================")

    # Inference only — no gradients or weight updates
    with torch.no_grad():
        outputs = model(**encoded)

    # Shape:
    # [batch_size, sequence_length, vocabulary_size]
    logits = outputs.logits

    print("\nLogits shape:")
    print(logits.shape)

    # We only need the logits from the final prompt position
    next_token_logits = logits[0, -1, :]

    print("\nNext-token logits shape:")
    print(next_token_logits.shape)

    # Convert raw logits into probabilities
    probabilities = torch.softmax(
        next_token_logits,
        dim=-1
    )

    # Get the highest-probability candidates
    top_probabilities, top_token_ids = torch.topk(
        probabilities,
        top_k
    )

    print(f"\nTop {top_k} predicted next tokens:\n")

    for rank, (token_id, probability) in enumerate(
        zip(top_token_ids, top_probabilities),
        start=1
    ):
        token_id = token_id.item()
        probability = probability.item()

        token_text = tokenizer.decode([token_id])

        print(
            f"{rank:2}. "
            f"Token ID: {token_id:5} | "
            f"Probability: {probability:.4f} | "
            f"Token: {repr(token_text)}"
        )

if __name__ == "__main__":

    tokenizer, model = load_model()

    prompt = "Artificial intelligence will change the world."

    inspect_prompt(prompt, tokenizer)

    inspect_next_token_predictions(
        prompt,
        tokenizer,
        model,
        top_k=10
    )