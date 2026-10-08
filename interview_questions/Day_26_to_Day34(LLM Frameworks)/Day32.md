1. What Is an AI Agent?
A. An AI agent is an LLM-based system that receives a goal, uses available context and tools to decide what actions to take, observes the results of those actions, and continues until it can complete the task or produce a final response.

2. Agent vs Chain
A. A chain follows a workflow defined by the developer, while an agent allows the model to dynamically choose actions such as which tool to call, in what order, and whether another step is necessary.

3. Agent vs Tool
A. A tool is an external capability such as a calculator or database lookup. An agent is the decision-making system that chooses when and how to use those tools to accomplish a goal.



4. What is an agent loop?
A. An agent loop is the repeated cycle in which an LLM examines the current state, decides whether to call a tool or return an answer, executes any requested tools, adds their results back to the state, and calls the model again until a termination condition is reached.

5. What Is the Stop Condition?
A. A common stop condition is that the latest model response contains no tool calls and instead returns a final response. Production systems should also enforce deterministic limits such as maximum iterations, timeout, budget, and policy constraints.

6. Why Do Agents Need State?
A. State allows each iteration to see the original user goal, previous model actions, tool calls, tool results, and conversation history. Without state, the model wouldn't know what happened in earlier iterations.

7. Why Use LangGraph for Agents?
A. An agent naturally forms a cyclic graph: model → conditional decision → tool → model. LangGraph provides explicit state, conditional edges, loops, persistence, and control over that workflow.

