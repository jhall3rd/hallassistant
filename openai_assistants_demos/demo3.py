import os
import sys
import asyncio

from openai import OpenAI
import dotenv

from util import poll_run_async


def print_messages(messages):
    print("[messages]")
    for message in reversed(list(messages)):
        for item in message.content:
            match item.type:
                case "text":
                    print("text:", item.text.value)
                case _:
                    print(item)
    print("[/messages]")


def print_steps(steps):
    for step in steps:
        print(step)


async def main():
    dotenv.load_dotenv()
    client = OpenAI()

    assistant = client.beta.assistants.create(
        name="Math Tutor",
        instructions="You are a personal math tutor. Write and run code to answer math questions.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-3.5-turbo-1106",
    )

    thread = client.beta.threads.create()

    #

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="I need to solve the equation `6x + 11 = 14`. Can you help me?",
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
    else:
        print(run.status)



if __name__ == "__main__":
    asyncio.run(main())
