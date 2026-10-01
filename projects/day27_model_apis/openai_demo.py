from openai import OpenAI


client = OpenAI()


response = client.responses.create(
    model="gpt-5.6",

    instructions=(
        "You are a GenAI tutor. "
        "Explain technical concepts clearly "
        "to a junior software engineer."
    ),

    input=(
        "Explain vector databases "
        "in exactly 3 bullet points."
    ),
)


print(response.output_text)