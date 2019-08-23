import profile_loading
import numpy as np


# def save_profiles():
#     metadata_dict = json_tools.import_json_as_dict('metadata/metadata_1.json')
#     (x_train, y_train), (x_test, y_test) = profile_loading.get_train_test_split_data(metadata_dict,
#                                                                                      label_name='experimental_combo',
#                                                                                      path_to_data='/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_downsized.npy',
#                                                                                      runs=[0, 1, 2, 3, 4, 5, 6, 7, 8])
#     np.save('/beegfs/desy/user/brockhul/preprocessed_data/x_train.npy', x_train)
#     np.save('/beegfs/desy/user/brockhul/preprocessed_data/x_test.npy', x_test)
#     np.save('/beegfs/desy/user/brockhul/preprocessed_data/y_train.npy', y_train)
#     np.save('/beegfs/desy/user/brockhul/preprocessed_data/y_test.npy', y_test)


def save_and_return_profiles(save_directory, metadata_dict, label_name, path_to_data):
    (x_train, y_train), (x_test, y_test) = profile_loading.get_train_test_split_data(metadata_dict,
                                                                                     label_name=label_name,
                                                                                     path_to_data=path_to_data,
                                                                                     runs=[0, 1, 2, 3, 4, 5, 6, 7, 8])
    np.save('{}/x_train.npy'.format(save_directory), x_train)
    np.save('{}/x_train.npy'.format(save_directory), x_test)
    np.save('{}/x_train.npy'.format(save_directory), y_train)
    np.save('{}/x_train.npy'.format(save_directory), y_test)
    return (x_train, y_train), (x_test, y_test)


def load_profiles(directory):
    x_train = np.load('{}/x_train.npy'.format(directory))
    x_test = np.load('{}/x_test.npy'.format(directory) )
    y_train = np.load('{}/y_train.npy'.format(directory))
    y_test = np.load('{}/y_test.npy'.format(directory))
    return (x_train, y_train), (x_test, y_test)


def load_train_test_split_data(data_save_directory, metadata_dict=None, label_name=None, path_to_profiles=None):
    try:
        return load_profiles(data_save_directory)
    except IOError:
        return save_and_return_profiles(data_save_directory, metadata_dict, label_name, path_to_profiles)
