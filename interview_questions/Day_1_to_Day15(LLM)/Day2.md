1. What is the difference between self-attention and multi-head attention?
A. Self-attention computes contextual relationships among tokens using Query, Key and Value vectors. Multi-head attention runs several independent self-attention operations with different learned projections in parallel, allowing the model to capture different types of relationships, then concatenates and projects their outputs.

2. What does the Feed-Forward Network do in a Transformer?
A. The FFN applies the same nonlinear transformation independently to each token representation after attention. Attention mixes information across tokens, while the FFN further transforms each token's contextual representation and increases the model's representational capacity.

3. Why do Transformers use residual connections and normalization?
A. Residual connections preserve the original representation while adding newly learned information and provide shortcut paths that help gradients flow through deep networks. Normalization stabilizes the scale of activations, improving optimization and training stability.



Attention mixes information across tokens. FFN transforms each token. Residuals preserve information. Normalization stabilizes processing. Stacking many such blocks progressively builds richer representations.



4. How does a Transformer generate the next token?
A. After the input passes through the Transformer blocks, the final hidden representation is projected into vocabulary-sized logits. Softmax converts those logits into a probability distribution over the vocabulary, and a decoding strategy such as greedy decoding or sampling selects the next token. The selected token is appended to the sequence, and the process repeats autoregressively.