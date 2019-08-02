import numpy as np


def get_specific_circle_indices_list(beam_profiles_metadata_dict, run_name,
                                     index_type,
                                     settings):
    beam_profiles_found = []
    circle_indices = []
    if index_type == 'area_perimeter':
        index_string = get_circle_index_string(run_name, index_type, binarisation_fraction=settings)
    elif index_type == 'masking':
        index_string = get_circle_index_string(run_name, index_type, **settings)

    for profile_index, profile_metadata in beam_profiles_metadata_dict.items():
        if index_string in profile_metadata['circularity_index'].keys():
            beam_profiles_found.append(profile_index)
            circle_indices.append(profile_metadata['circularity_index'][index_string]['value'])
    return beam_profiles_found, circle_indices


def get_circle_index_string(run_name, index_type, binarisation_fraction=None, ring_thickness=None, number_of_tests=None):
    if index_type == 'area_perimeter':
        settings_string = '_'.join([str(x - int(x)).split('.')[1] for x in binarisation_fraction])
    elif index_type == 'masking':
        settings_string = '_'.join([str(ring_thickness), str(number_of_tests)])
    return 'run_name_{}_{}_settings_{}'.format(run_name, index_type, settings_string)
