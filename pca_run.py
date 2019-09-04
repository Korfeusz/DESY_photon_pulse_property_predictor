import numpy as np
from pca import load_data, load_labels_for_plotting
import json_tools
from sklearn.decomposition import PCA
import tensorflow as tf
import profile_loading
from pca.pca_plots import plot_scatter, plot_scatter_continuous
from pca.tools import reshape_codes

if __name__ == '__main__':
    metadata_file = 'metadata/metadata.json'
    metadata_dict = json_tools.import_json_as_dict(metadata_file)
    codes_filename = load_data.get_codes_file(metadata_dict)
    codes = np.load(codes_filename)
    codes = reshape_codes(codes)
    profile_indices, code_indices = load_data.get_profile_indices_and_corresponding_code_indices(metadata_dict)
    pca_model = PCA(n_components=2)
    principal_components = pca_model.fit_transform(codes)
    print(pca_model.explained_variance_ratio_)
    explained_variance = pca_model.explained_variance_ratio_
    save_dir = '/afs/desy.de/user/b/brockhul/public/pca_plots/presentation/{}'

    # model = tf.keras.models.load_model('model/model_main_less_epochs.h5')
    # data_storage_filename = '/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_downsized.npy'
    # profiles = profile_loading.get_beam_profiles_from_indices(data_storage_filename, sorted_indices=profile_indices)
    # predictions = model.predict_classes(profiles)
    # predictions = np.array(['Gaussian' if x == 1 else 'Higher Order' for x in predictions])
    # plot_scatter(principal_components, predictions, explained_variance=explained_variance, axes=(0, 1),
    #              title='PCA with predicted order labels', save=save_dir.format('circularity'))
    #
    run_labels = np.array(list(load_labels_for_plotting.load_run_numbers(metadata_dict, profile_indices)))
    plot_scatter(principal_components, run_labels, explained_variance=explained_variance, axes=(0, 1),
                 title='PCA with run numbers', save=save_dir.format('runs'))
    #
    # undulator_translation = [9, 7, 6, 6, 7, 9, 9, 7, 6]
    # undulator_labels = np.array(load_labels_for_plotting.translate_run_labels(run_labels, undulator_translation))
    # plot_scatter(principal_components, undulator_labels, explained_variance=explained_variance,  axes=(0, 1),
    #              title='PCA with undulator number',
    #              sort_colors=True, save=save_dir.format('undulators'))
    #
    # electron_bunch_charge_translations = [0.3, 0.3, 0.3, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5]
    # electron_bunch_charge_labels = np.array(
    #     load_labels_for_plotting.translate_run_labels(run_labels, electron_bunch_charge_translations))
    # plot_scatter(principal_components, electron_bunch_charge_labels, explained_variance=explained_variance,
    #              axes=(0, 1),
    #              title='PCA with electron bunch charges [nC]', save=save_dir.format('e_bunch'))
    #
    # energy_translation = [131, 100, 90, 46, 202, 238, 88, 34, 22]
    # energy_labels = np.array(load_labels_for_plotting.translate_run_labels(run_labels, energy_translation))
    # plot_scatter(principal_components, energy_labels, axes=(0, 1), explained_variance=explained_variance,
    #              sort_colors=True, title='PCA with energies [uJ]',
    #              save=save_dir.format('energy'))
    #
    # intensities = load_labels_for_plotting.load_intensities(profiles)
    # plot_scatter_continuous(principal_components, intensities, explained_variance=explained_variance,
    #                         title='PCA with profile intensities',
    #                         save=save_dir.format('intensities'))

    plot_scatter(principal_components, np.zeros(len(principal_components)), axes=(0, 1), explained_variance=explained_variance,
                 sort_colors=True, title='PCA',
                 save=save_dir.format('empty'))
