# LLM Inference & Decoding Playground

A hands-on mini project created during Day 16 of my
GenAI 60-Day Roadmap.

## Objective

Understand and experimentally demonstrate how a
decoder-only Transformer generates text during inference.

## Model

DistilGPT-2

## Technologies

- Python
- PyTorch
- Hugging Face Transformers

## Concepts Demonstrated

- Tokenization
- Token IDs
- Context Window
- Next-Token Prediction
- Logits
- Softmax
- Greedy Search
- Beam Search
- Temperature
- Top-K Sampling
- Top-P / Nucleus Sampling
- Prefill
- Decode
- KV Cache

## Architecture

User Prompt
↓
Tokenizer
↓
Token IDs
↓
GPT Model
↓
Final Hidden Representation
↓
Vocabulary Logits
↓
Decoding Strategy
↓
Generated Token
↓
Append Token
↓
Repeat

## Experiments

### Tokenization

Inspect how raw text is converted into tokens and token IDs.

### Next-Token Prediction

Inspect vocabulary logits and the highest-probability
next-token candidates.

### Greedy Search

Manually generate tokens by always selecting the
highest-probability token.

### Temperature

Compare low-temperature and high-temperature sampling.

### Top-K

Restrict sampling to a fixed number of highest-probability
token candidates.

### Top-P

Dynamically select the smallest token set whose cumulative
probability reaches the configured threshold.

### KV Cache

Inspect actual Key and Value tensor shapes returned by the
Transformer.

Observed example:

Prompt tokens:

4

KV cache after prefill:

4 positions

After one decode step:

5 positions

### KV Cache Performance Experiment

Example result on local Intel Mac:

Without KV Cache:
2.8784 seconds

With KV Cache:
1.2156 seconds

Speedup:
2.37x

Results vary depending on hardware and input length.

## Key Learning

KV Cache improves autoregressive inference by reusing the
Keys and Values of previously processed tokens instead of
recomputing them at every decoding step.

The cache trades additional memory usage for faster
generation.

## Run

Activate the project environment:

```bash
source .venv-pytorch/bin/activate