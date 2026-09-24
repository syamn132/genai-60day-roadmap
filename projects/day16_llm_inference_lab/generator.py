import torch

from model_utils import load_model


def greedy_generate(
    prompt,
    tokenizer,
    model,
    max_new_tokens=20
):
    encoded = tokenizer(
        prompt,
        return_tensors="pt"
    )

    input_ids = encoded["input_ids"]

    print("\n================================")
    print("MANUAL GREEDY DECODING")
    print("================================")

    print(f"\nPrompt:\n{prompt}")

    print("\nGenerating:\n")

    for step in range(max_new_tokens):

        # Protect against exceeding the model context window
        if input_ids.shape[1] >= tokenizer.model_max_length:
            print("\nContext limit reached.")
            break

        # Inference only
        with torch.no_grad():
            outputs = model(
                input_ids=input_ids
            )

        # Get logits from the final sequence position
        next_token_logits = outputs.logits[:, -1, :]

        # Convert logits to probabilities
        probabilities = torch.softmax(
            next_token_logits,
            dim=-1
        )

        # GREEDY SEARCH:
        # choose highest-probability token
        next_token_id = torch.argmax(
            probabilities,
            dim=-1,
            keepdim=True
        )

        probability = probabilities.gather(
            dim=-1,
            index=next_token_id
        ).item()

        token_id = next_token_id.item()

        token_text = tokenizer.decode(
            [token_id]
        )

        print(
            f"Step {step + 1:2} | "
            f"Token ID: {token_id:5} | "
            f"Probability: {probability:.4f} | "
            f"Token: {repr(token_text)}"
        )

        # Append selected token to the sequence
        input_ids = torch.cat(
            [input_ids, next_token_id],
            dim=-1
        )

        # Stop if model predicts EOS
        if token_id == tokenizer.eos_token_id:
            print("\nEnd-of-sequence token generated.")
            break

    generated_text = tokenizer.decode(
        input_ids[0],
        skip_special_tokens=True
    )

    print("\n================================")
    print("FINAL GENERATED TEXT")
    print("================================")

    print(generated_text)

    return generated_text

def temperature_generate(
    prompt,
    tokenizer,
    model,
    temperature=1.0,
    max_new_tokens=20
):
    if temperature <= 0:
        raise ValueError("Temperature must be greater than 0.")

    encoded = tokenizer(
        prompt,
        return_tensors="pt"
    )

    input_ids = encoded["input_ids"]

    print("\n================================")
    print(f"TEMPERATURE SAMPLING — T={temperature}")
    print("================================")

    print(f"\nPrompt:\n{prompt}")

    print("\nGenerating:\n")

    for step in range(max_new_tokens):

        if input_ids.shape[1] >= tokenizer.model_max_length:
            print("\nContext limit reached.")
            break

        with torch.no_grad():
            outputs = model(
                input_ids=input_ids
            )

        # Logits for next token
        next_token_logits = outputs.logits[:, -1, :]

        # Apply temperature BEFORE softmax
        scaled_logits = next_token_logits / temperature

        probabilities = torch.softmax(
            scaled_logits,
            dim=-1
        )

        # SAMPLE instead of argmax
        next_token_id = torch.multinomial(
            probabilities,
            num_samples=1
        )

        probability = probabilities.gather(
            dim=-1,
            index=next_token_id
        ).item()

        token_id = next_token_id.item()

        token_text = tokenizer.decode(
            [token_id]
        )

        print(
            f"Step {step + 1:2} | "
            f"Token ID: {token_id:5} | "
            f"Probability: {probability:.4f} | "
            f"Token: {repr(token_text)}"
        )

        input_ids = torch.cat(
            [input_ids, next_token_id],
            dim=-1
        )

        if token_id == tokenizer.eos_token_id:
            print("\nEnd-of-sequence token generated.")
            break

    generated_text = tokenizer.decode(
        input_ids[0],
        skip_special_tokens=True
    )

    print("\n================================")
    print("FINAL GENERATED TEXT")
    print("================================")

    print(generated_text)

    return generated_text

def top_k_generate(
    prompt,
    tokenizer,
    model,
    top_k=20,
    temperature=1.0,
    max_new_tokens=20
):
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")

    encoded = tokenizer(
        prompt,
        return_tensors="pt"
    )

    input_ids = encoded["input_ids"]

    print("\n================================")
    print(f"TOP-K SAMPLING — K={top_k}")
    print("================================")

    print(f"\nPrompt:\n{prompt}")
    print("\nGenerating:\n")

    for step in range(max_new_tokens):

        if input_ids.shape[1] >= tokenizer.model_max_length:
            print("\nContext limit reached.")
            break

        with torch.no_grad():
            outputs = model(input_ids=input_ids)

        next_token_logits = outputs.logits[:, -1, :]

        # Optional temperature adjustment
        scaled_logits = next_token_logits / temperature

        # Find the K largest logits
        top_k_logits, top_k_ids = torch.topk(
            scaled_logits,
            top_k,
            dim=-1
        )

        # Softmax ONLY over those K candidates
        top_k_probabilities = torch.softmax(
            top_k_logits,
            dim=-1
        )

        # Sample an index inside the filtered candidate set
        sampled_index = torch.multinomial(
            top_k_probabilities,
            num_samples=1
        )

        # Convert candidate-set index back to vocabulary token ID
        next_token_id = top_k_ids.gather(
            dim=-1,
            index=sampled_index
        )

        selected_probability = top_k_probabilities.gather(
            dim=-1,
            index=sampled_index
        ).item()

        token_id = next_token_id.item()
        token_text = tokenizer.decode([token_id])

        print(
            f"Step {step + 1:2} | "
            f"Token ID: {token_id:5} | "
            f"Filtered Probability: {selected_probability:.4f} | "
            f"Token: {repr(token_text)}"
        )

        input_ids = torch.cat(
            [input_ids, next_token_id],
            dim=-1
        )

        if token_id == tokenizer.eos_token_id:
            print("\nEnd-of-sequence token generated.")
            break

    generated_text = tokenizer.decode(
        input_ids[0],
        skip_special_tokens=True
    )

    print("\n================================")
    print("FINAL GENERATED TEXT")
    print("================================")

    print(generated_text)

    return generated_text

def top_p_generate(
    prompt,
    tokenizer,
    model,
    top_p=0.90,
    temperature=1.0,
    max_new_tokens=20
):
    if not 0 < top_p <= 1:
        raise ValueError("top_p must be between 0 and 1.")

    encoded = tokenizer(
        prompt,
        return_tensors="pt"
    )

    input_ids = encoded["input_ids"]

    print("\n================================")
    print(f"TOP-P SAMPLING — P={top_p}")
    print("================================")

    print(f"\nPrompt:\n{prompt}")
    print("\nGenerating:\n")

    for step in range(max_new_tokens):

        if input_ids.shape[1] >= tokenizer.model_max_length:
            print("\nContext limit reached.")
            break

        with torch.no_grad():
            outputs = model(input_ids=input_ids)

        next_token_logits = outputs.logits[:, -1, :]

        scaled_logits = next_token_logits / temperature

        probabilities = torch.softmax(
            scaled_logits,
            dim=-1
        )

        # Sort probabilities from highest to lowest
        sorted_probs, sorted_ids = torch.sort(
            probabilities,
            descending=True,
            dim=-1
        )

        cumulative_probs = torch.cumsum(
            sorted_probs,
            dim=-1
        )

        # Keep tokens until cumulative probability reaches top_p.
        # Shift mask right so the token that crosses the threshold
        # is also retained.
        remove_mask = cumulative_probs > top_p

        remove_mask[..., 1:] = remove_mask[..., :-1].clone()
        remove_mask[..., 0] = False

        filtered_probs = sorted_probs.masked_fill(
            remove_mask,
            0.0
        )

        # Renormalize
        filtered_probs = (
            filtered_probs /
            filtered_probs.sum(dim=-1, keepdim=True)
        )

        sampled_index = torch.multinomial(
            filtered_probs,
            num_samples=1
        )

        next_token_id = sorted_ids.gather(
            dim=-1,
            index=sampled_index
        )

        selected_probability = filtered_probs.gather(
            dim=-1,
            index=sampled_index
        ).item()

        allowed_tokens = (
            filtered_probs > 0
        ).sum().item()

        token_id = next_token_id.item()
        token_text = tokenizer.decode([token_id])

        print(
            f"Step {step + 1:2} | "
            f"Candidates: {allowed_tokens:4} | "
            f"Token ID: {token_id:5} | "
            f"Filtered Probability: {selected_probability:.4f} | "
            f"Token: {repr(token_text)}"
        )

        input_ids = torch.cat(
            [input_ids, next_token_id],
            dim=-1
        )

        if token_id == tokenizer.eos_token_id:
            print("\nEnd-of-sequence token generated.")
            break

    generated_text = tokenizer.decode(
        input_ids[0],
        skip_special_tokens=True
    )

    print("\n================================")
    print("FINAL GENERATED TEXT")
    print("================================")

    print(generated_text)

    return generated_text

def beam_generate(
    prompt,
    tokenizer,
    model,
    num_beams=4,
    max_new_tokens=20
):
    encoded = tokenizer(
        prompt,
        return_tensors="pt"
    )

    print("\n================================")
    print(f"BEAM SEARCH — WIDTH={num_beams}")
    print("================================")

    print(f"\nPrompt:\n{prompt}")

    with torch.no_grad():
        output_ids = model.generate(
            **encoded,
            max_new_tokens=max_new_tokens,
            num_beams=num_beams,
            do_sample=False,
            early_stopping=True,
            pad_token_id=tokenizer.eos_token_id
        )

    generated_text = tokenizer.decode(
        output_ids[0],
        skip_special_tokens=True
    )

    print("\nGenerated text:")
    print(generated_text)

    return generated_text

if __name__ == "__main__":

    tokenizer, model = load_model()

    prompt = "Artificial intelligence will"

    top_k_generate(
        prompt,
        tokenizer,
        model,
        top_k=20,
        temperature=1.0,
        max_new_tokens=20
    )

    top_p_generate(
        prompt,
        tokenizer,
        model,
        top_p=0.90,
        temperature=1.0,
        max_new_tokens=20
    )