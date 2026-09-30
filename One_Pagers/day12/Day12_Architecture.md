INPUT
↓
Token Embeddings + Position
↓
────────────────────────────
ENCODER BLOCK
────────────────────────────
Multi-Head Self-Attention
↓
Residual + LayerNorm
↓
FFN
↓
Residual + LayerNorm
↓
Contextual representations
────────────────────────────

                ↓

────────────────────────────
DECODER BLOCK
────────────────────────────
Masked Self-Attention
↓
Residual + LayerNorm
↓
Cross-Attention
↓
Residual + LayerNorm
↓
FFN
↓
Residual + LayerNorm
↓
Hidden representation
────────────────────────────
↓
Vocabulary Projection
↓
Logits
↓
Softmax
↓
Next Token