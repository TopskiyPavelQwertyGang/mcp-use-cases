import asyncio

import ollama
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


MODEL = "qwen3:1.7b"

SERVER = StdioServerParameters(
    command=".venv/bin/python",
    args=["-m", "use_cases.cve_analysis.server"],
)


async def main():
    user_query = "Проверь уязвимости пакета freerdp3"

    print("\n=== LOCAL LLM + MCP DEMO ===\n")
    print(f"USER → {user_query}\n")

    async with stdio_client(SERVER) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools_result = await session.list_tools()

            ollama_tools = []
            for tool in tools_result.tools:
                ollama_tools.append(
                    {
                        "type": "function",
                        "function": {
                            "name": tool.name,
                            "description": tool.description or "",
                            "parameters": tool.input_schema,
                        },
                    }
                )

            print("MCP → available tools:")
            for tool in tools_result.tools:
                print(f"  • {tool.name}")

            messages = [
                {
                    "role": "system",
                    "content": (
                        "Ты агент по анализу уязвимостей пакетов. "
                        "Если для ответа доступны инструменты MCP, используй их. "
                        "Не придумывай CVE и данные об уязвимостях. "
                        "Для поиска уязвимостей пакета используй подходящий инструмент."
                    ),
                },
                {"role": "user", "content": user_query},
            ]

            print(f"\nLLM → deciding what to do ({MODEL})...\n")

            response = ollama.chat(
                model=MODEL,
                messages=messages,
                tools=ollama_tools,
                think=False,
                options={"temperature": 0, "num_predict": 128},
            )

            messages.append(response.message)
            tool_calls = response.message.tool_calls or []

            if not tool_calls:
                print("LLM → no MCP tool selected")
                print(f"\nANSWER → {response.message.content}")
                return

            for call in tool_calls:
                tool_name = call.function.name
                arguments = call.function.arguments or {}

                print(f"LLM → TOOL CALL: {tool_name}")
                print(f"ARGS → {arguments}")

                result = await session.call_tool(tool_name, arguments=arguments)

                result_parts = []
                for item in result.content:
                    if hasattr(item, "text"):
                        result_parts.append(item.text)
                    else:
                        result_parts.append(str(item))

                tool_result = "\n".join(result_parts)

                print("\nMCP → TOOL RESULT:")
                print(tool_result)

                messages.append(
                    {
                        "role": "tool",
                        "tool_name": tool_name,
                        "content": tool_result,
                    }
                )

            print("\nLLM → generating final answer...\n")

            final = ollama.chat(
                model=MODEL,
                messages=messages,
                think=False,
                options={"temperature": 0, "num_predict": 256},
            )

            print("=== FINAL ANSWER ===\n")
            print(final.message.content)


if __name__ == "__main__":
    asyncio.run(main())
