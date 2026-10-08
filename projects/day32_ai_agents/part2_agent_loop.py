from langchain.chat_models import init_chat_model

from langchain.messages import (
    HumanMessage,
    SystemMessage,
    ToolMessage,
)

from langchain.tools import tool


# --------------------------------------------------
# 1. Define tools
# --------------------------------------------------

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


tool_map = {
    tool.name: tool
    for tool in tools
}


# --------------------------------------------------
# 2. Create model
# --------------------------------------------------

model = init_chat_model(
    "google_genai:gemini-3.5-flash-lite"
)


model_with_tools = (
    model.bind_tools(
        tools
    )
)


# --------------------------------------------------
# 3. Initial state
# --------------------------------------------------

messages = [
    SystemMessage(
        content=(
            "You are a calculator assistant. "
            "Use the available tools for "
            "arithmetic calculations. "
            "Do not guess numerical results."
        )
    ),

    HumanMessage(
        content=(
            "Add 50 and 25, "
            "then multiply the result by 4."
        )
    ),
]


# --------------------------------------------------
# 4. Agent loop
# --------------------------------------------------

MAX_STEPS = 10


for step in range(
    1,
    MAX_STEPS + 1,
):

    print(
        f"\n========== STEP {step} =========="
    )


    # ----------------------------------------------
    # DECIDE
    # ----------------------------------------------

    ai_message = (
        model_with_tools.invoke(
            messages
        )
    )


    messages.append(
        ai_message
    )


    print(
        "\nModel output:"
    )

    print(
        ai_message
    )


    # ----------------------------------------------
    # STOP?
    # ----------------------------------------------

    if not ai_message.tool_calls:

        print(
            "\nNo tool requested."
        )

        print(
            "\nFINAL ANSWER:"
        )

        print(
            ai_message.text
        )

        break


    # ----------------------------------------------
    # ACT + OBSERVE
    # ----------------------------------------------

    for tool_call in (
        ai_message.tool_calls
    ):

        tool_name = (
            tool_call["name"]
        )

        tool_args = (
            tool_call["args"]
        )


        print(
            "\nTool requested:"
        )

        print(
            tool_name
        )


        print(
            "Arguments:"
        )

        print(
            tool_args
        )


        selected_tool = (
            tool_map[
                tool_name
            ]
        )


        observation = (
            selected_tool.invoke(
                tool_args
            )
        )


        print(
            "Observation:"
        )

        print(
            observation
        )


        tool_message = ToolMessage(
            content=str(
                observation
            ),
            tool_call_id=(
                tool_call["id"]
            ),
        )


        messages.append(
            tool_message
        )


else:

    print(
        "\nAgent stopped because "
        "MAX_STEPS was reached."
    )