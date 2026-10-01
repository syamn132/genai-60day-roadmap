from langchain.chat_models import init_chat_model

from langchain.messages import (
    HumanMessage,
    SystemMessage,
)


model = init_chat_model(
    "google_genai:gemini-3.5-flash-lite",
    temperature=0.2,
)


messages = [
    SystemMessage(
        "You are a GenAI tutor. "
        "Explain technical concepts clearly "
        "to a junior software engineer."
    ),

    HumanMessage(
        "Explain vector databases "
        "in exactly 3 bullet points."
    ),
]


response = model.invoke(
    messages
)


print(response.text)