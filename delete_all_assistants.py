import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
assistants =  client.beta.assistants.list()
for assistant in assistants:
    print(assistant)
    client.beta.assistants.delete(assistant_id=assistant.id)