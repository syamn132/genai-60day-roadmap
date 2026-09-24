Prefill = processing all existing prompt/context tokens in parallel to build their internal representations and attention state before generating new tokens.


Context is temporary working memory, not permanent model knowledge.

Top-K = keep/filter the K highest-probability token candidates, then sample from them. It doesn’t itself select the final token.

Top-P = keep the smallest set of highest-probability tokens whose cumulative probability reaches or exceeds P, then renormalize and sample.


FINAL GENERATION PIPELINE:

User Prompt
↓
Tokenizer
↓
Token IDs
↓
Embeddings + Position
↓
Prefill
↓
Build KV Cache
↓
Transformer Blocks
↓
Final Hidden State
↓
Vocabulary Projection
↓
Logits
↓
Temperature
↓
Softmax
↓
Probabilities
↓
Top-K / Top-P filtering
↓
Sampling / Decoding Strategy
↓
Selected Token
↓
Append token
↓
Update KV Cache
↓
Repeat Decode