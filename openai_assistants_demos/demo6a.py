"""
Original example of parallel function calling from openai.
Adjusted to work with dotenv.
"""
import time

from dotenv import load_dotenv
from openai import OpenAI
import json

from openai_assistants_demos.util import retrieve_assistant

load_dotenv()
client = OpenAI()

def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": "celsius"})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": "fahrenheit"})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": "celsius"})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})


def poll_run(run, thread):
    patience = 20
    start = time.perf_counter()
    while time.perf_counter() < start + patience:
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        match run.status:
            case "queued" | "in_progress" | "cancelling":
                time.sleep(1.0)
            case "completed" | "requires_action":
                break
            case "failed":
                break
            case "cancelled":
                break
            case "expired":
                break
    return run


def run_conversation():
    # Step 1: create the assistant
    assistant = retrieve_assistant(client, "demo_weather_bot_gpt3")
    # Step 2: make a thread in which to keep the conversation
    thread = client.beta.threads.create()

    # Step 3: create a message that triggers function calling.
    client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="What's the weather like in San Francisco, Tokyo, and Paris?",
    )

    # step 4: create and schedule the run
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
        instructions="Please address the user in German.",)
    run = poll_run(run, thread=thread)
    match run.status:
        case "requires_action":
            # call the functions
            available_functions = {
                "get_current_weather": get_current_weather,
            }
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            function_responses = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(location=function_args.get("location"),
                                                     unit=function_args.get("unit"),
                                                     )
                function_responses.append(function_response)

            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=[
                        {"tool_call_id": tool_call.id,
                         "output": function_response}
                        for tool_call,function_response in zip(tool_calls,function_responses)
                ],
            )
            run = poll_run(run,thread=thread)
            run_steps = client.beta.threads.runs.steps.list(
                thread_id=thread.id,
                run_id=run.id
            )
            for run_step in run_steps:
                match run_step.type:
                    case "message_creation":
                        print(run_step.type,
                              run_step.step_details.message_creation.message_id)
                    case "tool_calls":
                        for tool_call in   run_step.step_details.tool_calls:
                            match tool_call.type:
                                case "function":
                                    print(run_step.type,tool_call.function)
                                case "code":
                                    print(run_step)


            messages = client.beta.threads.messages.list(thread_id=thread.id)
            return  messages.data[0].content[0].text.value

        case "completed":
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            return messages.data[0].content[0].text.value



print(run_conversation())