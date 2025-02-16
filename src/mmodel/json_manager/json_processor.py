
import json


def read_json(path):
    with open(path, 'r') as f:
        json_parsed = json.load(f)
        f.close()
        return json_parsed


def save_file_as_json(path, file: list):
    with open(path, 'w') as f:
        serialized_json = json.dumps(file, indent=4)
        f.write(serialized_json)
        f.close()
