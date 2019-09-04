from os import listdir
from os.path import isfile, join

import constants
import numpy as np
import h5py
from beam_profiles_preprocessing.beam_profiles_pipeline import BeamProfilesPipeline
from contextlib import contextmanager


def get_paths_to_files_in_directory(directory):
    return [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]


def get_run_path(run_number=0):
    directory = constants.experiment_data_directory
    return join(directory, get_paths_to_files_in_directory(directory)[run_number])


@contextmanager
def get_run(run_number=0):
    current_run = h5py.File(get_run_path(run_number=run_number))
    yield current_run
    current_run.close()


def get_beam_profiles_pipeline(current_run, profiles_list=False):
    if constants.MOCK:
        data = np.round(np.random.rand(100, 200, 230) * constants.BEAM_PROFILE_COLOR_RESOLUTION)
    else:
        data = current_run[constants.beam_profiles_path]
        if np.any(profiles_list):
            data = data[profiles_list, :, :]
    return BeamProfilesPipeline(data=data)
