🚀 GENAI ENGINEER JOURNEY (DAY-WISE)

---

## 📌 SINGLE SOURCE OF TRUTH — CURRENT STATUS

**Last updated:** 2026-10-08

**Overall progress:** Days 1–32 completed.

**Current sprint:** 🟣 Sprint 3 — LLM Frameworks

**Next exact step:** Day 33 — Multi-Agent Systems

**Day 23 status:** Completed — Advanced RAG, Query Expansion, Compression, Reranking.

**Day 24 status:** Completed — Production RAG, Evaluation, Hallucination, Guardrails.

**Day 24 one-pagers:** Completed — Part 1 Production RAG, Part 2 Evaluation, Part 3 Hallucination, Part 4 Guardrails, plus Day 24 Master one-pager.

**Day 25 status:** Completed — Sprint 2 Project: Enterprise RAG Chatbot. Project was built, evaluated, refined, documented, and pushed to GitHub.

**Day 25 project:** `projects/day25_enterprise_rag_chatbot/`

**Day 25 implementation breakdown used in this study:**

- ✅ Part 1: Architecture & Setup
- ✅ Part 2: Document Ingestion
- ✅ Part 3: Semantic Retrieval
- ✅ Part 4: Advanced RAG
- ✅ Part 5: Generation + Guardrails
- ✅ Part 6: Evaluation
- ✅ Part 7: Integration + GitHub

**Day 25 core implementation:** paragraph-aware chunking, metadata propagation, MiniLM dense embeddings, FAISS indexing/search, query expansion, multi-query retrieval, cross-encoder reranking, extractive contextual compression, context building, FLAN-T5 grounded generation, evidence-threshold abstention, deterministic source attribution, automated evaluation, offline index build, and interactive chatbot runtime.

**Day 25 evaluation baseline before final refinements:** Candidate Hit Rate 100.0%, Rerank Hit Rate 100.0%, Answer Keyword Accuracy 77.8%, Source Hit Rate 100.0%, Status Accuracy 91.7%, No-Answer Guardrail Accuracy 66.7%, Strict End-to-End Pass Rate 75.0%. The evaluation exposed generation and abstention failures; the evidence threshold was then raised to 0.50 and prompt/output guardrails were refined. Post-refinement metrics were not recorded in the chat.

**Day 25 one-pager:** Completed — Enterprise RAG Chatbot project summary.

**Day 26 status:** Completed — Prompt Engineering and Prompt Patterns.

**Day 26 learning breakdown:**

- ✅ Part 1: Prompt Engineering — task, context, input, constraints, delimiters, output format, failure behavior, grounding, role instructions, prompt structure, prompt-vs-fine-tuning, prompt-vs-RAG, prompt-vs-decoding, and iterative prompt evaluation/refinement.
- ✅ Part 2: Prompt Patterns — zero-shot, few-shot, role/persona, structured output, constraints, context/grounding, templates, extraction, classification, decomposition, plan-then-execute, critique/refine, validation, abstention/fallback, source attribution, rewrite, comparison, audience adaptation, prompt chaining, and dynamic templates.

**Day 26 one-pagers:** Completed — Part 1 Prompt Engineering, Part 2 Prompt Patterns, plus Day 26 Master one-pager.

**Day 27 status:** Completed — Model APIs: OpenAI API, Gemini API, and Claude API.

**Day 27 project:** `projects/day27_model_apis/`

**Day 27 learning breakdown:**

- ✅ Part 1: OpenAI API — official Python SDK, Responses API, API-key authentication, `instructions` + `input`, response parsing, classification example, and basic error handling.
- ✅ Part 2: Gemini API — `google-genai` SDK, Interactions API, `GEMINI_API_KEY`, `system_instruction`, generation configuration, classification, conversation state with `previous_interaction_id`, streaming concepts, multimodal awareness, and error handling.
- ✅ Part 3: Claude API — Anthropic Python SDK, Messages API, `ANTHROPIC_API_KEY`, top-level `system` instructions, `messages` history, `max_tokens`, content-block parsing, streaming concepts, classification, stateless multi-turn conversations, and error handling.

**Day 27 runtime notes:**

- OpenAI: SDK and authentication worked and the request reached the API, but live generation was blocked by exhausted API credits (`credit_balance_exhausted`).
- Gemini: Live API request succeeded. The working model used during the exercise was `gemini-3.5-flash-lite` because it responded faster in the user's environment than the heavier option tried earlier.
- Claude: API integration and code were taught and prepared; a successful live Claude terminal run was not explicitly confirmed in the chat.

**Day 27 one-pagers:** Completed — Part 1 OpenAI API, Part 2 Gemini API, Part 3 Claude API, plus Day 27 Master Model APIs one-pager.

**Day 28 status:** Completed — LangChain Basics.

**Day 28 project:** `projects/day28_langchain_basics/`

**Day 28 learning breakdown:**

- ✅ LangChain purpose and architecture — framework vs LLM, provider integrations, standard model interface, and provider abstraction.
- ✅ `init_chat_model()` and `model.invoke()` for a common model-calling interface.
- ✅ `SystemMessage`, `HumanMessage`, and `AIMessage`.
- ✅ Plain-string inputs vs message-based inputs.
- ✅ `invoke()`, `stream()`, and `batch()` concepts.
- ✅ Provider switching concept using the same LangChain interface.
- ✅ Direct SDK vs LangChain trade-offs.

**Day 28 runtime notes:**

- Live Gemini call through LangChain succeeded using `gemini-3.5-flash-lite`.
- The model returned the requested three bullet points.
- A warning indicated that `temperature` is ignored for this model because it uses fixed sampling defaults.
- An AFC-related warning was informational only; the request still completed successfully.

**Day 28 one-pager:** Completed — LangChain Basics one-pager.

**Day 29 status:** Completed — LangChain Chains, Memory, and Tools.

**Day 29 project:** `projects/day29_langchain_chains_memory_tools/`

**Day 29 learning breakdown:**

- ✅ Part 1: LangChain Chains — `ChatPromptTemplate`, dynamic variables, `StrOutputParser`, runnable composition with `|`, `chain.invoke()`, `stream()`, `batch()`, chain input/output types, practical classification chain, and chain vs prompt chaining.
- ✅ Part 2: Memory — manual message history, `MessagesPlaceholder`, `HumanMessage` + `AIMessage`, conversational context, session-based memory, ephemeral vs persistent memory, short-term vs long-term memory, memory strategies (buffer/window/summary/retrieval), context-window limits, memory vs RAG, and memory vs fine-tuning.
- ✅ Part 3: Tools — `@tool`, type hints and docstrings as tool schema, direct tool testing, `bind_tools()`, `AIMessage.tool_calls`, manual tool execution loop, `ToolMessage`, multiple-tool registry, read vs write tools, tool safety, tool vs chain, and tool vs agent.

**Day 29 implementation pattern learned:**

```text
Chains:
Input → Prompt Template → Model → Output Parser → Result

Memory:
History + Current Question → Prompt → Model → Append New Turn → Updated History

Tools:
User → Tool-enabled Model → Tool Call → Application Executes Tool
→ Tool Result / ToolMessage → Model → Final Answer
```

**Day 29 execution note:** Teaching, code walkthroughs, and implementation examples were completed, but separate terminal output confirming each Day 29 local script was not explicitly posted in the chat.

**Day 29 one-pagers:** Completed — Part 1 Chains, Part 2 Memory, Part 3 Tools, plus Day 29 Master one-pager.

**Day 30 status:** Completed — LangGraph Basics, including a successful live conversational-state test.

**Day 30 project:** `projects/day30_langgraph_basics/`

**Day 30 concepts covered:** `StateGraph`, `TypedDict` state schemas, nodes, edges, `START`/`END`, `compile()`, `invoke()`, conditional routing, model nodes, `MessagesState`, `InMemorySaver`, checkpointers, `thread_id`, and thread-scoped conversation state. Distinguished RAM-based checkpointing from durable persistence, and LangGraph orchestration from chains and agents.

**Day 30 practical confirmation:** User ran `persistent_chat.py` using Gemini via LangGraph. First message introduced Syam and GenAI; the second call with the same thread recalled both correctly: “Your name is Syam, and you are learning Generative AI (GenAI)!” An automatic-function-calling (AFC) advisory warning appeared but did not prevent success. This demonstrates conversation continuity within the running process, not persistence after restarting Python. Terminal confirmation was supplied for `persistent_chat.py`; separate execution output for other example files was not provided.

**Day 30 one-pager:** Completed — LangGraph Basics one-pager.

**Day 31 status:** Completed — MCP (Model Context Protocol), including a successful live MCP server/client practical.

**Day 31 project:** `projects/day31_mcp/`

**Day 31 concepts covered:**

- ✅ MCP purpose — open, model-neutral protocol for connecting AI applications to external capabilities.
- ✅ MCP architecture — Host, Client, Protocol, Server, and external systems.
- ✅ Core primitives — Tools, Resources, and Prompts.
- ✅ Tool vs Resource vs Prompt: Tool = DO, Resource = READ, Prompt = GUIDE.
- ✅ Capability discovery through `list_tools()`, `list_resources()`, and `list_prompts()`.
- ✅ Tool invocation through `call_tool()`.
- ✅ Resource access through `read_resource()`.
- ✅ Prompt retrieval/rendering through `get_prompt()`.
- ✅ Typed schemas derived from Python type hints and docstrings.
- ✅ MCP protocol vs MCP Python SDK distinction.
- ✅ MCP vs direct function/tool calling.
- ✅ MCP vs REST APIs.
- ✅ MCP with LangChain, LangGraph, RAG, and future agent workflows.
- ✅ Transport concepts — stdio for local/subprocess integrations and Streamable HTTP for networked/deployed servers.
- ✅ MCP security principles — authentication, authorization, input validation, least privilege, auditability, confirmation for risky actions, and secret management.

**Day 31 practical implementation:**

```text
MCP Client
    ↓
MCP Protocol
    ↓
MCP Server
   /   |   \
Tool Resource Prompt
```

The learning server exposed:

- Tool: `add(a, b)`
- Resource: `guide://genai`
- Prompt: `explain_topic(topic, level)`

**Day 31 live practical confirmation:**

The user ran `projects/day31_mcp/client.py` successfully in the regular `.venv`.

Observed results:

- Protocol version negotiated successfully: `2026-07-28`
- Tool discovery succeeded: `add`
- Tool execution succeeded: `125 + 47 = 172`
- Resource discovery succeeded: `guide://genai`
- Resource reading returned the GenAI roadmap text
- Prompt discovery succeeded: `explain_topic`
- Prompt rendering succeeded for `vector databases` at `beginner` level
- Typed MCP response objects such as `TextContent`, `TextResourceContents`, and `PromptMessage` were returned correctly

A minor prompt-spacing typo (`Usesimple`) was noted as formatting only and did not affect the MCP integration.

**Day 31 one-pager:** Completed — MCP (Model Context Protocol) one-pager.

**Day 32 status:** Completed — AI Agents and Agent Loop, including successful live Gemini agent execution and a successful manually implemented agent loop.

**Day 32 project:** `projects/day32_ai_agents/`

**Day 32 learning breakdown:**

- ✅ Part 1: AI Agents — agent vs normal LLM, agent vs chain, agent vs tool, agent vs LangGraph, agent vs MCP, agent components (model, instructions, tools, state, runtime), `create_agent()`, tool selection, agent action space, multi-step tool use, safety boundaries, and when an agent is appropriate.
- ✅ Part 2: Agent Loop — decide → act → observe → repeat, manual tool-call inspection, tool dispatch, `ToolMessage`, accumulated message state, repeated model calls, tool-call IDs, termination conditions, `MAX_STEPS`, cost/latency implications, tool-error handling, retry limits, human-in-the-loop concepts, and agent-loop evaluation.

**Day 32 Part 1 live practical confirmation:**

The user ran `projects/day32_ai_agents/part1_agent.py` successfully with Gemini `gemini-3.5-flash-lite`.

Observed results included:

- `125 × 47 = 5875`
- `125 + 47 = 172`
- `(50 + 25) × 4 = 300`
- The full agent trace confirmed:
  - `HumanMessage`
  - `AIMessage` requesting `add(a=50, b=25)`
  - `ToolMessage` returning `75`
  - `AIMessage` requesting `multiply(a=75, b=4)`
  - `ToolMessage` returning `300`
  - Final `AIMessage` returning `300` with no further tool calls

This confirmed that the agent dynamically selected the correct tools and executed them in sequence rather than following a hard-coded chain.

**Day 32 Part 2 live practical confirmation:**

The user ran `projects/day32_ai_agents/part2_agent_loop.py` successfully without using the high-level `create_agent()` abstraction.

Observed loop:

```text
STEP 1
Model decision → add(50, 25)
Tool observation → 75

STEP 2
Model decision → multiply(75, 4)
Tool observation → 300

STEP 3
No tool requested
Final answer → 300
```

The practical confirmed the manual agent-loop mechanics:

```text
Current State
→ Model Decision
→ Tool Call?
   ↳ Yes → Execute Tool → Observation → Append ToolMessage → Model Again
   ↳ No  → Final Answer / Stop
```

The final model response contained no tool calls, demonstrating the normal termination condition. The run also showed increasing token usage across successive iterations, reinforcing the relationship between more agent steps, larger state, additional model calls, latency, and cost.

**Day 32 one-pagers:** Completed — Part 1 AI Agents and Part 2 Agent Loop. A Day 32 master one-pager has not yet been created.

**Day 33 roadmap:**

- Part 1: Multi-Agent Systems — NEXT

**Day 16 project status:** LLM Inference & Decoding Playground completed, tested, committed and uploaded. Final verbal project-review questions were intentionally deferred to final interview preparation.

**Day 16 project:** `projects/day16_llm_inference_lab/`

**Project topics implemented:** tokenization inspection, logits/probabilities, manual greedy decoding, beam search, temperature sampling, Top-K, Top-P, KV-cache inspection, and KV-cache performance comparison. Local measured example: 2.8784 s without cache vs 1.2156 s with cache (2.37× speedup; hardware/workload dependent).

**Development setup:**

- Repository: `https://github.com/syamn132/genai-60day-roadmap.git`
- Local repo: `~/Documents/genai-60day-roadmap`
- PyTorch environment: `.venv-pytorch`
- Python: 3.12 environment for PyTorch compatibility on Intel Mac
- PyTorch: 2.2.2
- Transformers: 4.46.3

**Learning workflow:** Continue strictly day-wise and part-wise from this roadmap. Explain concepts first, use checkpoints when useful, and create one-pagers after parts/master days when requested. Do not redo completed days unless requested.

---


🟢 Sprint 0 — Engineering Foundation

✅ Day 1

\- Repository Setup

\- Git Basics

\- GitHub

\- VS Code

\- Engineering Workflow

\- Documentation Structure

\- Learning Roadmap

🟡 Sprint 1 — LLM Foundations

✅ Day 2

\- Introduction to LLMs

\- Traditional Programming vs AI

\- Tokenizer

\- Token IDs

\- Embeddings

\- Context

\- Attention (Concept)

✅ Day 3

\- Query

\- Key

\- Value

\- Query-Key Matching

\- Attention Scores

\- Softmax (Concept)

\- Weighted Values

\- Engineering Assessment

✅ Day 4

\- Why Embeddings aren't enough

\- Query from Embedding

\- Key from Embedding

\- Value from Embedding

\- Wq

\- Wk

\- Wv

\- Learned Transformations

✅ Day 5

\- Matrix Basics

\- Vectors

\- Matrix Multiplication

\- Vector Transformation

\- Q = XWq

\- K = XWk

\- V = XWv

✅ Day 6

\- Dot Product

\- Similarity

\- Q × Kᵀ

\- Attention Score Calculation

✅ Day 7

\- Scaling (√dₖ)

\- Why Scaling is Needed

\- Numerical Stability

✅ Day 8

\- Softmax (Mathematics)

\- Attention Weights

\- Weighted Sum

\- Attention Equation

✅ Day 9

\- Self-Attention

\- Attention Matrix

\- Information Flow

✅ Day 10

\- Multi-Head Attention

\- Multiple Heads

\- Concatenation

\- Output Projection

✅ Day 11

\- Positional Encoding

\- Sin/Cos Encoding

\- Position Information

✅ Day 12

\- Transformer Architecture

\- Encoder

\- Decoder

\- Residual Connections

\- Layer Normalization

✅ Day 13

\- GPT Architecture

\- Decoder-only Transformer

\- Masked Attention

\- Next Token Prediction

✅ Day 14

\- Pretraining

\- Fine-Tuning

\- Transfer Learning

\- RLHF

✅ Day 15

\- Inference

\- Context Window

\- KV Cache

\- Greedy Search

\- Beam Search

\- Temperature

\- Top-K

\- Top-P

✅ Day 16

\- Sprint 1 Revision

\- LLM Interview Questions

\- Mock Interview

\- LLM Mini Project





🔵 Sprint 2 — RAG & Retrieval Engineering

✅ Day 17

\- Embedding Models

\- Embedding APIs

\- Similarity Search

✅ Day 18

\- Vector Databases

\- FAISS

\- ChromaDB

\- Pinecone

✅ Day 19

\- Chunking

\- Metadata

\- Indexing

✅ Day 20

\- Semantic Search

\- Hybrid Search

\- BM25

✅ Day 21

\- Retrieval

\- Top-K Retrieval

\- Context Building

✅ Day 22

\- RAG Architecture

\- End-to-End Flow

✅ Day 23

\- Advanced RAG

\- Query Expansion

\- Compression

\- Reranking

✅ Day 24

\- Production RAG

\- Evaluation

\- Hallucination

\- Guardrails

✅ Day 25

\- Sprint 2 Project

\- Enterprise RAG Chatbot

🟣 Sprint 3 — LLM Frameworks

✅ Day 26

\- Prompt Engineering

\- Prompt Patterns

✅ Day 27

\- OpenAI API

\- Gemini API

\- Claude API

✅ Day 28

\- LangChain Basics

✅ Day 29

\- LangChain Chains

\- Memory

\- Tools

✅ Day 30

\- LangGraph Basics

✅ Day 31

\- MCP (Model Context Protocol)

✅ Day 32

\- AI Agents

\- Agent Loop

⬜ Day 33

\- Multi-Agent Systems

⬜ Day 34

\- Sprint 3 Project

\- Multi-Agent Assistant

🟠 Sprint 4 — Backend Engineering

⬜ Day 35

\- FastAPI Basics

⬜ Day 36

\- REST APIs

\- Dependency Injection

⬜ Day 37

\- PostgreSQL

⬜ Day 38

\- SQLAlchemy

\- Alembic

⬜ Day 39

\- Authentication

\- JWT

\- OAuth

⬜ Day 40

\- Redis

\- Background Tasks

⬜ Day 41

\- Logging

\- Monitoring

\- Error Handling

⬜ Day 42

\- Sprint 4 Project

\- Production Backend

🔴 Sprint 5 — Production Engineering

⬜ Day 43

\- Docker

⬜ Day 44

\- Docker Compose

⬜ Day 45

\- Git Workflow

\- Branching

\- Pull Requests

\- Code Reviews

⬜ Day 46

\- CI/CD

⬜ Day 47

\- Kubernetes Basics

⬜ Day 48

\- AWS Basics

⬜ Day 49

\- Azure Basics

⬜ Day 50

\- Deployment Project

🟢 Sprint 6 — Enterprise Projects

⬜ Day 51

\- Enterprise RAG Chatbot

⬜ Day 52

\- AI Resume Screening System

⬜ Day 53

\- AI Customer Support Agent

⬜ Day 54

\- AI Meeting Assistant

⬜ Day 55

\- AI Research Agent

⬜ Day 56

\- Multi-Agent Enterprise Platform

⬜ Day 57

\- Production Monitoring

⬜ Day 58

\- Debugging Production Issues

⬜ Day 59

\- System Design Interview

\- GenAI Interview

⬜ Day 60

\- Final Capstone Project

\- Resume Review

\- Portfolio Review

\- Mock Interview

\- Job Application Strategy











































**# GenAI Engineer Roadmap**

**### Version 1.0**

**---**

**# Purpose**

This roadmap defines the complete engineering journey from the current skill level to becoming a Production Ready GenAI Engineer capable of performing at approximately a 4-year industry level.

This document is intentionally role-oriented instead of course-oriented.

The objective is not to complete topics.

The objective is to become capable of solving real engineering problems inside a software company.

**---**

**# Final Goal**

At the end of this roadmap I should be capable of:

\- Understanding Jira tickets independently

\- Designing technical solutions

\- Building production-grade GenAI applications

\- Reviewing Pull Requests

\- Debugging production issues

\- Deploying AI systems

\- Working inside an engineering team

\- Clearing Senior GenAI interviews confidently

\- Becoming productive from Day 1 inside a company

**---**

**# Current Assessment**

Current Date:

September 2026

Current Level:

Python

★★★★★★★☆☆☆

SQL

★☆☆☆☆☆☆☆☆☆

Machine Learning

★★★★☆☆☆☆☆☆

Deep Learning

★☆☆☆☆☆☆☆☆☆

Transformers

☆☆☆☆☆☆☆☆☆☆

LLMs

☆☆☆☆☆☆☆☆☆☆

RAG

☆☆☆☆☆☆☆☆☆☆

Agents

☆☆☆☆☆☆☆☆☆☆

FastAPI

☆☆☆☆☆☆☆☆☆☆

Docker

★★☆☆☆☆☆☆☆☆

Git

★★☆☆☆☆☆☆☆☆

Production Engineering

☆☆☆☆☆☆☆☆☆☆

Overall Engineering Readiness

2 / 10

**---**

**# Engineering Philosophy**

Every concept will be learned in the following order.

Business Problem

↓

Why Previous Solution Failed

↓

Core Concept

↓

Internal Working

↓

Implementation

↓

Real Company Usage

↓

Production Considerations

↓

Interview Questions

↓

Coding Exercise

↓

Office Scenario

↓

Manager Review

Memorization is not allowed.

Deep understanding is mandatory.

**---**

**# Engineering Capability Levels**

Level 0

Student

Characteristics

\- Watches tutorials

\- Copies code

\- Depends on documentation

Target Duration

0 Weeks

**---**

Level 1

Junior Engineer

Characteristics

\- Understands concepts

\- Can implement simple tasks

\- Needs guidance

Target

Week 2

**---**

Level 2

Software Engineer

Characteristics

\- Builds complete APIs

\- Understands debugging

\- Writes clean code

Target

Week 4

**---**

Level 3

GenAI Engineer

Characteristics

\- Builds RAG systems

\- Uses LLM APIs

\- Understands Vector Databases

Target

Week 6

**---**

Level 4

Production Engineer

Characteristics

\- Deploys applications

\- Reviews code

\- Handles production issues

\- Works independently

Target

Week 8+

**---**

**# Learning Phases**

**---**

**## Phase 0**

Engineering Mindset

Objective

Stop thinking like a student.

Start thinking like an engineer.

Topics

\- Terminal

\- Git Basics

\- Repository Structure

\- Engineering Documentation

\- Debugging Mindset

Status

✅ Completed

**---**

**## Phase 1**

LLM Foundations

Objective

Understand exactly how ChatGPT works.

Topics

\- Tokenization

\- Token IDs

\- Embeddings

\- Context

\- Attention

\- Transformer

\- Self Attention

\- Query

\- Key

\- Value

\- Positional Encoding

\- Feed Forward Network

\- Decoder

\- GPT Architecture

Current Status

🟡 In Progress

**---**

**## Phase 2**

Software Engineering Foundation

Objective

Build engineering discipline.

Topics

\- Advanced Python

\- OOP

\- Async Programming

\- Logging

\- Exception Handling

\- Testing

\- Packaging

Target

Become capable of writing maintainable production code.

**---**

**## Phase 3**

Backend Engineering

Objective

Build production APIs.

Topics

\- HTTP

\- REST

\- JSON

\- FastAPI

\- Validation

\- Dependency Injection

\- Authentication

\- Authorization

\- Background Tasks

\- WebSockets

Project

Enterprise Backend

**---**

**## Phase 4**

Database Engineering

Topics

\- SQL

\- PostgreSQL

\- Indexes

\- Transactions

\- Optimization

\- ORM

\- Alembic

Project

Production Database

**---**

**## Phase 5**

Machine Learning

Topics

\- Supervised Learning

\- Unsupervised Learning

\- Loss Functions

\- Gradient Descent

\- Optimization

\- Evaluation Metrics

Objective

Understand how models learn.

**---**

**## Phase 6**

Deep Learning

Topics

\- Neural Networks

\- Backpropagation

\- CNN

\- RNN

\- LSTM

\- GRU

\- Optimizers

Objective

Understand why Transformers replaced older architectures.

**---**

**## Phase 7**

GenAI Engineering

Topics

\- Prompt Engineering

\- Embeddings

\- Vector Databases

\- Semantic Search

\- RAG

\- LangChain

\- LangGraph

\- MCP

\- AI Agents

\- Function Calling

\- Structured Output

Projects

Enterprise RAG

Enterprise Agent

SQL Agent

Meeting Assistant

**---**

**## Phase 8**

Production Engineering

Topics

\- Docker

\- Docker Compose

\- CI/CD

\- GitHub Actions

\- Monitoring

\- Logging

\- Observability

\- Scaling

\- Security

\- Cost Optimization

Project

Production Deployment

**---**

**## Phase 9**

System Design

Topics

\- High Level Design

\- Low Level Design

\- AI Architecture

\- Scaling

\- Caching

\- Load Balancing

Objective

Become capable of architecture discussions.

**---**

**## Phase 10**

Enterprise Projects

Projects

1\.

Enterprise AI Platform

**---------------------**

2\.

Enterprise RAG Platform

**---------------------**

3\.

Multi-Agent AI System

**---------------------**

4\.

Recruitment AI Platform

**---------------------**

5\.

SQL AI Agent

**---------------------**

6\.

AI Meeting Assistant

**---------------------**

7\.

Document Intelligence Platform

**---**

**## Phase 11**

Interview Preparation

Objective

Become interview ready.

Includes

\- HR Questions

\- Technical Questions

\- LLD

\- HLD

\- Coding

\- Debugging

\- Live Machine Coding

\- Resume Discussion

\- Project Discussion

**---**

**## Phase 12**

Office Readiness

Objective

Prepare for the first 90 days inside a company.

Topics

\- Jira

\- Git Workflow

\- Branching Strategy

\- Pull Requests

\- Code Reviews

\- Production Bugs

\- Sprint Planning

\- Daily Standups

\- Documentation

\- Knowledge Sharing

**---**

**# Engineering Projects**

The following projects will be built completely from scratch.

Project 1

Enterprise AI Platform

Objective

Learn complete enterprise architecture.

**---**

Project 2

Enterprise RAG

Objective

Learn document retrieval systems.

**---**

Project 3

SQL AI Agent

Objective

Convert natural language into SQL.

**---**

Project 4

Meeting Assistant

Objective

Speech to insights.

**---**

Project 5

Interview Assistant

Objective

Desktop AI application.

**---**

Project 6

Multi-Agent Platform

Objective

Learn orchestration.

**---**

**# Engineering Workflow**

Every project follows the same workflow.

Requirement

↓

Architecture

↓

Database Design

↓

API Design

↓

Implementation

↓

Testing

↓

Git

↓

Pull Request

↓

Review

↓

Bug Fix

↓

Deployment

↓

Monitoring

↓

Retrospective

**---**

**# Weekly Routine**

6 Days Per Week

Daily

\- Learn Concepts

\- Coding

\- Problem Solving

\- Office Scenario

\- Git Practice

Weekly

\- Manager Review

\- Skill Assessment

\- Cheat Sheet Update

\- Documentation Update

**---**

**# Success Criteria**

This roadmap is complete only if I can:

✓ Explain every major GenAI concept from first principles.

✓ Build production-grade APIs.

✓ Build enterprise RAG systems.

✓ Build AI Agents.

✓ Use Git professionally.

✓ Raise Pull Requests.

✓ Review code.

✓ Debug production issues.

✓ Deploy AI applications.

✓ Pass 4-year experience interviews.

✓ Contribute independently inside an engineering team.

**---**

**# Guiding Principle**

Do not learn technologies.

Learn to solve engineering problems.

Technology changes.

Engineering thinking remains valuable.