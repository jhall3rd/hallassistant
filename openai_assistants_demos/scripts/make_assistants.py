import openai
import dotenv
from openai import OpenAI

dotenv.load_dotenv()

client = OpenAI()


tracker_assistant = client.beta.assistants.create(
        name="Dialogue tracker (GPT3.5 turbo)",
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