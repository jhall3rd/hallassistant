"""
This is just a generic travel agent.
"""
import json

from dotenv import load_dotenv
from openai import OpenAI
from util import poll_run, UnexpectedStatus

load_dotenv()
client = OpenAI()

class DialogStateTracker:
    def __init__(self,thread):
        self.thread = thread

    def __call__(self,message):
        print(f"I [T:U] {message}")
        return message
    def track_assistant_message(self,message):
        print(f"[T:A] {message}")


def run_conversation():
    assistant = client.beta.assistants.create(
        name="Dialogue tracker",
        instructions="""You are a travel assistant. Use the dialog state tracker to record what you say.""",
        model="gpt-3.5-turbo-1106",
        tools = [
        {
            "type": "function",
            "function": {
                "name": "track_dialogue",
                "description": "Record the dialogue",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "The message sent.",
                        },
                    },
                    "required": ["message"],
                },
            },
        }

    ]
    )

    thread = client.beta.threads.create()
    dst = DialogStateTracker(thread)
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
        run = poll_run(client=client, run_id=run.id, thread_id=thread.id)
        match run.status:

            case "requires_action":
                available_functions = {"track_dialogue": dst}
                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                function_responses = []
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = available_functions[function_name]
                    function_args = json.loads(tool_call.function.arguments)
                    function_response = function_to_call(message=function_args.get("message"))
                    function_responses.append(function_response)

                run = client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread.id,
                    run_id=run.id,
                    tool_outputs=[
                        {"tool_call_id": tool_call.id,
                         "output": function_response}
                        for tool_call, function_response in zip(tool_calls, function_responses)
                    ],
                )
                run = poll_run(client=client, run_id=run.id, thread_id=thread.id)
                messages = client.beta.threads.messages.list(thread_id=thread.id)

                msg =  messages.data[0].content[0].text.value
                dst.track_assistant_message(msg)
                yield msg
            case "completed":
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                msg = messages.data[0].content[0].text.value
                dst.track_assistant_message(msg)
                yield msg
            case _:
                raise UnexpectedStatus(run.status)
        user_message = input("[H] ")


for message in run_conversation():
    print(f"[A] {message}")
