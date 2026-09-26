1. Why do LLMs use subword tokenization instead of pure word tokenization?
A: Subword tokenization balances vocabulary size and sequence length. It lets the tokenizer represent common words efficiently while still handling rare or unseen words by breaking them into smaller reusable pieces.

2. In simple words, what does BPE try to do?
A. BPE repeatedly merges frequently occurring adjacent token pairs, allowing common patterns to become larger tokens while rare words can still be represented using smaller pieces.

3. Why can't we use token IDs directly as input to the transformer?
A. Token IDs are arbitrary integer identifiers and do not encode semantic relationships. An embedding layer maps each token ID into a learned dense vector so the neural network can perform meaningful mathematical operations on token representations.

4. What is self-attention?
A. Self-attention allows every token to determine how relevant other tokens in the same sequence are. Each token is transformed into Query, Key, and Value vectors. Query–Key dot products produce attention scores, softmax converts those scores into weights, and the weighted Value vectors are combined to create a context-aware representation.

