# Enterprise RAG Chatbot

Day 25 Sprint 2 project from my GenAI Engineering roadmap.

This project implements an end-to-end Retrieval-Augmented Generation
(RAG) system for answering questions from enterprise policy documents.

## Architecture

### Offline indexing pipeline

Documents
→ Loading
→ Chunking
→ Metadata
→ Embeddings
→ FAISS Index

### Online query pipeline

User Query
→ Query Expansion
→ Semantic Retrieval
→ Cross-Encoder Reranking
→ Evidence Guardrail
→ Contextual Compression
→ Context Building
→ Grounded LLM Generation
→ Output Guardrail
→ Answer + Source

## Technologies

- Python
- PyTorch
- Hugging Face Transformers
- FAISS
- MiniLM embeddings
- Cross-Encoder reranking
- FLAN-T5 generation

## Features

- Enterprise document ingestion
- Paragraph-aware chunking
- Metadata propagation
- Dense semantic embeddings
- FAISS vector search
- Multi-query retrieval
- Query expansion
- Cross-encoder reranking
- Extractive contextual compression
- Grounded answer generation
- Evidence-score guardrail
- No-answer / abstention handling
- Deterministic source attribution
- Automated RAG evaluation

## Project Documents

The demo knowledge base contains synthetic enterprise policies for:

- Employee handbook
- Annual leave
- Contractors
- Remote work
- IT security

## Setup

Activate the project environment:

```bash
source ~/Documents/genai-60day-roadmap/.venv-pytorch/bin/activate