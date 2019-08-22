import numpy as np
from pca import load_data, load_labels_for_plotting
import json_tools
from functools import reduce
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tensorflow as tf
import profile_loading

import colorsys


def reshape_codes(codes):
    new_code_shape = reduce(lambda x, y: x*y, codes.shape[1:])
    return np.reshape(codes, newshape=(codes.shape[0], new_code_shape))


def plot_scatter(principal_components, labels, axes=(0, 1)):
    n = len(set(labels))
    hsv = [(x * 1.0 / n, 0.5, 0.5) for x in range(n)]
    rgb = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv))
    for i, label in enumerate(set(labels)):
        mask = labels == label
        plt.scatter(principal_components[mask, axes[0]], principal_components[mask, axes[1]], c=rgb[i], s=0.2, label=label, alpha=0.7)

    plt.legend(markerscale=10)
    plt.show()



def plot_scatter_3d(principal_components, labels):
    n = len(set(labels))
    hsv = [(x * 1.0 / n, 0.5, 0.5) for x in range(n)]
    rgb = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv))
    fig = plt.figure()
    ax = Axes3D(fig)
    for i, label in enumerate(set(labels)):
        mask = labels == label
        ax.scatter(principal_components[mask, 0], principal_components[mask, 1], principal_components[mask, 2], c=rgb[i], s=1)


if __name__ == '__main__':
    metadata_file = '../metadata/metadata_1.json'
    metadata_dict = json_tools.import_json_as_dict(metadata_file)
    codes_filename = load_data.get_codes_file(metadata_dict)
    codes = np.load(codes_filename)
    codes = reshape_codes(codes)
    profile_indices, code_indices = load_data.get_profile_indices_and_corresponding_code_indices(metadata_dict)
    pca_model = PCA(n_components=2)
    principal_components = pca_model.fit_transform(codes)
    print(pca_model.explained_variance_ratio_)


    model = tf.keras.models.load_model('../model/model_2_biased.h5')
    data_storage_filename = '/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_downsized.npy'
    profiles = profile_loading.get_beam_profiles_from_indices(data_storage_filename, sorted_indices=profile_indices)
    predictions = model.predict_classes(profiles)
    plot_scatter(principal_components, predictions)

    run_labels = np.array(list(load_labels_for_plotting.load_run_numbers(metadata_dict, profile_indices)))
    plot_scatter(principal_components, run_labels)

    undulator_translation = [9, 7, 6, 6, 7, 9, 9, 7, 6]
    undulator_labels = np.array(load_labels_for_plotting.translate_run_labels(run_labels, undulator_translation))
    plot_scatter(principal_components, undulator_labels)


    electron_bunch_charge_translations = [0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5]
    electron_bunch_charge_labels = np.array(
        load_labels_for_plotting.translate_run_labels(run_labels, electron_bunch_charge_translations))
    plot_scatter(principal_components, electron_bunch_charge_labels)

    energy_translation = [131, 100, 90, 46, 202, 238, 88, 34, 22]
    energy_labels = np.array(load_labels_for_plotting.translate_run_labels(run_labels, energy_translation))
    plot_scatter(principal_components, energy_labels)

    # plt.scatter(principal_components[~labels, 0], principal_components[~labels, 1], c='red', s=1)
    # plt.scatter(principal_components[labels, 0], principal_components[labels, 1], c='green', s=1, alpha=0.5)

    # plt.show()
