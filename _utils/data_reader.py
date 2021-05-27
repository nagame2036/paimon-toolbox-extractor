import json


def read_json(path: str):
    with open(path, encoding='utf-8') as file:
        return json.loads(file.read())
