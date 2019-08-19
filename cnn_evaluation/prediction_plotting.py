import numpy as np
from cnn_evaluation import prediction_tools
import imaging_tools
from cnn_evaluation import model_loading, prediction_tools
import matplotlib.pyplot as plt


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
        title = 'FP: {FP}, FN: {FN}, TP: {TP}, TN: {TN}'.format(**prediction_tools.get_confusion_matrix(predicted, correct))
        colors = np.array(['green' if p == t else 'red' for p, t in zip(predicted, correct)])
    else:
        title = 'ones: {}, zeros: {}'.format(sum(predicted), 100 - sum(predicted))
        colors = None

    labels = np.array(['1' if p == 1 else '0' for p in predicted])

    imaging_tools.show_images(images=input_images,
                              rows=10,
                              title=title,
                              list_of_labels=labels,
                              list_of_colors=colors)


def plot_0_1_composition_of_runs(data_storage_filename, metadata_dict, model_file):
    ratio_of_0s = []
    for run_no in range(9):
        beam_profiles = model_loading.get_uncorrupted_beam_profiles_for_run(data_storage_filename,
                                                                                 metadata_dict,
                                                                                 run_no)
        predictions = prediction_tools.get_predictions_from_model(model_file, beam_profiles)
        ratio_of_0s.append(prediction_tools.get_ratio_of_1s(predictions))
    plt.show()
    plt.bar(list(range(9)), ratio_of_0s)
    plt.title('Ratio of number of detected circles to all profiles')
    plt.ylabel('Ratio')
    plt.xlabel('Experimental run number')
    plt.show()
