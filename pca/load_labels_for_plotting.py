import numpy as np


def load_labels(metadata_dict, indices, label_name):
    for index in indices:
        if 'label' in metadata_dict[index] and label_name in metadata_dict[index]['label']:
            yield metadata_dict[index]['label'][label_name]['value']


def load_run_numbers(metadata_dict, indices):
    for index in indices:
        yield metadata_dict[index]['address']['run']


def translate_run_labels(labels, translation):
    return [translation[x] for x in labels]


def load_intensities(profiles):
    return np.sum(np.sum(profiles, axis=2), axis=1)
