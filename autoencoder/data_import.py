import profile_loading
from beam_profile_metadata import dictionary_tools
import numpy as np


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


def get_data_and_index_under_mask(data, indices, mask):
    return data[mask, :, :], indices[mask]

if __name__ == '__main__':
    import json_tools
    metadata_dict = json_tools.import_json_as_dict('../metadata/metadata_1.json')
    data_storage_filename='/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_lowcolor_downsized.npy'
    profiles, indices = profile_loading.get_all_uncorrupted_profiles_and_indices()
