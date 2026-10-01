from google import genai
from google.genai import errors


client = genai.Client()


try:
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input="Explain RAG in one sentence.",
    )

    print(
        interaction.output_text
    )

except errors.ClientError as error:
    print(
        "Gemini client/API request error:"
    )
    print(error)

except errors.ServerError as error:
    print(
        "Gemini server error:"
    )
    print(error)

except Exception as error:
    print(
        "Unexpected error:"
    )
    print(error)