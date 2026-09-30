# A tiny fake vocabulary

vocabulary = {
    "cat": 0,
    "dog": 1,
    "car": 2,
    "love": 3,
    "AI": 4
}


# A tiny fake embedding matrix
# Each row corresponds to one token ID.

embedding_matrix = [
    [0.80, 0.20, 0.70],   # cat
    [0.75, 0.25, 0.68],   # dog
    [-0.40, 0.90, 0.10],  # car
    [0.30, -0.70, 0.80],  # love
    [0.60, 0.40, -0.20]   # AI
]


token = "dog"

token_id = vocabulary[token]

embedding = embedding_matrix[token_id]


print("Token:", token)
print("Token ID:", token_id)
print("Embedding:", embedding)

sentence = ["cat", "love", "AI"]

token_ids = [vocabulary[token] for token in sentence]

embeddings = [
    embedding_matrix[token_id]
    for token_id in token_ids
]

print("\nSentence:", sentence)
print("Token IDs:", token_ids)

print("\nEmbeddings:")

for token, token_id, embedding in zip(
    sentence,
    token_ids,
    embeddings
):
    print(
        token,
        "→",
        token_id,
        "→",
        embedding
    )