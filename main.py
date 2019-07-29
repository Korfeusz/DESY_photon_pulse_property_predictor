import file_tools
import beam_profile_imaging
from circle_finding_tools import is_circle_in_center_of_images
import time
import numpy as np


if __name__ == '__main__':
    image_number = 74
    profiles_range = (0, 100)
    h_min, h_max, v_min, v_max = 105, 364, 90, 349
    # h_min, h_max, v_min, v_max = 0, 483, 0, 360
    final_color_resolution = 63

    with file_tools.get_run(run_number=1) as current_run:
        beam_profiles = file_tools\
            .get_beam_profiles_pipeline(current_run=current_run, clip_to_profiles=profiles_range) \
            .slice_horizontally(h_min=h_min, h_max=h_max)\
            .slice_vertically(v_min=v_min, v_max=v_max)\
            .remove_background(number_of_lowest_colors=5, masking_color_resolution=15)\
            .opening() \
            .rescale_images(horizontal_scale=1.2) \
            .shift_to_center_of_mass()\
            .change_color_resolution(new_resolution=final_color_resolution)\
            .get_rounded_beam_profiles()

        beam_profiles_raw = file_tools\
            .get_beam_profiles_pipeline(current_run=current_run, clip_to_profiles=profiles_range)\
            .slice_horizontally(h_min=h_min, h_max=h_max)\
            .slice_vertically(v_min=v_min, v_max=v_max)\
            .change_color_resolution(new_resolution=4095)\
            .get_rounded_beam_profiles()

        beam_profile_imaging.save_beam_profile_image(beam_profiles[image_number, :, :], name='final_profile.png')
        beam_profile_imaging.save_beam_profile_image(beam_profiles_raw[image_number, :, :], name='input_profile.png')
        print(beam_profiles.shape)

        t = time.time()
        labels = is_circle_in_center_of_images(beam_profiles, ring_thickness=30, number_of_tests=2,
                                               relative_tolerance=1e-1,
                                               additive_tolerance=1e-2)
        print(np.where(labels))
        print(len(np.where(labels)[0]))
        print(labels.shape)
    print('elapsed:', time.time() - t)


# (array([ 365,  615,  737,  805,  826,  932,  951, 1003, 1192, 1513, 1684,
#        2058, 2193, 2317, 2723, 3173, 3190, 3412, 4340, 4818, 4912, 5240]