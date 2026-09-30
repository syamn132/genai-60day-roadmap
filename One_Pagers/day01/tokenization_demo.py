import tiktoken

# Load a tokenizer
encoding = tiktoken.get_encoding("cl100k_base")

text = "I love Generative AI!"

# Convert text into token IDs
token_ids = encoding.encode(text)

print("Original text:")
print(text)

print("\nToken IDs:")
print(token_ids)

print("\nNumber of tokens:")
print(len(token_ids))

print("\nIndividual tokens:")

for token_id in token_ids:
    token_bytes = encoding.decode_single_token_bytes(token_id)

    print(
        "Token ID:",
        token_id,
        "| Raw bytes:",
        token_bytes,
        "| Decoded:",
        token_bytes.decode("utf-8", errors="replace")
    )

print("\nDecoded text:")
print(encoding.decode(token_ids))


#2nd Example text = "electroencephalographically"
text = "electroencephalographically"

# Convert text into token IDs
token_ids = encoding.encode(text)

print("Original text:")
print(text)

print("\nToken IDs:")
print(token_ids)

print("\nNumber of tokens:")
print(len(token_ids))

print("\nIndividual tokens:")

for token_id in token_ids:
    token_bytes = encoding.decode_single_token_bytes(token_id)

    print(
        "Token ID:",
        token_id,
        "| Raw bytes:",
        token_bytes,
        "| Decoded:",
        token_bytes.decode("utf-8", errors="replace")
    )

print("\nDecoded text:")
print(encoding.decode(token_ids))


# Next Experiment 2 Space matters
texts = [
    "hello",
    " hello",
    "hello world",
    "hello  world"
]

for text in texts:
    token_ids = encoding.encode(text)

    print(text)
    print(token_ids)
    print("Token count:", len(token_ids))
    print()


#Exp 3 Eng Vs Kannada

texts = [
    "Hello, how are you?",
    "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?"
]

for text in texts:
    token_ids = encoding.encode(text)

    print("Text:", text)
    print("Token IDs:", token_ids)
    print("Token count:", len(token_ids))
    print()



#Sample Exp
text = "ನಮಸ್ಕಾರ"

token_ids = encoding.encode(text)

print("Text:", text)
print("Token count:", len(token_ids))

for token_id in token_ids:
    token_bytes = encoding.decode_single_token_bytes(token_id)

    print(
        "Token ID:",
        token_id,
        "| Bytes:",
        token_bytes,
        "| Decoded:",
        token_bytes.decode("utf-8", errors="replace")
    )