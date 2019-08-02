import file_tools
from masking_method_circle_finding_tool import is_circle_in_center_of_images
import time
import numpy as np
from area_perimeter_circle_finding_tool import get_circularity_index
from tools import get_n_highest_values
import beam_profile_imaging
import beam_profiles_import_tool
import json_tools

if __name__ == '__main__':
    image_number = 90
    run_input = json_tools.import_json_as_dict('run_input.json')
    beam_profiles = beam_profiles_import_tool.get_beam_profiles_from_dict(run_input)
    beam_profiles_raw = beam_profiles_import_tool.get_raw_beam_profiles_from_dict(run_input)
    beam_profile_imaging.show_beam_profile(beam_profiles_raw, image_number)
    beam_profile_imaging.show_beam_profile(beam_profiles, image_number)

    # print('\nFinding circles: Method 1')
    # t = time.time()
    # circularity_indices_m1 = is_circle_in_center_of_images(beam_profiles, ring_thickness=20, number_of_tests=2)
    # print(circularity_indices_m1[:20])
    # print('Method 1: elapsed:', time.time() - t)
    # smallest_indices_m1 = get_n_highest_values(circularity_indices_m1, number_of_best=100)
    # print('Positions', smallest_indices_m1)
    # beam_profile_imaging.show_images(beam_profiles_raw[smallest_indices_m1], rows=10,
    #                                  title='masking_method_100_best_less_rings')
    # # print('Values', circularity_indices[smallest_indices])
    #
    # print('\nFinding circles: Method 2')
    # t = time.time()
    # circularity_indices_m2 = get_circularity_index(beam_profiles, binarisation_fractions=[0.2, 0.3, 0.5])
    # print(circularity_indices_m2[:20])
    # print('Method 2: elapsed:', time.time() - t)
    # smallest_indices_m2 = get_n_highest_values(circularity_indices_m2, number_of_best=100)
    # print('Positions', smallest_indices_m2)
    # beam_profile_imaging.show_images(beam_profiles_raw[smallest_indices_m2], rows=10,
    #                                  title='method_2_run_3_100_best_2_3_5')
    # # print('Values', circularity_indices[smallest_indices])
    # print('Found by both: ', np.intersect1d(smallest_indices_m1, smallest_indices_m2))


    # average_score = np.mean([circularity_indices_m1, circularity_indices_m2], axis=0)
    # smallest_average_indices = get_position_of_most_circular_images(average_score, number_of_best=100)
    # beam_profile_imaging.show_images(beam_profiles_raw[smallest_average_indices], rows=5,
    #                                  title='average_10_best.png')