I built an enterprise RAG chatbot from scratch
without hiding the core pipeline behind LangChain.

I separated offline document indexing from
online question answering.

Documents are chunked, embedded and indexed in FAISS.

At query time I perform query expansion,
semantic retrieval and cross-encoder reranking.

I compress the final evidence before building
the LLM context.

The generator is instructed to answer only from
retrieved evidence.

I added a calibrated evidence threshold and
abstention logic to reduce hallucinations.

I also created a golden evaluation suite that
separately measures retrieval, reranking,
generation, source attribution and no-answer behavior.