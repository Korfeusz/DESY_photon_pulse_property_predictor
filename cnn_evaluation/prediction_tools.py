import tensorflow as tf


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


def get_predictions_from_model(filename, profiles):
    model = tf.keras.models.load_model(filename)
    return model.predict_classes(profiles)
