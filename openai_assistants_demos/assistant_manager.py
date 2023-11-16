import time

from dotenv import load_dotenv
from openai import OpenAI

from util import print_messages, retrieve_assistant


class Manager:
    load_dotenv()
    def __init__(self):
        self.client = OpenAI()
        self.assistant = retrieve_assistant(self.client,"demo_weather_bot_gpt3")
        thread = self.client.beta.threads.create()
        self.thread_id = thread.id
        self.run_id = None

    def __call__(self,user_message):
        self.client.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=user_message,
        )
        run = self.client.beta.threads.runs.create(thread_id=self.thread_id,assistant_id=self.assistant.id)
        self.run_id = run.id

    @property
    def status(self):
        run = self.client.beta.threads.runs.retrieve(run_id = self.run_id,thread_id=self.thread_id)
        return run.status

    @property
    def messages(self):
        messages = self.client.beta.threads.messages.list(self.thread_id)
        return messages

    @property
    def last_error(self):
        run = self.client.beta.threads.runs.retrieve(run_id=self.run_id, thread_id=self.thread_id)
        return run.last_error


def main():
    manager = Manager()

    user_message = input("[H] ").strip()
    while user_message != '!q':
        manager(user_message=user_message)
        while manager.status != "completed":
            time.sleep(1.0)
            if manager.status == "failed":
                print(manager.last_error)
                break
        print_messages(manager.messages)
        user_message = input("[H] ").strip()


if __name__ == "__main__":
    main()



