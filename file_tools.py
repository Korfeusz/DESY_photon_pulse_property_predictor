from os import listdir
from os.path import isfile, join
import path_constants
import numpy as np
import h5py
from beam_profiles_pipeline import BeamProfilesPipeline
import constants


def get_paths_to_files_in_directory(directory):
    return [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]


def get_run_path(run_number=0):
    directory = path_constants.experiment_data_directory
    return join(directory, get_paths_to_files_in_directory(directory)[run_number])


def get_beam_profiles_pipeline(run_number=0):
    if path_constants.MOCK:
        data = np.round(np.random.rand(100, 200, 230) * constants.BEAM_PROFILE_COLOR_RESOLUTION)
    else:
        with h5py.File(get_run_path(run_number=run_number), 'r') as current_run:
            data = current_run[path_constants.beam_profiles_path]
    return BeamProfilesPipeline(data=data)


def get_beam_profile_creator(run_number=0, profile_number=0):
    beam_profiles = get_beam_profiles_pipeline(run_number=run_number)
    return BeamProfilesPipeline(data=beam_profiles[profile_number])
