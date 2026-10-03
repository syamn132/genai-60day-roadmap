from langchain.chat_models import init_chat_model

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
)

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
)


model = init_chat_model(
    "google_genai:gemini-3.5-flash-lite"
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful GenAI tutor. "
            "Use the conversation history "
            "when it is relevant.",
        ),

        MessagesPlaceholder(
            variable_name="history"
        ),

        (
            "human",
            "{question}",
        ),
    ]
)


chain = (
    prompt
    | model
)


sessions = {}


def chat(
    session_id: str,
    question: str,
) -> str:

    history = sessions.setdefault(
        session_id,
        [],
    )

    response = chain.invoke(
        {
            "history": history,
            "question": question,
        }
    )

    history.append(
        HumanMessage(
            content=question
        )
    )

    history.append(
        AIMessage(
            content=response.text
        )
    )

    return response.text


SESSION_ID = "syam_session"


print(
    "Type 'exit' to stop."
)


while True:

    question = input(
        "\nYou: "
    ).strip()

    if question.lower() in {
        "exit",
        "quit",
    }:
        break

    if not question:
        continue

    answer = chat(
        SESSION_ID,
        question,
    )

    print(
        "\nAssistant:",
        answer,
    )


print(
    "\n--- FINAL MEMORY ---"
)


for message in sessions[
    SESSION_ID
]:

    print(
        type(message).__name__,
        ":",
        message.content,
    )