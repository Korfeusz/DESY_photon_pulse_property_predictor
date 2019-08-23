def insert_keyval_without_overwriting(dictionary: dict, key, value):
    dictionary.setdefault(key)
    dictionary[key] = value


def insert_value_at_end_of_keys(dictionary: dict, keys, value):
    if len(keys) == 1:
        insert_keyval_without_overwriting(dictionary, keys[0], value)
        return
    current_key = keys.pop(0)
    dictionary.setdefault(current_key, {})
    insert_value_at_end_of_keys(dictionary[current_key], keys, value)
