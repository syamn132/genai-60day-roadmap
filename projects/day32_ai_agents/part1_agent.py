from langchain.agents import create_agent
from langchain.tools import tool


# ----------------------------------------
# Tools
# ----------------------------------------

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


tools = [
    add,
    multiply,
]


# ----------------------------------------
# Agent
# ----------------------------------------

agent = create_agent(
    model=(
        "google_genai:"
        "gemini-3.5-flash-lite"
    ),

    tools=tools,

    system_prompt=(
        "You are a helpful calculator assistant. "
        "Use the available tools for arithmetic "
        "instead of guessing calculations. "
        "Return a concise final answer."
    ),
)


# ----------------------------------------
# Invoke
# ----------------------------------------

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content":
                    "Add 50 and 25, "
                    "then multiply the result by 4."
            }
        ]
    }
)


print(
    result["messages"][-1].text
)

print(
    "\n--- AGENT TRACE ---"
)


for message in result[
    "messages"
]:

    print(
        type(message).__name__
    )

    print(
        message
    )

    print(
        "-" * 50
    )