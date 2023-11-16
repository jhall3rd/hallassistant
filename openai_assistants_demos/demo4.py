"""
Function calling.
"""

import os
import sys
import asyncio
from openai import OpenAI
import dotenv

from util import poll_run_async, print_messages, retrieve_assistant


def print_steps(steps):
    for step in steps:
        print(step)

async def main():
    dotenv.load_dotenv()
    client = OpenAI()

    assistant = retrieve_assistant(client, "demo_weather_bot")



    thread = client.beta.threads.create()

#

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="What's the weather in Point Scramble, New Brunswick?",
    )

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print_messages(messages)

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as Jane Doe. The user has a premium account.",
    )

    run = await poll_run_async(client, thread_id=thread.id, run_id=run.id)

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print_messages(messages)
    elif run.status == "requires_action":
        # make up an answer
        tool_call =run.required_action.submit_tool_outputs.tool_calls[0]
        run = client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread.id,
            run_id=run.id,
            tool_outputs=[
                {
                    "tool_call_id": tool_call.id,
                    "output": "-4C",
                }
            ]
        )
        run = await poll_run_async(client, thread_id=thread.id, run_id=run.id)

        assert run.status == "completed" # maybe not, but error handling is dull.
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print_messages(messages)

    else:
        print(run.status)


if __name__ == "__main__":
    asyncio.run(main())