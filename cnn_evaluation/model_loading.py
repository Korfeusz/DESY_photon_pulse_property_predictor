import numpy as np


def get_all_beam_profiles_from_filename(filename, metadata_dict):
    data = np.load(filename.format(0))
    for i in range(1, 9):
        data = np.vstack((data, np.load(filename.format(i))))
    return data
