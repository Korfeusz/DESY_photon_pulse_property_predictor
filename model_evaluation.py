import cnn_evaluation
import cnn
import json_tools
import numpy as np
if __name__ == '__main__':
    metadata_dict = json_tools.import_json_as_dict('metadata/metadata_1.json')
    model = 'model/model_2_biased.h5'
    data_storage_filename='/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_downsized.npy'
    all_data = cnn_evaluation.get_all_uncorrupted_beam_profiles(data_storage_filename=data_storage_filename,
                                                   metadata_dict=metadata_dict)

    print(all_data.shape)
    # (_, _), (x_test, y_test) = cnn.save_and_load_profiles.load_profiles()
    predictions = cnn_evaluation.get_predictions_from_model(model, all_data)
    # cnn_evaluation.show_random_100_images_with_labels(images=all_data, predicted_label=predictions,
    #                                                   correct_label=None)
    # cnn_evaluation.plot_0_1_composition_of_runs(data_storage_filename=data_storage_filename,
    #                                             metadata_dict=metadata_dict,
    #                                             model_file=model)

    profiles_labeled_1 = cnn_evaluation.mean_profile_tools.get_profiles_labeled_1(predictions, all_data)
    mean_profile_1 = cnn_evaluation.mean_profile_tools.create_mean_profile(data=profiles_labeled_1)
    fit_1 = cnn_evaluation.mean_profile_tools.fit_gaussian_to_profile(mean_profile_1)

    profiles_labeled_0 = cnn_evaluation.mean_profile_tools.get_profiles_labeled_0(predictions, all_data)
    mean_profile_0 = cnn_evaluation.mean_profile_tools.create_mean_profile(data=profiles_labeled_0)
    fit_0 = cnn_evaluation.mean_profile_tools.fit_gaussian_to_profile(mean_profile_0)



    print(fit_1)
    print(fit_0)
    print('median intensity of profiles labeled 1: {}'.format(np.median(profiles_labeled_1)))

    print('median intensity of profiles labeled 0: {}'.format(np.median(profiles_labeled_0)))

