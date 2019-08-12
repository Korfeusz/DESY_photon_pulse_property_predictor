import json_tools


def get_address_and_label_of_train_test_data(metadata_dict: dict, label_name, assignment='train'):
    for index, metadata in metadata_dict.items():
        if "train_test" in metadata and metadata['train_test'] == assignment:
            yield (metadata['address'], metadata['label'][label_name]['value'])


def get_lists_of_addresses_and_labels(metadata_dict: dict, label_name, assignment='train'):
    addresses_and_labels = [(address, label) for address, label in
                            get_address_and_label_of_train_test_data(metadata_dict, label_name,
                                                                     assignment)]
    return list(zip(*addresses_and_labels))


if __name__ == '__main__':
    metadata_dict = json_tools.import_json_as_dict('metadata/meta_test_1.json')
    addresses, labels = get_lists_of_addresses_and_labels(metadata_dict, label_name='experimental_combo', assignment='train')
    print(addresses)
    print(labels)