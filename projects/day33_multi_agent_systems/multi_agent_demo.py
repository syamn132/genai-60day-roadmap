from langchain.agents import create_agent
from langchain.tools import tool


# Math Tools

@tool
def add(
    a: int,
    b: int,
) -> int:
    """Add two integers."""

    return a + b


@tool
def multiply(
    a: int,
    b: int,
) -> int:
    """Multiply two integers."""

    return a * b


# GenAI Knowledge Tool

@tool
def get_genai_note(
    topic: str,
) -> str:
    """
    Return a short trusted learning note
    for a GenAI concept.
    """

    notes = {
        "agent loop": (
            "An agent loop repeatedly lets a model "
            "decide whether to call a tool or finish. "
            "Tool results are added to state and the "
            "model is called again."
        ),

        "mcp": (
            "Model Context Protocol standardizes how "
            "AI applications connect to external "
            "tools, resources and prompts."
        ),

        "rag": (
            "Retrieval-Augmented Generation retrieves "
            "relevant external information and provides "
            "it as context before generation."
        ),
    }

    normalized = (
        topic
        .strip()
        .lower()
    )

    return notes.get(
        normalized,
        (
            "No trusted note is available "
            "for that topic."
        ),
    )



# Math Agent

MODEL = (
    "google_genai:"
    "gemini-3.5-flash-lite"
)


math_agent = create_agent(
    model=MODEL,

    tools=[
        add,
        multiply,
    ],

    system_prompt=(
        "You are a math specialist. "
        "Solve arithmetic using the provided tools. "
        "Do not guess calculations. "
        "Return only the useful result and "
        "a short explanation."
    ),
)


# GenAI Agent

genai_agent = create_agent(
    model=MODEL,

    tools=[
        get_genai_note,
    ],

    system_prompt=(
        "You are a GenAI learning specialist. "
        "Use get_genai_note for supported concepts. "
        "Explain the retrieved information clearly "
        "and concisely."
    ),
)


# We expose each specialist as a tool to the supervisor.

@tool
def ask_math_agent(
    task: str,
    
) -> str:
    """
    Delegate arithmetic or mathematical
    calculation tasks to the math specialist.
    """

    result = math_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": task,
                }
            ]
        }
    )

    print(
        "\n[MATH AGENT]"
    )

    print(
        "Task:",
        task
    )

    return result[
        "messages"
    ][-1].text


@tool
def ask_genai_agent(
    task: str,
) -> str:
    """
    Delegate GenAI concept questions
    to the GenAI learning specialist.
    """

    result = genai_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": task,
                }
            ]
        }
    )

    print(
        "\n[GENAI AGENT]"
    )

    print(
        "Task:",
        task
    )

    return result[
        "messages"
    ][-1].text



# Supervisor Agent

supervisor = create_agent(
    model=MODEL,

    tools=[
        ask_math_agent,
        ask_genai_agent,
    ],

    system_prompt=(
        "You are a supervisor agent. "

        "Your job is to delegate work to "
        "specialist agents. "

        "Use ask_math_agent for arithmetic "
        "or mathematical tasks. "

        "Use ask_genai_agent for questions "
        "about GenAI concepts. "

        "If the user's request contains both "
        "types of tasks, delegate to both "
        "specialists and combine their results. "

        "Do not perform specialist work yourself "
        "when the appropriate specialist exists."
    ),
)



request = (
    "Calculate (50 + 25) multiplied by 4. "
    "Also explain what an agent loop is."
)


result = supervisor.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": request,
            }
        ]
    }
)


print(
    "\nFINAL ANSWER:"
)

print(
    result["messages"][-1].text
)

print(
    "\n--- SUPERVISOR TRACE ---"
)


for message in result[
    "messages"
]:

    print(
        type(message).__name__
    )

    print(
        message
    )

    print(
        "-" * 60
    )