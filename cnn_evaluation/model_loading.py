import numpy as np


def get_uncorrupted_indices_for_a_specific_run(metadata_dict, run_no):
    return [index for index in metadata_dict.keys() if
            index.startswith(str(run_no)) and metadata_dict[index]['corrupted'] is False]


def sort_indices_by_run_number_and_profile_number(indices):
    return sorted(indices, key=lambda s: ([int(x) for x in s.split('_')]))


def convert_index_to_address(index):
    return [int(x) for x in index.split('_')]


def get_beam_profiles_from_indices(data_storage_filename, sorted_indices):
    previous_run_no = convert_index_to_address(sorted_indices[0])[0]
    data = np.load(data_storage_filename.format(previous_run_no))
    beam_profiles = np.zeros(shape=(len(sorted_indices), data.shape[1], data.shape[2]))
    for i, index in enumerate(sorted_indices):
        current_run_no, profile_number = convert_index_to_address(index)
        if not previous_run_no == current_run_no:
            data = np.load(data_storage_filename.format(current_run_no))
        beam_profiles[i, :, :] = data[profile_number, :, :]
        previous_run_no = current_run_no
    return beam_profiles


def get_all_uncorrupted_indices(metadata_dict):
    indices = []
    for i in range(9):
        indices.extend(get_uncorrupted_indices_for_a_specific_run(metadata_dict, i))
    return indices


def get_all_uncorrupted_beam_profiles(data_storage_filename, metadata_dict):
    indices = get_all_uncorrupted_indices(metadata_dict)
    sorted_indices = sort_indices_by_run_number_and_profile_number(indices)
    return get_beam_profiles_from_indices(data_storage_filename, sorted_indices)
