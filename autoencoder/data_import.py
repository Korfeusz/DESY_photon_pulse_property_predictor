import profile_loading
from beam_profile_metadata import dictionary_tools
import numpy as np
import json_tools


def cut_data_to_size(data, image_shape=(32, 32)):
    return data[:, :image_shape[0], :image_shape[1]]


def create_train_test_split_mask(length_of_profiles, fraction_of_train):
    idx = np.arange(length_of_profiles)
    np.random.shuffle(idx)
    mask = np.zeros(length_of_profiles)
    number_of_train_data = int(fraction_of_train * length_of_profiles)
    mask[idx[:number_of_train_data]] = 1
    return mask.astype(np.int)


def get_train_test_split_labels(train_test_split_mask):
    return ['train' if m == 1 else 'test' for m in train_test_split_mask]


def insert_autoencoder_train_test_label(indices, metadata_dict, train_test_split_mask):
    train_test_split_labels = get_train_test_split_labels(train_test_split_mask)
    for label, index in zip(train_test_split_labels, indices):
        dictionary_tools.insert_value_at_end_of_keys(metadata_dict[index], ['autoencoder', 'train_test'], label)


def get_train_test_mask_from_indices(indices, metadata_dict):
    mask = []
    for index in indices:
        if 'autoencoder' in metadata_dict[index]:
            mask.append(metadata_dict[index]['autoencoder']['train_test'])
    return np.array([True if m == 'train' else False for m in mask])


def get_train_test_split_data(data_storage_filename, metadata_dict, normalize, cut_to, reshape):
    profiles, indices = profile_loading.get_all_uncorrupted_profiles_and_indices(data_storage_filename, metadata_dict)
    mask = get_train_test_mask_from_indices(indices, metadata_dict)
    profiles = cut_data_to_size(profiles, cut_to)
    if normalize:
        profiles = minmax_imagewise(profiles)
    if reshape:
        shape = profiles.shape
        profiles = np.reshape(profiles, (shape[0], shape[1], shape[2], 1))
    return (profiles[mask], indices[mask]), (profiles[~mask], indices[~mask]), (profiles, indices)


def minmax_imagewise(profiles):
    return profiles.astype('float16') / np.max(np.max(profiles, axis=1), axis=1).reshape((profiles.shape[0], 1, 1))


def create_autoencoder_label(data_storage_filename, metadata_filename, fraction_of_train):
    metadata_dict = json_tools.import_json_as_dict(metadata_filename)
    profiles, indices = profile_loading.get_all_uncorrupted_profiles_and_indices(data_storage_filename, metadata_dict)
    train_test_split_mask = create_train_test_split_mask(len(indices), fraction_of_train=fraction_of_train)
    insert_autoencoder_train_test_label(indices, metadata_dict, train_test_split_mask)
    json_tools.dump_dict_to_json(metadata_filename, metadata_dict, indent=2)


if __name__ == '__main__':
    data_storage_filename = '/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_lowcolor_downsized.npy'
    metadata_filename = '../metadata/metadata_1.json'
    create_autoencoder_label(data_storage_filename, metadata_filename, fraction_of_train=0.8)
