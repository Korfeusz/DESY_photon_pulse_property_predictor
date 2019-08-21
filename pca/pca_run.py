import numpy as np
from pca import load_data, load_labels_for_plotting
import json_tools
from functools import reduce
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import tensorflow as tf
import profile_loading

def reshape_codes(codes):
    new_code_shape = reduce(lambda x, y: x*y, codes.shape[1:])
    return np.reshape(codes, newshape=(codes.shape[0], new_code_shape))


if __name__ == '__main__':
    metadata_file = '../metadata/metadata_1.json'
    metadata_dict = json_tools.import_json_as_dict(metadata_file)
    codes_filename = load_data.get_codes_file(metadata_dict)
    codes = np.load(codes_filename)
    codes = reshape_codes(codes)
    profile_indices, code_indices = load_data.get_profile_indices_and_corresponding_code_indices(metadata_dict)
    print(codes.shape)

    pca_model = PCA(n_components=2)
    principal_components = pca_model.fit_transform(codes)
    print(np.shape(principal_components))
    print(pca_model.explained_variance_ratio_)


    model = tf.keras.models.load_model('../model/model_2_biased.h5')
    data_storage_filename = '/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_downsized.npy'
    profiles = profile_loading.get_beam_profiles_from_indices(data_storage_filename, sorted_indices=profile_indices)
    predictions = model.predict_classes(profiles)
    labels = np.array(predictions, dtype=np.bool)
    # labels = np.array(list(load_labels_for_plotting.load_labels(metadata_dict, profile_indices, "experimental_combo")), dtype=np.bool)

    plt.scatter(principal_components[~labels, 0], principal_components[~labels, 1], c='red', s=1)
    plt.scatter(principal_components[labels, 0], principal_components[labels, 1], c='green', s=1, alpha=0.5)

    plt.show()
