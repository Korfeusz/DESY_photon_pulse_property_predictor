import numpy as np
from tools import get_indices_of_n_lowest_values
import beam_profile_imaging
import beam_profiles_import_tool
import json_tools
import beam_profile_metadata_tools
import labeling_algo

if __name__ == '__main__':
    # image_number = 2
    for i in range(9):
        print('Run number: {} started'.format(i))
        run_input = json_tools.import_json_as_dict('run_inputs/run_input_{}.json'.format(i))
        beam_profiles_import_tool.store_run_input_in_json(run_inputs_file='run_inputs.json', run_input=run_input, indent=2)
        beam_profiles = beam_profiles_import_tool.get_beam_profiles_from_dict(run_input)
        beam_profiles_raw = beam_profiles_import_tool.get_raw_beam_profiles_from_dict(run_input)
        # beam_profile_imaging.show_beam_profile(beam_profiles_raw, image_number)
        # beam_profile_imaging.show_beam_profile(beam_profiles, image_number)

        metadata_file = 'metadata_total.json'
        beam_profile_metadata_tools.get_metadata_writer(beam_profiles, run_input, metadata_file) \
            .add_beam_profiles_addresses() \
            .add_area_perimeter_squared_circularity_indices(binarisation_fractions=[0.3, 0.5]) \
            .add_masking_method_circularity_indices(ring_thickness=10, number_of_tests=2) \
            .add_masking_method_circularity_indices(ring_thickness=20, number_of_tests=2) \
            .add_area_perimeter_squared_circularity_indices(binarisation_fractions=[0.3, 0.5, 0.7]) \
            .dump_metadata_to_json(filename=metadata_file, indent=2)



    # metadata_dict = json_tools.import_json_as_dict(metadata_file)

    # print('\nFinding circles: Method 1')
    # profiles, circularity_indices_m1 = labeling_algo.get_specific_circle_indices_list(metadata_dict, experiment_name='0',
    #                                                                                   index_type='masking',
    #                                                                                   settings={'ring_thickness': 10,
    #                                                                                             'number_of_tests': 2})
    # best_profile_indices = get_n_highest_values(np.array(circularity_indices_m1), number_of_best=10)
    # print('Positions', best_profile_indices)
    # beam_profile_imaging.show_images(beam_profiles_raw[best_profile_indices], rows=5,
    #                                  title='masking_method_10_best_less_rings')
    #
    # print('\nFinding circles: Method 2')
    # profiles, circularity_indices_m2 = labeling_algo.get_specific_circle_indices_list(metadata_dict, experiment_name='0',
    #                                                                                   index_type='area_perimeter',
    #                                                                                   settings=[0.3, 0.5])
    # best_profile_indices = get_n_highest_values(np.array(circularity_indices_m2), number_of_best=10)
    # print('Positions', best_profile_indices)
    # beam_profile_imaging.show_images(beam_profiles_raw[best_profile_indices], rows=20,
    #                                  title='masking_method_10_best_less_rings')



    #
    # average_score = np.mean([circularity_indices_m1, circularity_indices_m2], axis=0)
    # smallest_average_indices = get_position_of_most_circular_images(average_score, number_of_best=100)
    # beam_profile_imaging.show_images(beam_profiles_raw[smallest_average_indices], rows=5,
    #                                  title='average_10_best.png')
