import tensorflow as tf
import cnn
import imaging_tools
import numpy as np
import json_tools

def get_confusion_matrix(predicted, correct):
    false_positive = sum([1 for p, c in zip(predicted, correct) if p != c and p == 1])
    true_positive = sum([1 for p, c in zip(predicted, correct) if p == c and p == 1])
    true_negative = sum([1 for p, c in zip(predicted, correct) if p == c and p == 0])
    false_negative = sum([1 for p, c in zip(predicted, correct) if p != c and p == 0])
    return {
        'FP': false_positive,
        'TP': true_positive,
        'TN': true_negative,
        'FN': false_negative
    }


def get_random_sample_of_images_predictions_and_labels(images, predicted, correct=None, length=100):
    random_indices = np.random.choice(range(len(predicted)), size=length)
    if correct is not None:
        return images[random_indices, :, :], predicted[random_indices], correct[random_indices]
    else:
        return images[random_indices, :, :], predicted[random_indices], None


def show_random_100_images_with_labels(images, predicted_label, correct_label=None):
    input_images, predicted, correct = get_random_sample_of_images_predictions_and_labels(images,
                                                                                          predicted_label,
                                                                                          correct_label,
                                                                                          length=100)
    if correct is not None:
        title = 'FP: {FP}, FN: {FN}, TP: {TP}, TN: {TN}'.format(**get_confusion_matrix(predicted, correct))
        colors = np.array(['green' if p == t else 'red' for p, t in zip(predicted, correct)])
    else:
        title = 'Predicted_labels'
        colors = None

    labels = np.array(['1' if p == 1 else '0' for p in predicted])

    imaging_tools.show_images(images=input_images,
                              rows=10,
                              title=title,
                              list_of_labels=labels,
                              list_of_colors=colors)


def get_predictions_from_model(filename, profiles):
    model = tf.keras.models.load_model(filename)
    return model.predict_classes(profiles)


def get_all_beam_profiles_from_filename(filename, metadata_dict):


    return data


if __name__ == '__main__':
    metadata_dict = json_tools.import_json_as_dict('../metadata/metadata.json')
    all_data = get_all_beam_profiles_from_filename(filename='/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_downsized.npy',
                                                   metadata_dict=metadata_dict)

    print(all_data.shape)
    # (_, _), (x_test, y_test) = cnn.save_and_load_profiles.load_profiles()
    predictions = get_predictions_from_model('../model/model_1.h5', all_data)
    show_random_100_images_with_labels(images=all_data, predicted_label=predictions,
                                       correct_label=None)
