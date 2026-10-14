from mcp.server import MCPServer


mcp = MCPServer(
    "Sprint3 Knowledge Server"
)


GENAI_NOTES = {
    "rag": (
        "Retrieval-Augmented Generation retrieves "
        "relevant external information and provides "
        "it to an LLM as context before generation."
    ),

    "langchain": (
        "LangChain provides reusable abstractions "
        "for models, prompts, tools, messages, "
        "chains and agents."
    ),

    "langgraph": (
        "LangGraph is an orchestration framework "
        "for stateful workflows built using "
        "state, nodes and edges."
    ),

    "mcp": (
        "Model Context Protocol standardizes how "
        "AI applications connect to external tools, "
        "resources and prompts."
    ),

    "agent": (
        "An AI agent receives a goal and dynamically "
        "decides which available actions or tools "
        "to use until the task is complete."
    ),

    "agent loop": (
        "An agent loop repeatedly follows the cycle "
        "decide, act, observe, update state and repeat "
        "until a termination condition is reached."
    ),

    "multi-agent system": (
        "A multi-agent system uses multiple specialized "
        "agents that collaborate, delegate or route work "
        "to solve a larger task."
    ),
}


@mcp.tool()
def get_genai_note(
    topic: str,
) -> str:
    """
    Return a trusted learning note
    for a Sprint 3 GenAI topic.
    """

    normalized = (
        topic
        .strip()
        .lower()
    )

    return GENAI_NOTES.get(
        normalized,
        (
            "No trusted Sprint 3 note "
            f"is available for '{topic}'."
        ),
    )


@mcp.resource(
    "guide://sprint3"
)
def sprint3_guide() -> str:
    """
    Return the Sprint 3 topic sequence.
    """

    return (
        "Sprint 3: "
        "Prompt Engineering → "
        "Model APIs → "
        "LangChain → "
        "LangGraph → "
        "MCP → "
        "AI Agents → "
        "Multi-Agent Systems."
    )