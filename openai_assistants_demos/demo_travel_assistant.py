"""
This is just a generic travel agent.
"""

from dotenv import load_dotenv
from openai import OpenAI
from util import poll_run, UnexpectedStatus, retrieve_assistant

load_dotenv()
client = OpenAI()

def run_conversation():


    assistant  = retrieve_assistant(client, 'travel_assistant_gpt_35_turbo')

    thread = client.beta.threads.create()
    user_message = input("[H] ")

    while user_message.strip() != "!q":
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message,
        ),

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )
        run = poll_run(client=client, run=run, thread=thread, patience=60)
        match run.status:
            case "completed":
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                yield messages.data[0].content[0].text.value
            case _:
                raise UnexpectedStatus(run.status)
        user_message = input("[H] ")


for message in run_conversation():
    print(f"[A] {message}")
