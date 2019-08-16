import numpy as np
from cnn_evaluation import prediction_tools
import imaging_tools


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
