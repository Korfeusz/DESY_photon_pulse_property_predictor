import json_tools
import numpy as np
import cnn
import profile_loading
import constants

if __name__ == '__main__':
    metadata_dict = json_tools.import_json_as_dict(constants.metadata_file)
    model = constants.cnn_model_saveas
    data_storage_filename = '/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_downsized.npy'
    all_data = profile_loading.get_all_uncorrupted_beam_profiles(data_storage_filename=data_storage_filename,
                                                                 metadata_dict=metadata_dict)
    predictions = cnn.cnn_evaluation.get_predictions_from_model(model, all_data)
    cnn.cnn_evaluation.show_random_100_images_with_labels(images=all_data, predicted_label=predictions,
                                                          correct_label=None)
    cnn.cnn_evaluation.plot_0_1_composition_of_runs(data_storage_filename=data_storage_filename,
                                                    metadata_dict=metadata_dict,
                                                    model_file=model)

    profiles_labeled_1 = cnn.cnn_evaluation.mean_profile_tools.get_profiles_labeled_1(predictions, all_data)
    mean_profile_1 = cnn.cnn_evaluation.mean_profile_tools.create_mean_profile(data=profiles_labeled_1)
    fit_1 = cnn.cnn_evaluation.mean_profile_tools.fit_gaussian_to_profile(mean_profile_1)

    profiles_labeled_0 = cnn.cnn_evaluation.mean_profile_tools.get_profiles_labeled_0(predictions, all_data)
    mean_profile_0 = cnn.cnn_evaluation.mean_profile_tools.create_mean_profile(data=profiles_labeled_0)
    fit_0 = cnn.cnn_evaluation.mean_profile_tools.fit_gaussian_to_profile(mean_profile_0)

    print(fit_1)
    print(fit_0)
    print('median intensity of profiles labeled 1: {}'.format(np.median(profiles_labeled_1)))

    print('median intensity of profiles labeled 0: {}'.format(np.median(profiles_labeled_0)))

    print(sum(sum(sum(profiles_labeled_1))))
    print(sum(sum(sum(profiles_labeled_0))))

    print(np.shape(profiles_labeled_1))
    print(np.shape(profiles_labeled_0))


    data_save_directory= constants.cnn_train_test_split_data_directory
    label_name = 'combination_label'
    path_to_profiles = constants.preprocessed_beam_profiles_directory + '/beam_profiles_run_{}_raw_downsized.npy'
    (x_train, y_train), (x_test, y_test) = cnn.save_and_load_profiles.load_train_test_split_data(data_save_directory,
                                                                                                 metadata_dict,
                                                                                                 label_name,
                                                                                                 path_to_profiles)
    train_pred = cnn.cnn_evaluation.get_predictions_from_model(model, x_train)
    test_pred = cnn.cnn_evaluation.get_predictions_from_model(model, x_test)
    print(cnn.cnn_evaluation.get_confusion_matrix(train_pred, y_train))
    print(cnn.cnn_evaluation.get_confusion_matrix(test_pred, y_test))

