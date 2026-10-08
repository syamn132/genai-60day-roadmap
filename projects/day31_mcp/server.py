from mcp.server import MCPServer


mcp = MCPServer(
    "Day31 GenAI Learning Server"
)


# -----------------------------------
# TOOL
# -----------------------------------

@mcp.tool()
def add(
    a: int,
    b: int,
) -> int:
    """Add two integers."""

    return a + b


# -----------------------------------
# RESOURCE
# -----------------------------------

@mcp.resource(
    "guide://genai"
)
def genai_guide() -> str:
    """Return a short GenAI roadmap guide."""

    return (
        "GenAI roadmap: "
        "LLM foundations → "
        "RAG → "
        "LangChain → "
        "LangGraph → "
        "MCP → "
        "Agents."
    )


# -----------------------------------
# PROMPT
# -----------------------------------

@mcp.prompt()
def explain_topic(
    topic: str,
    level: str = "beginner",
) -> str:
    """Create a GenAI tutoring prompt."""

    return (
        f"Explain {topic} to a "
        f"{level} GenAI learner. "
        f"Use simple language and "
        f"one practical example."
    )