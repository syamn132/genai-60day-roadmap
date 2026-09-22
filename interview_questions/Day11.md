1. Why do Transformers need positional encoding?
A. Self-attention does not inherently encode token order, so Transformers need positional information to represent where each token occurs in the sequence. Positional encoding is combined with token embeddings so the model can reason about order and relative position.

2. Why did the original Transformer use sine and cosine positional encodings?
A. Because self-attention does not inherently contain sequence order. Sinusoidal positional encoding creates a deterministic vector for every token position using sine and cosine waves at different frequencies. This positional vector is added to the token embedding so the Transformer receives both token meaning and position information.