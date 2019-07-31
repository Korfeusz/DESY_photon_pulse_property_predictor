import file_tools
from circle_finding_tools import is_circle_in_center_of_images
import time
import numpy as np
import matplotlib.pyplot as plt
from simple_circle_finding_tools import get_position_of_most_circular_images, get_circularity_index
import beam_profile_imaging

if __name__ == '__main__':
    image_number = 90
    profiles_range = (0, 100)
    h_min, h_max, v_min, v_max = 105, 364, 90, 349
    # h_min, h_max, v_min, v_max = 0, 483, 0, 360
    final_color_resolution = 63
    # .remove_background(number_of_lowest_colors=5, masking_color_resolution=15) \
    with file_tools.get_run(run_number=3) as current_run:
        t = time.time()
        beam_profiles = file_tools \
            .get_beam_profiles_pipeline(current_run=current_run, clip_to_profiles=profiles_range) \
            .slice_horizontally(h_min=h_min, h_max=h_max) \
            .slice_vertically(v_min=v_min, v_max=v_max) \
            .remove_background(number_of_lowest_colors=5, masking_color_resolution=15) \
            .opening() \
            .rescale_images(horizontal_scale=1.2) \
            .shift_to_highest_intensity(fraction=0.8) \
            .change_color_resolution(new_resolution=final_color_resolution) \
            .get_rounded_beam_profiles()
        print(time.time() - t)


        beam_profiles_raw = file_tools \
            .get_beam_profiles_pipeline(current_run=current_run, clip_to_profiles=profiles_range) \
            .slice_horizontally(h_min=h_min, h_max=h_max) \
            .slice_vertically(v_min=v_min, v_max=v_max) \
            .change_color_resolution(new_resolution=4095) \
            .get_rounded_beam_profiles()

        plt.imshow(beam_profiles_raw[image_number, :, :], cmap=plt.cm.jet)
        plt.show()
        plt.imshow(beam_profiles[image_number, :, :], cmap=plt.cm.jet)
        plt.show()



        # print('\nFinding circles: Method 1')
        # t = time.time()
        # labels, circularity_indices = is_circle_in_center_of_images(beam_profiles, ring_thickness=10, number_of_tests=2,
        #                                                             relative_tolerance=1e-3,
        #                                                             additive_tolerance=1e-3)
        # print('Method 1: elapsed:', time.time() - t)
        # smallest_indices_m1 = get_position_of_most_circular_images(circularity_indices, number_of_best=100)
        # print('Positions', smallest_indices_m1)
        # beam_profile_imaging.show_images(beam_profiles_raw[smallest_indices_m1], rows=10,
        #                                  title='Masking method 100 best',
        #                                  saveas='method_1_run_3_100_best.png')
        # # print('Values', circularity_indices[smallest_indices])
        #
        #
        # print('\nFinding circles: Method 2')
        # t = time.time()
        # circularity_indices = get_circularity_index(beam_profiles, binarisation_fractions=[0.3, 0.5])
        # print('Method 2: elapsed:', time.time() - t)
        # smallest_indices_m2 = get_position_of_most_circular_images(circularity_indices, number_of_best=100)
        # print('Positions', smallest_indices_m2)
        # beam_profile_imaging.show_images(beam_profiles_raw[smallest_indices_m2], rows=10,
        #                                  title='Area over perimeter squared  method 100 best',
        #                                  saveas='method_2_run_3_100_best.png')
        # # print('Values', circularity_indices[smallest_indices])
        # print('Found by both: ', np.intersect1d(smallest_indices_m1, smallest_indices_m2))



# TEST
# labels = is_circle_in_center_of_images(beam_profiles, ring_thickness=10, number_of_tests=2,
#                                                relative_tolerance=1e-2,
#                                                additive_tolerance=1e-3)


# Circularity indeces - best 100, run 3
# [0.00022564 0.00023002 0.00036762 0.00036762 0.00039633 0.00039633
#  0.00041438 0.00042021 0.00044913 0.00077508 0.00079694 0.00086892
#  0.0008918  0.00095063 0.00095524 0.00098886 0.00101005 0.00106759
#  0.0010689  0.00107799 0.00108438 0.00109768 0.00111204 0.0011203
#  0.0011213  0.0011252  0.0011378  0.0011759  0.00119299 0.00122005
#  0.00123648 0.00124581 0.00129703 0.00131868 0.00131917 0.00132468
#  0.00135391 0.001372   0.00138895 0.00141555 0.00145925 0.00147454
#  0.00148333 0.00151073 0.0015727  0.00158386 0.00158879 0.00159434
#  0.00161435 0.00161559 0.00163312 0.00165183 0.00167128 0.00167716
#  0.00169337 0.00169819 0.00171613 0.00173444 0.00178318 0.00179788
#  0.00179872 0.00179902 0.00181194 0.00182727 0.0018359  0.00185273
#  0.00189903 0.0019025  0.00193575 0.00195062 0.00202482 0.00204771
#  0.00206036 0.00206077 0.00206245 0.00206695 0.00208379 0.00209731
#  0.00210311 0.00211379 0.00211471 0.00213521 0.00214801 0.00215148
#  0.00215712 0.00216532 0.00216671 0.0022335  0.00224184 0.00226077
#  0.00226244 0.0022651  0.00227042 0.00227187 0.00228172 0.00231792
#  0.00232518 0.00233487 0.0023408  0.00235118]
# [  90 5777 7970   58 1908  768 1194 3708 4224 5537 7331 3784 8226 2698
#  6520 7649 1204 7585  971 4146  593 1544  525  246 4514 5706 1533  560
#  7010 8465 5646 3987 8895 5092  353 6954 3571 5006 7050 8386 5346 6611
#   799 6247 1211 5725 1381 4086 5400  398 1110 8075 8703 6567 5147 9090
#  4850 8736 4482 6519 5358 6790 2552 7943 2615 2976 8383 5838 7582 8332
#  8961  992  271 3714 7405 5044 7522 5773 7731 1561 5024 4852   15 5837
#  8400 7904  529  267 3087 3741 5753 6425  698 5365 8873 5788 4996 6189
#  6155 1376]