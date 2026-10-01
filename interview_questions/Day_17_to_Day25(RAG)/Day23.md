1. What is reranking in RAG?
A. A reranker is a second-stage relevance model that rescans a smaller set of candidates returned by the first-stage retriever and reorders them based on their relevance to the query. A common architecture is to retrieve a larger candidate set quickly using dense, BM25, or hybrid search, then use a more accurate but slower reranker to select the final Top-K chunks for context.

If asked why:
It improves final retrieval precision without applying the expensive relevance model to the entire knowledge base.