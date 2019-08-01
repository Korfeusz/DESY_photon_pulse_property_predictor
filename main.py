import file_tools
from masking_method_circle_finding_tool import is_circle_in_center_of_images
import time
import numpy as np
from area_perimeter_circle_finding_tool import get_circularity_index
from tools import get_n_highest_values
import beam_profile_imaging

if __name__ == '__main__':
    image_number = 90
    profiles_range = (2400, 2500)
    h_min, h_max, v_min, v_max = 105, 364, 90, 349
    final_color_resolution = 63
    with file_tools.get_run(run_number=3) as current_run:
        beam_profiles = file_tools \
            .get_beam_profiles_pipeline(current_run=current_run, clip_to_profiles=profiles_range) \
            .slice_horizontally(h_min=h_min, h_max=h_max) \
            .slice_vertically(v_min=v_min, v_max=v_max) \
            .remove_background_by_intensity_fraction(cut_off_level=0.6) \
            .opening() \
            .rescale_images(horizontal_scale=1.2) \
            .shift_to_highest_intensity(fraction=0.8) \
            .change_color_resolution(new_resolution=final_color_resolution) \
            .get_rounded_beam_profiles()

        beam_profiles_raw = file_tools \
            .get_beam_profiles_pipeline(current_run=current_run, clip_to_profiles=profiles_range) \
            .slice_horizontally(h_min=h_min, h_max=h_max) \
            .slice_vertically(v_min=v_min, v_max=v_max) \
            .change_color_resolution(new_resolution=4095) \
            .get_rounded_beam_profiles()

        beam_profile_imaging.show_beam_profile(beam_profiles_raw, image_number)
        beam_profile_imaging.show_beam_profile(beam_profiles, image_number)

    print('\nFinding circles: Method 1')
    t = time.time()
    circularity_indices_m1 = is_circle_in_center_of_images(beam_profiles, ring_thickness=10, number_of_tests=2)
    print(circularity_indices_m1[:20])
    print('Method 1: elapsed:', time.time() - t)
    smallest_indices_m1 = get_n_highest_values(circularity_indices_m1, number_of_best=10)
    print('Positions', smallest_indices_m1)
    beam_profile_imaging.show_images(beam_profiles_raw[smallest_indices_m1], rows=5,
                                     title='masking_method_10_best')
    # print('Values', circularity_indices[smallest_indices])

    print('\nFinding circles: Method 2')
    t = time.time()
    circularity_indices_m2 = get_circularity_index(beam_profiles, binarisation_fractions=[0.3, 0.5])
    print(circularity_indices_m2[:20])
    print('Method 2: elapsed:', time.time() - t)
    smallest_indices_m2 = get_n_highest_values(circularity_indices_m2, number_of_best=10)
    print('Positions', smallest_indices_m2)
    beam_profile_imaging.show_images(beam_profiles_raw[smallest_indices_m2], rows=5,
                                     title='method_2_run_3_10_best_3_5')
    # print('Values', circularity_indices[smallest_indices])
    print('Found by both: ', np.intersect1d(smallest_indices_m1, smallest_indices_m2))


    # average_score = np.mean([circularity_indices_m1, circularity_indices_m2], axis=0)
    # smallest_average_indices = get_position_of_most_circular_images(average_score, number_of_best=100)
    # beam_profile_imaging.show_images(beam_profiles_raw[smallest_average_indices], rows=5,
    #                                  title='average_10_best.png')