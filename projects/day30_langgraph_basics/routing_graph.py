from typing import Literal

from typing_extensions import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END,
)


class State(TypedDict):
    question: str
    difficulty: str
    answer: str


def classify(
    state: State,
):
    question = state[
        "question"
    ]

    if len(
        question.split()
    ) <= 5:

        difficulty = "simple"

    else:

        difficulty = "detailed"

    return {
        "difficulty":
            difficulty
    }


def route(
    state: State,
) -> Literal[
    "simple_answer",
    "detailed_answer",
]:

    return (
        "simple_answer"
        if state["difficulty"]
        == "simple"
        else "detailed_answer"
    )


def simple_answer(
    state: State,
):
    return {
        "answer":
            "Short explanation."
    }


def detailed_answer(
    state: State,
):
    return {
        "answer":
            "Detailed explanation "
            "with more context."
    }


builder = StateGraph(
    State
)


builder.add_node(
    "classify",
    classify,
)

builder.add_node(
    "simple_answer",
    simple_answer,
)

builder.add_node(
    "detailed_answer",
    detailed_answer,
)


builder.add_edge(
    START,
    "classify",
)


builder.add_conditional_edges(
    "classify",
    route,
    [
        "simple_answer",
        "detailed_answer",
    ],
)


builder.add_edge(
    "simple_answer",
    END,
)

builder.add_edge(
    "detailed_answer",
    END,
)


graph = builder.compile()


result = graph.invoke(
    {
        "question":
            "Explain RAG",
        "difficulty": "",
        "answer": "",
    }
)


print(
    result
)