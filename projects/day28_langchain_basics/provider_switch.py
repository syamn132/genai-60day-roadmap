from langchain.chat_models import init_chat_model

PROVIDER = "gemini"

if PROVIDER == "gemini":

    model = init_chat_model(
        "google_genai:gemini-3.5-flash-lite"
    )

elif PROVIDER == "openai":

    model = init_chat_model(
        "openai:gpt-5.5"
    )

elif PROVIDER == "claude":

    model = init_chat_model(
        "claude-sonnet-4-6"
    )

else:
    raise ValueError(
        f"Unsupported provider: {PROVIDER}"
    )

response = model.invoke(
    "Explain embeddings in one sentence."
)

print(response.text)