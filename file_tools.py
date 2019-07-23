from os import listdir
from os.path import isfile, join
import path_constants


def get_paths_to_files_in_directory(directory):
    return [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]


def get_run_path(run_number=0):
    directory = path_constants.experiment_data_directory
    return join(directory, get_paths_to_files_in_directory(directory)[run_number])


def get_beam_profiles(run):
    return run[path_constants.beam_profiles_path]
