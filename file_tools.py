from os import listdir
from os.path import isfile, join
import path_constants
import numpy as np
import h5py
from beam_profiles_pipeline import BeamProfilesPipeline
import constants
from contextlib import contextmanager


def get_paths_to_files_in_directory(directory):
    return [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]


def get_run_path(run_number=0):
    directory = path_constants.experiment_data_directory
    return join(directory, get_paths_to_files_in_directory(directory)[run_number])


@contextmanager
def get_run(run_number):
    current_run = h5py.File(get_run_path(run_number=run_number))
    yield current_run
    current_run.close()


def get_beam_profiles_pipeline(current_run, clip_to_ten_profiles=False):
    if path_constants.MOCK:
        data = np.round(np.random.rand(100, 200, 230) * constants.BEAM_PROFILE_COLOR_RESOLUTION)
    else:
        data = current_run[path_constants.beam_profiles_path]
        if clip_to_ten_profiles:
            data = data[0:10, :, :]
    return BeamProfilesPipeline(data=data)
