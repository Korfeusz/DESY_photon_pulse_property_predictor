import random
from beam_profile_metadata import dictionary_tools


def generate_profiles_by_label_name(metadata_dict, label_name):
    for profile, data in metadata_dict.items():
        if 'label' in data and label_name in data['label']:
            yield profile


def get_profiles_labeled_specifically(metadata_dict, label_name, label):
    profiles_generator = generate_profiles_by_label_name(metadata_dict, label_name)
    return [p for p in profiles_generator if metadata_dict[p]['label'][label_name]['value'] == label]


def sample_train_test_profiles(metadata_dict, label_name, number_to_sample):
    labeled_1 = get_profiles_labeled_specifically(metadata_dict, label_name, 1)
    labeled_0 = get_profiles_labeled_specifically(metadata_dict, label_name, 0)
    if number_to_sample > len(labeled_1):
        number_to_sample = len(labeled_1)
    if number_to_sample > len(labeled_0):
        number_to_sample = len(labeled_0)
    return random.sample(labeled_1, number_to_sample), random.sample(labeled_0, number_to_sample)


def clear_previous_train_test_split(metadata_dict):
    for profile, data in metadata_dict.items():
        dictionary_tools.insert_keyval_without_overwriting(data, key='train_test', value=False)


def insert_train_test_value(metadata_dict, profiles, value):
    for profile, data in metadata_dict.items():
        if profile in profiles:
            dictionary_tools.insert_keyval_without_overwriting(data, key='train_test', value=value)


def train_test_split(metadata_dict, label_name, number_to_sample):
    labeled_1_sample, labeled_0_sample = sample_train_test_profiles(metadata_dict, label_name, number_to_sample)
    clear_previous_train_test_split(metadata_dict)
    insert_train_test_value(metadata_dict, labeled_1_sample, True)
    insert_train_test_value(metadata_dict, labeled_0_sample, True)
