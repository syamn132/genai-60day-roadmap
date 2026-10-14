from agents import supervisor


THREAD_ID = (
    "syam-day34-session"
)


config = {
    "configurable": {
        "thread_id":
            THREAD_ID
    }
}


print(
    "=" * 65
)

print(
    "SPRINT 3 MULTI-AGENT ASSISTANT"
)

print(
    "Math + GenAI + MCP + Memory"
)

print(
    "Type 'exit' to stop."
)

print(
    "=" * 65
)


while True:

    user_input = input(
        "\nYou: "
    ).strip()


    if user_input.lower() in {
        "exit",
        "quit",
    }:
        break


    if not user_input:
        continue


    result = supervisor.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                }
            ]
        },

        config=config,
    )


    final_message = (
        result["messages"][-1]
    )


    print(
        "\nAssistant:"
    )

    print(
        final_message.text
    )
    