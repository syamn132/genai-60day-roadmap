from langchain.chat_models import (
    init_chat_model,
)

from langgraph.checkpoint.memory import (
    InMemorySaver,
)

from langgraph.graph import (
    StateGraph,
    MessagesState,
    START,
    END,
)


model = init_chat_model(
    "google_genai:gemini-3.5-flash-lite"
)


def call_model(
    state: MessagesState,
):

    response = model.invoke(
        state["messages"]
    )

    return {
        "messages": [
            response
        ]
    }


builder = StateGraph(
    MessagesState
)


builder.add_node(
    "call_model",
    call_model,
)


builder.add_edge(
    START,
    "call_model",
)


builder.add_edge(
    "call_model",
    END,
)


checkpointer = InMemorySaver()


graph = builder.compile(
    checkpointer=checkpointer
)


config = {
    "configurable": {
        "thread_id":
            "syam-session-1"
    }
}


first = graph.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content":
                    "My name is Syam "
                    "and I am learning GenAI.",
            }
        ]
    },
    config,
)


print(
    "First response:"
)

print(
    first["messages"][-1].content
)


second = graph.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content":
                    "What is my name "
                    "and what am I learning?",
            }
        ]
    },
    config,
)


print(
    "\nSecond response:"
)

print(
    second["messages"][-1].content
)