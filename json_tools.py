import json


def read_on_key(filename, key, value):
    pass


def import_json_as_dict(filename):
    with open(filename, 'r') as f:
        return json.load(f)
