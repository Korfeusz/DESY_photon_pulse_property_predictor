import file_tools
from circle_finding_tools import is_circle_in_center_of_images
import time
import numpy as np
import matplotlib.pyplot as plt
from simple_circle_finding_tools import get_position_of_most_circular_images, get_circularity_index
import beam_profile_imaging

if __name__ == '__main__':
    image_number = 90
    profiles_range = False  # (2400, 2500)
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
            .remove_background_by_intensity_fraction(cut_off_level=0.6) \
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



        print('\nFinding circles: Method 1')
        t = time.time()
        labels, circularity_indices_m1 = is_circle_in_center_of_images(beam_profiles, ring_thickness=10, number_of_tests=2,
                                                                    relative_tolerance=1e-3,
                                                                    additive_tolerance=1e-3)
        print(circularity_indices_m1[:20])
        print('Method 1: elapsed:', time.time() - t)
        smallest_indices_m1 = get_position_of_most_circular_images(circularity_indices_m1, number_of_best=100)
        print('Positions', smallest_indices_m1)
        beam_profile_imaging.show_images(beam_profiles_raw[smallest_indices_m1], rows=10,
                                         title='Masking method 100 best',
                                         saveas='method_1_run_3_100_best_rt_10.png')
        # print('Values', circularity_indices[smallest_indices])


        print('\nFinding circles: Method 2')
        t = time.time()
        circularity_indices_m2 = get_circularity_index(beam_profiles, binarisation_fractions=[0.3, 0.5])
        print(circularity_indices_m2[:20])
        print('Method 2: elapsed:', time.time() - t)
        smallest_indices_m2 = get_position_of_most_circular_images(circularity_indices_m2, number_of_best=100)
        print('Positions', smallest_indices_m2)
        beam_profile_imaging.show_images(beam_profiles_raw[smallest_indices_m2], rows=10,
                                         title='Area over perimeter squared  method 100 best',
                                         saveas='method_2_run_3_100_best_3_5.png')
        # print('Values', circularity_indices[smallest_indices])
        print('Found by both: ', np.intersect1d(smallest_indices_m1, smallest_indices_m2))


        average_score = np.mean([circularity_indices_m1, circularity_indices_m2], axis=0)
        smallest_average_indices = get_position_of_most_circular_images(average_score, number_of_best=100)
        beam_profile_imaging.show_images(beam_profiles_raw[smallest_average_indices], rows=10,
                                         title='Average index 100 best',
                                         saveas='average_100_best.png')
# new shifter
# Finding circles: Method 1
# Method 1: elapsed: 19.403303623199463
# Positions [  90 7530   58 7970 5145 1327 2487 4514 7904 7649 1204 1194 7585  971
#   246 7010 6612 6790 1908 6954 6163 5646  593 6830 4146 8736 1813  606
#  6519 5716 3420 6682 5777  529 2615 5738 8400 3987 8961 4954 3714 6714
#  3086 8111 7811 2576  331 7943 3859 5400 6520 8386 5092 5365 7573 6934
#  1683   19 3458 8234 6212 2629 3794 5588  503 7327 3018 7315 7246 3144
#  4996 8529 7973  768 5134 4863 2634 3750 8116 2082 3811 7371 1100 4751
#   221 4259 8531 5545  605 5969 5006 5654 1339  540 4681 1823  907 2640
#  7761  476]

# Finding circles: Method 2
# Method 2: elapsed: 48.22590708732605
# Positions [2432 1478  932 3915  592 6725 3517   90 5257 5542 1334 1944 5296  889
#   362 4916 3718 3292 1781 6702  303 3172  324 4287 5441 2762  848 1442
#  7209 1156 7371 2364 2493 3714 6937 6771 7315 8224 3945 5005 6706   44
#  2926 4362 2343 2909 3811 5765 1381 5014 1173 5933 4572 2578  338 2814
#   290  593  990 2206 1092 4404 1360 2589 5239 8551 8849 7304 4637 5044
#  5107 1437 5086 1823 6043 7295 2423 7191 1459 3876 1764  759 5969 5732
#  7669 5110 3183  221  562 7216 4991 8126 1204 2667  443 4566 6744  998
#  5365 7241]
# Found by both:  [  90  221  593 1204 1823 3714 3811 5365 5969 7315 7371]


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