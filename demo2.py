import os
import sys
import time

from openai import OpenAI
import dotenv


def print_messages(messages):
    print("[messages]")
    for message in messages:
        for item in message.content:
            match item.type:
                case 'text': print("text:",item.text.value)
                case _: print(item)
    print("[/messages]")

def print_steps(steps):
    for step in steps:
        print(step)

dotenv.load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview",
)

thread = client.beta.threads.create()

# trick question: this has no real solutions, because sin and cos are in range -1..+1, but it does have complex
# solutions. In fact, the range of sine and cos with complex inputs is the whole complex plane.

message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `sin(x) + cos(x) + 11 = 14`. Can you help me?",
)

messages = client.beta.threads.messages.list(thread_id=thread.id)
print_messages(messages)

run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions="Please address the user as Jane Doe. The user has a premium account.",
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
    sys.exit(-1)


run_steps = client.beta.threads.runs.steps.list(thread_id=thread.id, run_id=run.id)
print_steps(run_steps)
