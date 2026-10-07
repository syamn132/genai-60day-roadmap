from typing_extensions import TypedDict

from langchain.chat_models import (
    init_chat_model,
)

from langgraph.graph import (
    StateGraph,
    START,
    END,
)


model = init_chat_model(
    "google_genai:gemini-3.5-flash-lite"
)


class State(TypedDict):
    topic: str
    explanation: str


def call_model(
    state: State,
):

    response = model.invoke(
        f"""
Explain {state['topic']}
in exactly 3 concise bullet points.
"""
    )

    return {
        "explanation":
            response.text
    }


builder = StateGraph(
    State
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


graph = builder.compile()


result = graph.invoke(
    {
        "topic": "LangGraph",
        "explanation": "",
    }
)


print(
    result["explanation"]
)