import asyncio

from langchain.agents import create_agent
from langchain.tools import tool

from langgraph.checkpoint.memory import (
    InMemorySaver,
)

from mcp import Client
from mcp.types import TextContent

from mcp_server import mcp


MODEL = (
    "google_genai:"
    "gemini-3.5-flash-lite"
)


@tool
def add(
    a: int,
    b: int,
) -> int:
    """Add two integers."""

    return a + b


@tool
def multiply(
    a: int,
    b: int,
) -> int:
    """Multiply two integers."""

    return a * b



math_agent = create_agent(
    model=MODEL,

    tools=[
        add,
        multiply,
    ],

    system_prompt=(
        "You are the Math Specialist. "
        "Use the provided tools for calculations. "
        "Do not guess arithmetic results. "
        "Return the result with a concise explanation."
    ),

    name="math_agent",
)



async def _read_genai_note(
    topic: str,
) -> str:

    async with Client(
        mcp
    ) as client:

        result = await client.call_tool(
            "get_genai_note",
            {
                "topic": topic
            },
        )

        print(
            f"[MCP CLIENT] Calling get_genai_note({topic})"
        )

        if result.is_error:
            return (
                "MCP knowledge lookup failed."
            )

        for block in result.content:

            if isinstance(
                block,
                TextContent,
            ):
                return block.text

        return (
            "MCP returned no text content."
        )



@tool
def get_sprint3_knowledge(
    topic: str,
) -> str:
    """
    Retrieve a trusted Sprint 3 GenAI note
    through the project's MCP server.
    """

    print(
        f"\n[MCP KNOWLEDGE TOOL] topic={topic}"
    )

    return asyncio.run(
        _read_genai_note(
            topic
        )
    )



genai_agent = create_agent(
    model=MODEL,

    tools=[
        get_sprint3_knowledge,
    ],

    system_prompt=(
        "You are the GenAI Specialist. "

        "For questions about Sprint 3 topics, "
        "use get_sprint3_knowledge whenever "
        "an appropriate topic exists. "

        "Base the explanation on the retrieved "
        "trusted note and explain it clearly. "

        "Do not invent retrieved information."
    ),

    name="genai_agent",
)



@tool
def ask_math_agent(
    task: str,
) -> str:
    """
    Delegate arithmetic calculations
    to the Math Specialist.
    """

    print(
        "\n[MATH AGENT]"
    )

    print(
        "Task:",
        task,
    )


    result = math_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": task,
                }
            ]
        }
    )


    return result[
        "messages"
    ][-1].text


@tool
def ask_genai_agent(
    task: str,
) -> str:
    """
    Delegate Sprint 3 GenAI questions
    to the GenAI Specialist.
    """

    print(
        "\n[GENAI AGENT]"
    )

    print(
        "Task:",
        task,
    )


    result = genai_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": task,
                }
            ]
        }
    )


    return result[
        "messages"
    ][-1].text


checkpointer = InMemorySaver()

supervisor = create_agent(
    model=MODEL,

    tools=[
        ask_math_agent,
        ask_genai_agent,
    ],

    system_prompt=(
        "You are the Supervisor of a "
        "multi-agent GenAI assistant. "

        "Understand the user's overall goal "
        "and delegate specialist work. "

        "Use ask_math_agent for arithmetic. "

        "Use ask_genai_agent for Sprint 3 "
        "GenAI concepts such as RAG, LangChain, "
        "LangGraph, MCP, agents, agent loops "
        "and multi-agent systems. "

        "If a request contains multiple independent "
        "tasks, delegate each task to the correct "
        "specialist and combine the results. "

        "Do not redo specialist calculations or "
        "knowledge work when a specialist is available. "

        "Answer ordinary conversational messages "
        "directly when no specialist is needed."
    ),

    checkpointer=checkpointer,

    name="supervisor",
)