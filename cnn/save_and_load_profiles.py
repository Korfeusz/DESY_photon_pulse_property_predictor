import json_tools
import profile_loading
import numpy as np


def save_profiles():
    metadata_dict = json_tools.import_json_as_dict('metadata/metadata.json')
    (x_train, y_train), (x_test, y_test) = profile_loading.get_train_test_split_data(metadata_dict,
                                                                                     label_name='experimental_combo',
                                                                                     path_to_data='/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_downsized.npy',
                                                                                     runs=[0, 1, 2, 3, 4, 5, 6, 7, 8])

    print(x_train.shape)
    print(np.shape(y_train[y_train == 1]))
    print(x_test.shape)
    print(np.shape(y_test[y_test == 1]))
    np.save('/beegfs/desy/user/brockhul/preprocessed_data/x_train.npy', x_train)
    np.save('/beegfs/desy/user/brockhul/preprocessed_data/x_test.npy', x_test)
    np.save('/beegfs/desy/user/brockhul/preprocessed_data/y_train.npy', y_train)
    np.save('/beegfs/desy/user/brockhul/preprocessed_data/y_test.npy', y_test)


def load_profiles():
    x_train = np.load('/beegfs/desy/user/brockhul/preprocessed_data/x_train.npy')
    x_test = np.load('/beegfs/desy/user/brockhul/preprocessed_data/x_test.npy')
    y_train = np.load('/beegfs/desy/user/brockhul/preprocessed_data/y_train.npy')
    y_test = np.load('/beegfs/desy/user/brockhul/preprocessed_data/y_test.npy')
    return (x_train, y_train), (x_test, y_test)
