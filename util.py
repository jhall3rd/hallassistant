import asyncio
import time


class UnexpectedStatus(ValueError):
    pass


async def poll_run(client,thread_id,run_id, patience = 20):
    start = time.perf_counter()
    while time.perf_counter() < start + patience:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        match run.status:
            case "queued" | "in_progress" | "cancelling":
                await asyncio.sleep(1.0)
            case "completed" | "requires_action" | "failed" | "cancelled" | "expired":
                return run
            case _:
                raise UnexpectedStatus(run.status)


def print_messages(messages):
    print("[messages]")
    for message in reversed(list(messages)):
        for item in message.content:
            match item.type:
                case 'text': print("text:",item.text.value)
                case _: print(item)
    print("[/messages]")
