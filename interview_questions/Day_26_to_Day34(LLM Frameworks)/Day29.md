1. What is a LangChain chain?
A. A chain is a deterministic composition of components where the output of one step becomes the input to the next. For example, a prompt template can feed a language model whose output is then processed by an output parser.
Eg: chain = prompt | model | parser

and chain.invoke(input)  executes the complete workflow.

2. What is memory in an LLM application?
A. Memory is application-managed context that preserves useful information from previous interactions and supplies relevant information to later model calls. The LLM itself does not automatically remember independent API requests; the application manages conversation state and persistence.

3. How would you implement basic conversational memory?
A. Store previous HumanMessage and AIMessage objects, inject them into subsequent prompts through a message-history placeholder, and maintain separate histories per conversation or user session.

4. What is a tool in LangChain?
A. A tool is a callable capability with a defined schema, description, inputs, and outputs that can be exposed to a language model. The model can request a tool call, but the application or agent is responsible for actually executing it and returning the result to the model.

5. What does bind_tools() do?
A. It exposes one or more tool schemas to the chat model so the model can decide whether to request those tools and generate the appropriate arguments.