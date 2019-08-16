import cnn_evaluation
import cnn

if __name__ == '__main__':
    # metadata_dict = json_tools.import_json_as_dict('../metadata/metadata.json')
    # all_data = get_all_beam_profiles_from_filename(filename='/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_downsized.npy',
    #                                                metadata_dict=metadata_dict)
    #
    # print(all_data.shape)
    (_, _), (x_test, y_test) = cnn.save_and_load_profiles.load_profiles()
    predictions = cnn_evaluation.get_predictions_from_model('../model/model_5.h5', x_test)
    cnn_evaluation.show_random_100_images_with_labels(images=x_test, predicted_label=predictions,
                                                      correct_label=y_test)
