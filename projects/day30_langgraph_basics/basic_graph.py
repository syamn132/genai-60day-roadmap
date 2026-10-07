from typing_extensions import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END,
)


class LearningState(TypedDict):
    topic: str
    explanation: str
    status: str


def create_explanation(
    state: LearningState,
):
    print(
        "Running create_explanation..."
    )

    return {
        "explanation":
            f"You are currently learning "
            f"{state['topic']}."
    }


def mark_complete(
    state: LearningState,
):
    print(
        "Running mark_complete..."
    )

    return {
        "status": "complete"
    }


builder = StateGraph(
    LearningState
)


builder.add_node(
    "create_explanation",
    create_explanation,
)


builder.add_node(
    "mark_complete",
    mark_complete,
)


builder.add_edge(
    START,
    "create_explanation",
)


builder.add_edge(
    "create_explanation",
    "mark_complete",
)


builder.add_edge(
    "mark_complete",
    END,
)


graph = builder.compile()


result = graph.invoke(
    {
        "topic": "LangGraph",
        "explanation": "",
        "status": "",
    }
)


print(
    "\nFinal state:"
)

print(
    result
)