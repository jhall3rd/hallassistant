import os
import sys
import time

from openai import OpenAI
import dotenv

from util import print_messages
from openai_assistants_demos.registry import retrieve_assistant

dotenv.load_dotenv()
client = OpenAI()


assistant = retrieve_assistant(client,"basic_assistant")


thread = client.beta.threads.create()

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Compose a poem that explains the concept of recursion in programming.",
)

messages = client.beta.threads.messages.list(thread_id=thread.id)
print_messages(messages)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

patience = 180

start = time.perf_counter()

while time.perf_counter() < start + patience:
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    match run.status:
        case "queued" | "in_progress" | "cancelling":
            time.sleep(1.0)
        case "completed":
            break
        case "requires_action":
            print("should be impossible")
            sys.exit(-1)
        case "failed":
            break
        case "cancelled":
            break
        case "expired":
            break

if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    print_messages(messages)
else:
    print(run.status)




