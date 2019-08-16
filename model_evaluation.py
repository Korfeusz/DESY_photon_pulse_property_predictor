import cnn_evaluation
import cnn
import json_tools

if __name__ == '__main__':
    metadata_dict = json_tools.import_json_as_dict('metadata/metadata.json')
    all_data = cnn_evaluation.get_all_uncorrupted_beam_profiles(data_storage_filename='/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_downsized.npy',
                                                   metadata_dict=metadata_dict)

    print(all_data.shape)
    # (_, _), (x_test, y_test) = cnn.save_and_load_profiles.load_profiles()
    predictions = cnn_evaluation.get_predictions_from_model('model/model_5.h5', all_data)
    cnn_evaluation.show_random_100_images_with_labels(images=all_data, predicted_label=predictions,
                                                      correct_label=None)
