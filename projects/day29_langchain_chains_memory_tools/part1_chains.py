from langchain.chat_models import init_chat_model

from langchain_core.prompts import (
    ChatPromptTemplate,
)

from langchain_core.output_parsers import (
    StrOutputParser,
)


# --------------------------------------------------
# 1. Create model
# --------------------------------------------------

model = init_chat_model(
    "google_genai:gemini-3.5-flash-lite"
)


# --------------------------------------------------
# 2. Create reusable prompt template
# --------------------------------------------------

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a GenAI tutor. "
            "Explain technical concepts clearly "
            "to a junior software engineer.",
        ),
        (
            "human",
            "Explain {topic} in exactly "
            "3 concise bullet points.",
        ),
    ]
)


# --------------------------------------------------
# 3. Create output parser
# --------------------------------------------------

parser = StrOutputParser()


# --------------------------------------------------
# 4. Build chain
# --------------------------------------------------

chain = (
    prompt
    | model
    | parser
)


# --------------------------------------------------
# 5. Invoke chain
# --------------------------------------------------

result = chain.invoke(
    {
        "topic": "vector databases"
    }
)


print(result)