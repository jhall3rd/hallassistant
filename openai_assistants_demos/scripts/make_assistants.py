import openai
import dotenv
from openai import OpenAI

from openai_assistants_demos.registry import retrieve_or_create

dotenv.load_dotenv()

client = OpenAI()


assistants = [
    {
        "filename": "basic_assistant.json",
        "name": "Basic Assistant",
        "description": "",
        "instructions": "",
        "model": "gpt-3.5-turbo-1106",
    },
    {
        "filename":"demo_weather_bot.json",
        "name": "Demo Weather Bot",
        "description": "",
        "instructions": "You are a weather bot. Use the provided functions to answer questions.",
        "model": "gpt-4-1106-preview",
    },
    {
        "filename": "demo_weather_bot_gpt3.json",
        "name": "Weather Advisor (GPT3)",
        "description": "",
        "instructions": "Discuss the weather.",
        "model": "gpt-3.5-turbo-1106",
    },
    {
        "filename": "math_assistant_tutor.json",
        "name": "Math Assistant Tutor",
        "description": "",
        "instructions": "You are a personal math tutor. Write and run code to answer math questions.\n",
        "model": "gpt-3.5-turbo-1106",
    },
    {
        "filename": "math_tutor.json",
        "name": "Math Tutor",
        "description": "",
        "instructions": "You are a personal math tutor. Write and run code to answer math questions.\n",
        "model": "gpt-4-1106-preview",
    },
    {
        "filename": "tracker_assistant_gpt_3.json",
        "name": "Dialogue tracker (GPT3.5 turbo)",
        "description": "",
        "instructions": "You are a travel assistant. Use the dialog state tracker to record what you say.",
        "model": "gpt-3.5-turbo-1106",
    },
    {
        "filename":"travel_assistant_gpt_35_turbo.json",
        "name": "Travel assistant",
        "description": "",
        "instructions": "You are a travel booking agent.",
        "model": "gpt-3.5-turbo-1106",
    },
]

for assistant in assistants:
    print(retrieve_or_create(client,**assistant))