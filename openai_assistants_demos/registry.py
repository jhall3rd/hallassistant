import importlib.resources
import json
from pathlib import Path
from typing import Optional

import openai
from openai.types.beta import Assistant


def retrieve_assistant(client: openai.Client,filename:str) -> Optional[Assistant]:
    path = (importlib.resources.files("openai_assistants_demos").joinpath("assistants") / filename)
    assert isinstance(path,Path)
    path = path.with_suffix('.json')
    if path.exists():
        info = path.read_text(encoding="utf8")
        js = json.loads(info)
        return client.beta.assistants.retrieve(assistant_id = js['assistant_id'])
    else:
        return None


def create_assistant(client: openai.Client, filename, name,description, instructions,model,tools=None) -> Assistant:
    """
    Create an assistant and store it under filename.
:
    """
    if tools is None:
        tools = []
    assistant = client.beta.assistants.create(name=name,
                                              description=description,
                                              instructions=instructions,model=model,tools=tools)
    return save_assistant(assistant,filename)


def save_assistant(assistant, filename):
    desc = dict(name=assistant.name,
                description=assistant.description,
                instructions=assistant.instructions,
                model=assistant.model,
                assistant_id=assistant.id)
    path = (importlib.resources.files("openai_assistants_demos").joinpath("assistants") / filename).with_suffix('.json')
    with path.open(encoding="utf8",mode='w') as out_file:
        json.dump(desc,out_file)
    return assistant


def retrieve_and_save(client,assistant_id,filename) -> Assistant:
    assistant = client.beta.assistants.retrieve(assistant_id=assistant_id)
    return save_assistant(assistant,filename)


def retrieve_or_create(client: openai.Client,
                       filename=None,
                       name = None,
                       description=None,
                       instructions=None,
                       model = None,
                       tools=None,
                       overwrite=False) -> Assistant:
    """
    Either obtain the assistant from our registry or make one.

    :param client: OpenAI client to use.
    :param filename: base name of JSON file which will be stored
    :param name:
    :param instructions:
    :param model:
    :param tools:
    :return:
    """
    retrieved = retrieve_assistant(client,filename)
    if retrieved is None:
        return create_assistant(client, filename, name, description, instructions,model,tools=tools)
    else:
        return retrieved
