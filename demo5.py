"""
This demo shows the use of asyncio to structure client and server interaction
with OpenAI clients.

"""

import asyncio
import json
import os
import random

import dotenv
import requests
from openai import OpenAI
from util import poll_run


def get_weather(location):
    match location:
        case "London":
            return "12C"
        case "Paris":
            return "15C"
        case "Jakarta":
            return "20C"
        case _:
            return f"{random.randint(0,20)}C"


class Session:
    def __init__(self):
        dotenv.load_dotenv()
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        assistant = client.beta.assistants.create(
            instructions="You are a weather bot. Use the provided functions to answer questions.",
            model="gpt-4-1106-preview",
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "getCurrentWeather",
                        "description": "Get the weather in location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state e.g. San Francisco, CA",
                                },
                                "unit": {"type": "string", "enum": ["c", "f"]},
                            },
                            "required": ["location"],
                        },
                    },
                },
                {
                    "type": "function",
                    "function": {
                        "name": "getNickname",
                        "description": "Get the nickname of a city",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state e.g. San Francisco, CA",
                                },
                            },
                            "required": ["location"],
                        },
                    },
                },
            ],
        )

        thread = client.beta.threads.create()
        self.client, self.assistant, self.thread = client, assistant, thread
        self.run = None

    @property
    def status(self):
        return self.run and self.run.status

    async def start_run(self, message):
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message,
        )

        self.run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions="Please address the user as Alfred Clement.",
        )
        self.run = await poll_run(
            self.client, thread_id=self.thread.id, run_id=self.run.id
        )

    def get_result(self):
        assert self.run.status == "completed"
        messages = self.client.beta.threads.messages.list(thread_id=self.thread.id)
        message = messages.data[0].content[0].text.value
        return message

    async def do_required_action(self):
        assert self.status == "requires_action"
        tool_call = self.run.required_action.submit_tool_outputs.tool_calls[0]
        run = self.client.beta.threads.runs.submit_tool_outputs(
            thread_id=self.thread.id,
            run_id=self.run.id,
            tool_outputs=[
                {
                    "tool_call_id": tool_call.id,
                    "output": get_weather(
                        json.loads(tool_call.function.arguments)["location"]
                    ),
                }
            ],
        )
        self.run = await poll_run(self.client, thread_id=self.thread.id, run_id=run.id)
        return self.get_result()


async def run_server(q_in: asyncio.Queue[str], q_out: asyncio.Queue[str]):
    """
    Stub for openai LLM.

    :param q_in:
    :param q_out:
    :return:
    """
    session = Session()
    while True:
        msg = await q_in.get()
        msg_in = msg[msg.index(" ") + 1 :]
        await session.start_run(msg_in)
        if session.status == "completed":
            msg_out = session.get_result()
        elif session.status == "requires_action":
            msg_out = await session.do_required_action()
        else:
            msg_out = session.status
        await q_out.put(msg_out)


async def run_client(name: int, q_in: asyncio.Queue[str], q_out: asyncio.Queue[str]):
    while True:
        try:
            text = input("[H] ").strip()
            if text in ("!q", "bye"):
                break
            elif text:
                await q_out.put(f"[A] {text}")
                msg = await q_in.get()
                print("[A]", msg)
        except EOFError:
            break

    print("[A] bye")


async def main():
    q1 = asyncio.Queue()  # messages pass from client to server
    q2 = asyncio.Queue()  # messages pass from server to client

    client1 = asyncio.create_task(run_client(name=1, q_in=q2, q_out=q1))
    server1 = asyncio.create_task(run_server(q_in=q1, q_out=q2))
    await asyncio.gather(client1)
    server1.cancel()


if __name__ == "__main__":
    asyncio.run(main())
