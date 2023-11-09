"""
This demo shows the use of asyncio to structure client and server interaction
with OpenAI clients.

"""

import asyncio
import os
import dotenv
from openai import OpenAI
from util import poll_run, print_messages


async def run_openai(msg):
    dotenv.load_dotenv()
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    assistant = client.beta.assistants.create(
        instructions="You are a weather bot. Use the provided functions to answer questions.",
        model="gpt-4-1106-preview",
        tools=[{
            "type": "function",
            "function": {
                "name": "getCurrentWeather",
                "description": "Get the weather in location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
                        "unit": {"type": "string", "enum": ["c", "f"]}
                    },
                    "required": ["location"]
                }
            }
        }, {
            "type": "function",
            "function": {
                "name": "getNickname",
                "description": "Get the nickname of a city",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
                    },
                    "required": ["location"]
                }
            }
        }]
    )

    thread = client.beta.threads.create()

    #

    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=msg,
    )

    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print_messages(messages)

    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user as Jane Doe. The user has a premium account.",
    )

    run = await poll_run(client, thread_id=thread.id, run_id=run.id)

    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print_messages(messages)
    elif run.status == "requires_action":
        # make up an answer
        tool_call = run.required_action.submit_tool_outputs.tool_calls[0]
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
        run = await poll_run(client, thread_id=thread.id, run_id=run.id)

        assert run.status == "completed"  # maybe not, but error handling is dull.
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print_messages(messages)
    else:
        print(run.status)
    return "[hj]"





async def server(q_in: asyncio.Queue, q_out: asyncio.Queue):
    """
    Stub for openai LLM.

    :param q_in:
    :param q_out:
    :return:
    """
    while True:
        msg = await q_in.get()
        msg_in = msg[msg.index(" ")+1:]
        msg_out = await run_openai(msg_in)
        await q_out.put(msg_out)


async def client(name: int,
                 q_in: asyncio.Queue,
                 q_out: asyncio.Queue):
    while True:
        try:
            text = input("[H] ").strip()
            if text in ('!q',"bye"):
                break
            elif text:
                await q_out.put(f"[A] {text}")
                msg = await q_in.get()
                print(msg)
        except EOFError:
            break

    print("[A] bye")


async def main():
    q1 = asyncio.Queue()  # messages pass from client to server
    q2 = asyncio.Queue()  # messages pass from server to client

    client1 = asyncio.create_task(client(name=1, q_in=q2, q_out=q1))
    server1 = asyncio.create_task(server(q_in=q1, q_out=q2))
    await asyncio.gather(client1)
    server1.cancel()

if __name__ == "__main__":
    asyncio.run(main())