import random
from beam_profile_metadata.tools import dictionary_tools


def generate_profiles_by_label_name(metadata_dict, label_name):
    for profile, data in metadata_dict.items():
        if 'label' in data and label_name in data['label']:
            yield profile


def get_profiles_labeled_specifically(metadata_dict, label_name, label):
    profiles_generator = generate_profiles_by_label_name(metadata_dict, label_name)
    return [p for p in profiles_generator if metadata_dict[p]['label'][label_name]['value'] == label]


def sample_train_test_profiles(metadata_dict, label_name, number_to_sample, ratio_of_1s):
    labeled_1 = get_profiles_labeled_specifically(metadata_dict, label_name, 1)
    labeled_0 = get_profiles_labeled_specifically(metadata_dict, label_name, 0)
    number_of_1s_to_sample, number_of_0s_to_sample = get_number_of_1s_and_0s(number_to_sample,
                                                                             ratio_of_1s,
                                                                             len(labeled_0),
                                                                             len(labeled_1))
    return random.sample(labeled_1, number_of_1s_to_sample), random.sample(labeled_0, number_of_0s_to_sample)


def get_number_of_1s_and_0s(number_to_sample, ratio_of_1s, true_number_of_0s, true_number_of_1s):
    number_of_1s_to_sample = number_to_sample * ratio_of_1s
    if number_of_1s_to_sample > true_number_of_1s:
        number_of_1s_to_sample = true_number_of_1s
    number_of_0s_to_sample = calculate_number_of_0s(ratio_of_1s, number_of_1s_to_sample)
    if number_of_0s_to_sample > true_number_of_0s:
        number_of_0s_to_sample = true_number_of_0s
    return int(number_of_1s_to_sample), int(number_of_0s_to_sample)


def clear_previous_train_test_split(metadata_dict):
    for profile, data in metadata_dict.items():
        dictionary_tools.insert_keyval_without_overwriting(data, key='train_test', value='unused')


def insert_train_test_value(metadata_dict, profiles, value):
    for profile, data in metadata_dict.items():
        if profile in profiles:
            dictionary_tools.insert_keyval_without_overwriting(data, key='train_test', value=value)


def calculate_number_of_0s(ratio_of_1s, number_of_zeros):
    return number_of_zeros * (1 / ratio_of_1s - 1)


def train_test_split(metadata_dict, label_name, number_to_sample, ratio_of_train, ratio_of_1s):
    labeled_1_sample, labeled_0_sample = sample_train_test_profiles(metadata_dict, label_name, number_to_sample, ratio_of_1s)
    clear_previous_train_test_split(metadata_dict)

    number__of_0s_to_sample_as_train = int(len(labeled_0_sample) * ratio_of_train)
    number__of_1s_to_sample_as_train = int(len(labeled_1_sample) * ratio_of_train)

    random.shuffle(labeled_1_sample)
    random.shuffle(labeled_0_sample)

    labeled_1_sample_for_training = labeled_1_sample[:number__of_1s_to_sample_as_train]
    labeled_1_sample_for_testing = labeled_1_sample[number__of_1s_to_sample_as_train:]
    labeled_0_sample_for_training = labeled_0_sample[:number__of_0s_to_sample_as_train]
    labeled_0_sample_for_testing = labeled_0_sample[number__of_0s_to_sample_as_train:]

    insert_train_test_value(metadata_dict, labeled_1_sample_for_training, 'train')
    insert_train_test_value(metadata_dict, labeled_1_sample_for_testing, 'test')
    insert_train_test_value(metadata_dict, labeled_0_sample_for_training, 'train')
    insert_train_test_value(metadata_dict, labeled_0_sample_for_testing, 'test')

