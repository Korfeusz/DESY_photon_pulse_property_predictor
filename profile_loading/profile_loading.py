import json_tools
import numpy as np
from contextlib import suppress


def get_train_test_split_data(metadata_dict, label_name, path_to_data, runs=list(range(9))):
    labels_and_profiles_train = get_labels_and_profiles_list(metadata_dict, label_name=label_name, assignment='train', runs=runs)
    labels_and_profiles_test = get_labels_and_profiles_list(metadata_dict, label_name=label_name, assignment='test', runs=runs)
    return get_x_y_data(labels_and_profiles_train, path_to_data), get_x_y_data(labels_and_profiles_test, path_to_data)


def get_address_and_label_of_train_test_data(metadata_dict: dict, label_name, assignment='train'):
    for index, metadata in metadata_dict.items():
        if "train_test" in metadata and metadata['train_test'] == assignment:
            yield {'run_number': metadata['address']['run'],
                   'profile_number': metadata['address']['profile_number'],
                   'label': metadata['label'][label_name]['value']}


def get_labels_and_profiles_list(metadata_dict: dict, label_name, assignment='train', runs=list(range(9))):
    output_list = [{'labels': [], 'profiles': []} for _ in runs]
    for data in get_address_and_label_of_train_test_data(metadata_dict, label_name, assignment):
        output_list[data['run_number']]['labels'].append(data['label'])
        output_list[data['run_number']]['profiles'].append(data['profile_number'])
    return output_list


def get_placeholder_images_from_first_run(beam_profiles, labels_and_profiles):
    image_shape = beam_profiles.shape[-2:]
    number_of_profiles_to_import = sum([len(x['profiles']) for x in labels_and_profiles])
    return np.zeros(shape=(number_of_profiles_to_import, image_shape[0], image_shape[1]))


def insert_new_profiles_to_placeholder(beam_profiles, access_dict, image_index, images):
    imported_profiles = beam_profiles[access_dict['profiles']]
    number_of_imported_profiles = len(access_dict['profiles'])
    images[image_index:(number_of_imported_profiles + image_index)] = imported_profiles
    image_index += number_of_imported_profiles
    return image_index


def get_x_y_data(labels_and_profiles, path_to_data):
    labels = []
    image_index = 0
    for run_number, access_dict in enumerate(labels_and_profiles):
        beam_profiles = np.load(path_to_data.format(run_number))
        if run_number == 0:
            images = get_placeholder_images_from_first_run(beam_profiles, labels_and_profiles)
        labels.extend(access_dict['labels'])
        image_index = insert_new_profiles_to_placeholder(beam_profiles, access_dict, image_index, images)
    return images, np.array(labels)




if __name__ == '__main__':
    metadata_dict = json_tools.import_json_as_dict('metadata/meta_test_1.json')
    (x_train, y_train), (x_test, y_test) = get_train_test_split_data(metadata_dict, label_name='experimental_combo',
                                                                     path_to_data='preprocessed_data/beam_profiles_run_{}_raw_small.npy',
                                                                     runs=[0, 1, 2, 3])
