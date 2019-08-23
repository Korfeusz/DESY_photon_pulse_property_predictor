import numpy as np
from pca import load_data, load_labels_for_plotting
import json_tools
from functools import reduce
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import tensorflow as tf
import profile_loading
import matplotlib.cm as cm
import colorsys


def reshape_codes(codes):
    new_code_shape = reduce(lambda x, y: x * y, codes.shape[1:])
    return np.reshape(codes, newshape=(codes.shape[0], new_code_shape))


def plot_scatter(principal_components, labels, axes=(0, 1), title=None, sort_colors=False, save=None):
    n = len(set(labels))
    rgb = cm.rainbow(np.linspace(0.0, 1.0, n))
    if sort_colors:
        sorting_dict = dict([(x, y) for x, y in zip(sorted(set(labels)), range(len(set(labels))))])
        rgb = [rgb[sorting_dict[x]] for x in set(labels)]
    for i, label in enumerate(set(labels)):
        mask = labels == label
        plt.scatter(principal_components[mask, axes[0]], principal_components[mask, axes[1]], c=rgb[i], s=0.2,
                    label=label, alpha=0.7)

    plt.title(title)
    plt.legend(markerscale=30)
    if save is not None:
        plt.savefig(save)
    plt.show()


def plot_scatter_continuous(principal_components, continuous_labels, title=None, save=None):
    rgb = cm.rainbow(np.linspace(0.0, 1.0, len(continuous_labels)))
    sorting_dict = dict([(x, y) for x, y in zip(sorted(continuous_labels), range(len(continuous_labels)))])
    rgb = [rgb[sorting_dict[x]] for x in continuous_labels]
    plt.scatter(principal_components[:, 0], principal_components[:, 1], c=rgb, s=0.2)
    plt.title(title)
    if save is not None:
        plt.savefig(save)
    plt.show()

def plot_scatter_3d(principal_components, labels):
    n = len(set(labels))
    hsv = [(x * 1.0 / n, 0.5, 0.5) for x in range(n)]
    rgb = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv))
    fig = plt.figure()
    ax = Axes3D(fig)
    for i, label in enumerate(set(labels)):
        mask = labels == label
        ax.scatter(principal_components[mask, 0], principal_components[mask, 1], principal_components[mask, 2],
                   c=rgb[i], s=1)


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

    save_dir = '../pca_plots/r3/{}'

    model = tf.keras.models.load_model('../model/model_2_biased.h5')
    data_storage_filename = '/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_downsized.npy'
    profiles = profile_loading.get_beam_profiles_from_indices(data_storage_filename, sorted_indices=profile_indices)
    predictions = model.predict_classes(profiles)
    plot_scatter(principal_components, predictions, axes=(0, 1),
                 title='PCA with predicted circularity labels', save=save_dir.format('circularity'))

    run_labels = np.array(list(load_labels_for_plotting.load_run_numbers(metadata_dict, profile_indices)))
    plot_scatter(principal_components, run_labels, axes=(0, 1), title='PCA with run numbers')

    undulator_translation = [9, 7, 6, 6, 7, 9, 9, 7, 6]
    undulator_labels = np.array(load_labels_for_plotting.translate_run_labels(run_labels, undulator_translation))
    plot_scatter(principal_components, undulator_labels, axes=(0, 1), title='PCA with undulator number',
                 sort_colors=True, save=save_dir.format('undulators'))

    electron_bunch_charge_translations = [0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5]
    electron_bunch_charge_labels = np.array(
        load_labels_for_plotting.translate_run_labels(run_labels, electron_bunch_charge_translations))
    plot_scatter(principal_components, electron_bunch_charge_labels, axes=(0, 1),
                 title='PCA with electron bunch charges [nC]', save=save_dir.format('e_bunch'))

    energy_translation = [131, 100, 90, 46, 202, 238, 88, 34, 22]
    energy_labels = np.array(load_labels_for_plotting.translate_run_labels(run_labels, energy_translation))
    plot_scatter(principal_components, energy_labels, axes=(0, 1), sort_colors=True, title='PCA with energies [uJ]',
                 save=save_dir.format('energy'))

    intensities = load_labels_for_plotting.load_intensities(profiles)
    plot_scatter_continuous(principal_components, intensities, title='PCA with profile intensities',
                            save=save_dir.format('intensities'))
