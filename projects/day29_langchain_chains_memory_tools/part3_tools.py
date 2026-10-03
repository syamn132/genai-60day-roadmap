from langchain.chat_models import (
    init_chat_model,
)

from langchain.tools import tool


@tool
def multiply(
    a: int,
    b: int,
) -> int:
    """Multiply two integers."""

    return a * b


@tool
def add(
    a: int,
    b: int,
) -> int:
    """Add two integers."""

    return a + b


tools = [
    multiply,
    add,
]


tool_map = {
    tool.name: tool
    for tool in tools
}


model = init_chat_model(
    "google_genai:gemini-3.5-flash-lite"
)


model_with_tools = model.bind_tools(
    tools
)


messages = [
    {
        "role": "user",
        "content": (
            "Multiply 125 by 47."
        ),
    }
]


ai_message = model_with_tools.invoke(
    messages
)


messages.append(
    ai_message
)


print(
    "Tool calls:",
    ai_message.tool_calls,
)


for tool_call in ai_message.tool_calls:

    selected_tool = tool_map[
        tool_call["name"]
    ]

    tool_result = (
        selected_tool.invoke(
            tool_call
        )
    )

    messages.append(
        tool_result
    )


final_response = (
    model_with_tools.invoke(
        messages
    )
)


print(
    "\nFinal answer:"
)

print(
    final_response.text
)