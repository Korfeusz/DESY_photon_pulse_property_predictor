import profile_loading
import json_tools
from cnn import preparatory_tools

if __name__ == '__main__':
    metadata_dict = json_tools.import_json_as_dict('../metadata/meta_test_1.json')
    (x_train, y_train), (x_test, y_test) = profile_loading.get_train_test_split_data(metadata_dict,
                                                                                     label_name='experimental_combo',
                                                                                     path_to_data='../preprocessed_data/beam_profiles_run_{}_raw_small.npy',
                                                                                     runs=[0, 1, 2, 3])
    y_train_1h = preparatory_tools.one_hot(y_train, 2)
    y_test_1h = preparatory_tools.one_hot(y_test, 2)
    print(y_test_1h)