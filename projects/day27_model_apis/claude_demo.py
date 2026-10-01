import anthropic


client = anthropic.Anthropic()


ticket = """
My payment was deducted,
but the order still shows unpaid.
"""


message = client.messages.create(
    model="claude-haiku-4-5",

    max_tokens=50,

    system="""
You are a customer support ticket classifier.

Allowed categories:

PAYMENT_PENDING
PAYMENT_FAILED
REFUND_DELAY
DELIVERY
OTHER

Return exactly one category and nothing else.
""",

    messages=[
        {
            "role": "user",
            "content": ticket,
        }
    ],
)


for block in message.content:
    if block.type == "text":
        print(block.text)