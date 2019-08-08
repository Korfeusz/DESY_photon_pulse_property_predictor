import json


def read_on_key(filename, key, value):
    pass


def import_json_as_dict(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def dump_dict_to_json(filename, contents, indent=None):
    with open(filename, 'w') as f:
        json.dump(contents, f, indent=indent)