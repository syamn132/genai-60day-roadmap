from model_utils import (
    load_model,
    inspect_prompt,
    inspect_next_token_predictions
)

from generator import (
    greedy_generate,
    beam_generate,
    temperature_generate,
    top_k_generate,
    top_p_generate
)

from cache_demo import (
    inspect_kv_cache,
    compare_cache_performance
)


def show_menu():
    print("\n")
    print("=" * 50)
    print("        LLM INFERENCE & DECODING PLAYGROUND")
    print("=" * 50)

    print("""
1. Inspect Prompt / Tokens
2. Inspect Next-Token Predictions
3. Greedy Search
4. Beam Search
5. Low Temperature
6. High Temperature
7. Top-K Sampling
8. Top-P Sampling
9. Inspect KV Cache
10. KV Cache Performance Test
0. Exit
""")


def main():

    print("Loading model...")

    tokenizer, model = load_model()

    while True:

        show_menu()

        choice = input("Choose an option: ").strip()

        if choice == "0":
            print("\nExiting playground.")
            break

        prompt = input(
            "\nEnter prompt: "
        ).strip()

        if not prompt:
            print("Prompt cannot be empty.")
            continue

        if choice == "1":

            inspect_prompt(
                prompt,
                tokenizer
            )

        elif choice == "2":

            inspect_next_token_predictions(
                prompt,
                tokenizer,
                model,
                top_k=10
            )

        elif choice == "3":

            greedy_generate(
                prompt,
                tokenizer,
                model,
                max_new_tokens=30
            )

        elif choice == "4":

            beam_generate(
                prompt,
                tokenizer,
                model,
                num_beams=4,
                max_new_tokens=30
            )

        elif choice == "5":

            temperature_generate(
                prompt,
                tokenizer,
                model,
                temperature=0.3,
                max_new_tokens=30
            )

        elif choice == "6":

            temperature_generate(
                prompt,
                tokenizer,
                model,
                temperature=1.2,
                max_new_tokens=30
            )

        elif choice == "7":

            top_k_generate(
                prompt,
                tokenizer,
                model,
                top_k=20,
                temperature=1.0,
                max_new_tokens=30
            )

        elif choice == "8":

            top_p_generate(
                prompt,
                tokenizer,
                model,
                top_p=0.90,
                temperature=1.0,
                max_new_tokens=30
            )

        elif choice == "9":

            inspect_kv_cache(
                prompt,
                tokenizer,
                model
            )

        elif choice == "10":

            compare_cache_performance(
                prompt,
                tokenizer,
                model,
                max_new_tokens=50
            )

        else:
            print("\nInvalid option. Try again.")


if __name__ == "__main__":
    main()