import numpy as np

def one_hot(data, num_classes):
    length = data.shape[0]
    one_hot = np.zeros((length, num_classes))
    one_hot[np.arange(length), data] = 1
    return one_hot


def next_batch(remaining_set, training_set, batch_size=64):
    x, y = remaining_set
    length = x.shape[0]
    if batch_size > length:
        return (x, y), training_set
    mask = np.zeros(length, dtype=np.bool)
    idx = np.random.choice(length, batch_size, replace=False)
    mask[idx] = True
    x_batch = x[mask]
    x_rest = x[~mask]
    y_batch = y[mask]
    y_rest = y[~mask]
    return (x_batch, y_batch), (x_rest, y_rest)