import asyncio

from mcp import Client

from server import mcp


async def main():

    async with Client(
        mcp
    ) as client:

        # -------------------------
        # Server information
        # -------------------------

        print(
            "\nProtocol version:"
        )

        print(
            client.protocol_version
        )


        # -------------------------
        # TOOLS
        # -------------------------

        tools_result = (
            await client.list_tools()
        )

        print(
            "\nAvailable tools:"
        )

        for tool in tools_result.tools:
            print(
                "-",
                tool.name,
            )


        tool_result = (
            await client.call_tool(
                "add",
                {
                    "a": 125,
                    "b": 47,
                },
            )
        )

        print(
            "\nTool result:"
        )

        print(
            tool_result.content
        )


        # -------------------------
        # RESOURCES
        # -------------------------

        resources_result = (
            await client.list_resources()
        )

        print(
            "\nAvailable resources:"
        )

        for resource in (
            resources_result.resources
        ):
            print(
                "-",
                resource.uri,
            )


        resource_result = (
            await client.read_resource(
                "guide://genai"
            )
        )

        print(
            "\nResource result:"
        )

        print(
            resource_result.contents
        )


        # -------------------------
        # PROMPTS
        # -------------------------

        prompts_result = (
            await client.list_prompts()
        )

        print(
            "\nAvailable prompts:"
        )

        for prompt in (
            prompts_result.prompts
        ):
            print(
                "-",
                prompt.name,
            )


        prompt_result = (
            await client.get_prompt(
                "explain_topic",
                {
                    "topic":
                        "vector databases",

                    "level":
                        "beginner",
                },
            )
        )

        print(
            "\nRendered prompt:"
        )

        print(
            prompt_result.messages
        )


asyncio.run(
    main()
)