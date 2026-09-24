import torch
import time

from model_utils import load_model


def inspect_kv_cache(prompt, tokenizer, model):

    print("\n================================")
    print("KV CACHE DEMO")
    print("================================")

    print(f"\nPrompt:\n{prompt}")

    encoded = tokenizer(
        prompt,
        return_tensors="pt"
    )

    input_ids = encoded["input_ids"]

    print("\nPrompt token IDs:")
    print(input_ids[0].tolist())

    print("\nPrompt token count:")
    print(input_ids.shape[1])

    # ---------------------------------
    # PREFILL
    # ---------------------------------

    print("\n================================")
    print("PREFILL")
    print("================================")

    with torch.no_grad():

        outputs = model(
            input_ids=input_ids,
            use_cache=True
        )

    past_key_values = outputs.past_key_values

    print("\nNumber of Transformer layers:")
    print(len(past_key_values))

    # Look at first layer
    first_layer_key = past_key_values[0][0]
    first_layer_value = past_key_values[0][1]

    print("\nLayer 1 Key shape:")
    print(first_layer_key.shape)

    print("\nLayer 1 Value shape:")
    print(first_layer_value.shape)

    print("\nShape meaning:")
    print(
        "[batch, attention_heads, "
        "cached_sequence_length, head_dimension]"
    )

    print("\nCached sequence length:")
    print(first_layer_key.shape[-2])

    # ---------------------------------
    # SELECT FIRST GENERATED TOKEN
    # ---------------------------------

    next_token_logits = outputs.logits[:, -1, :]

    next_token_id = torch.argmax(
        next_token_logits,
        dim=-1,
        keepdim=True
    )

    next_token_text = tokenizer.decode(
        next_token_id[0]
    )

    print("\nFirst generated token:")
    print(repr(next_token_text))

    print("\nToken ID:")
    print(next_token_id.item())

    # ---------------------------------
    # DECODE ONE STEP USING KV CACHE
    # ---------------------------------

    print("\n================================")
    print("DECODE — ONE NEW TOKEN")
    print("================================")

    with torch.no_grad():

        decode_outputs = model(
            input_ids=next_token_id,
            past_key_values=past_key_values,
            use_cache=True
        )

    updated_cache = decode_outputs.past_key_values

    updated_key = updated_cache[0][0]
    updated_value = updated_cache[0][1]

    print("\nLayer 1 Key shape AFTER decode:")
    print(updated_key.shape)

    print("\nLayer 1 Value shape AFTER decode:")
    print(updated_value.shape)

    print("\nUpdated cached sequence length:")
    print(updated_key.shape[-2])

    print("\n================================")
    print("SUMMARY")
    print("================================")

    print(
        f"Prompt tokens: "
        f"{input_ids.shape[1]}"
    )

    print(
        f"Cache after prefill: "
        f"{first_layer_key.shape[-2]}"
    )

    print(
        f"Cache after one decode step: "
        f"{updated_key.shape[-2]}"
    )

def generate_without_cache(
    prompt,
    tokenizer,
    model,
    max_new_tokens=50
):
    encoded = tokenizer(
        prompt,
        return_tensors="pt"
    )

    input_ids = encoded["input_ids"]

    start_time = time.perf_counter()

    for _ in range(max_new_tokens):

        if input_ids.shape[1] >= tokenizer.model_max_length:
            break

        with torch.no_grad():
            outputs = model(
                input_ids=input_ids,
                use_cache=False
            )

        next_token_logits = outputs.logits[:, -1, :]

        next_token_id = torch.argmax(
            next_token_logits,
            dim=-1,
            keepdim=True
        )

        input_ids = torch.cat(
            [input_ids, next_token_id],
            dim=-1
        )

        if next_token_id.item() == tokenizer.eos_token_id:
            break

    elapsed = time.perf_counter() - start_time

    generated_text = tokenizer.decode(
        input_ids[0],
        skip_special_tokens=True
    )

    return generated_text, elapsed

def generate_with_cache(
    prompt,
    tokenizer,
    model,
    max_new_tokens=50
):
    encoded = tokenizer(
        prompt,
        return_tensors="pt"
    )

    input_ids = encoded["input_ids"]

    start_time = time.perf_counter()

    # -----------------------------
    # PREFILL
    # -----------------------------

    with torch.no_grad():
        outputs = model(
            input_ids=input_ids,
            use_cache=True
        )

    past_key_values = outputs.past_key_values

    next_token_logits = outputs.logits[:, -1, :]

    next_token_id = torch.argmax(
        next_token_logits,
        dim=-1,
        keepdim=True
    )

    generated_ids = [
        input_ids,
        next_token_id
    ]

    if next_token_id.item() == tokenizer.eos_token_id:
        elapsed = time.perf_counter() - start_time

        full_ids = torch.cat(
            generated_ids,
            dim=-1
        )

        return (
            tokenizer.decode(
                full_ids[0],
                skip_special_tokens=True
            ),
            elapsed
        )

    # First generated token already produced above.
    # Generate the remaining tokens using the cache.

    for _ in range(max_new_tokens - 1):

        with torch.no_grad():
            outputs = model(
                input_ids=next_token_id,
                past_key_values=past_key_values,
                use_cache=True
            )

        past_key_values = outputs.past_key_values

        next_token_logits = outputs.logits[:, -1, :]

        next_token_id = torch.argmax(
            next_token_logits,
            dim=-1,
            keepdim=True
        )

        generated_ids.append(next_token_id)

        if next_token_id.item() == tokenizer.eos_token_id:
            break

    elapsed = time.perf_counter() - start_time

    full_ids = torch.cat(
        generated_ids,
        dim=-1
    )

    generated_text = tokenizer.decode(
        full_ids[0],
        skip_special_tokens=True
    )

    return generated_text, elapsed

def compare_cache_performance(
    prompt,
    tokenizer,
    model,
    max_new_tokens=50
):
    print("\n================================")
    print("KV CACHE PERFORMANCE TEST")
    print("================================")

    print(f"\nPrompt:\n{prompt}")

    print(
        f"\nGenerating {max_new_tokens} new tokens..."
    )

    text_without_cache, time_without_cache = (
        generate_without_cache(
            prompt,
            tokenizer,
            model,
            max_new_tokens
        )
    )

    text_with_cache, time_with_cache = (
        generate_with_cache(
            prompt,
            tokenizer,
            model,
            max_new_tokens
        )
    )

    print("\n================================")
    print("WITHOUT KV CACHE")
    print("================================")

    print(
        f"Time: {time_without_cache:.4f} seconds"
    )

    print("\nGenerated text:")
    print(text_without_cache)

    print("\n================================")
    print("WITH KV CACHE")
    print("================================")

    print(
        f"Time: {time_with_cache:.4f} seconds"
    )

    print("\nGenerated text:")
    print(text_with_cache)

    if time_with_cache > 0:

        speedup = (
            time_without_cache /
            time_with_cache
        )

        print("\n================================")
        print("RESULT")
        print("================================")

        print(
            f"Speedup: {speedup:.2f}x"
        )


if __name__ == "__main__":

    tokenizer, model = load_model()

    prompt = (
        "Artificial intelligence will transform "
        "many industries because"
    )

    inspect_kv_cache(
        prompt,
        tokenizer,
        model
    )

    compare_cache_performance(
        prompt,
        tokenizer,
        model,
        max_new_tokens=50
    )