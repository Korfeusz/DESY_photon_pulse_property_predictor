import file_tools
import beam_profile_imaging
import time

if __name__ == '__main__':
    image_number = 0
    h_min, h_max, v_min, v_max = 115, 334, 100, 319
    final_color_resolution = 127
    t = time.time()

    with file_tools.get_run(run_number=5) as current_run:
        beam_profiles = file_tools\
            .get_beam_profiles_pipeline(current_run=current_run, clip_to_ten_profiles=True) \
            .slice_horizontally(h_min=h_min, h_max=h_max)\
            .slice_vertically(v_min=v_min, v_max=v_max)\
            .remove_background(number_of_lowest_colors=4, masking_color_resolution=15)\
            .opening()\
            .shift_to_center_of_mass()\
            .change_color_resolution(new_resolution=final_color_resolution)\
            .get_rounded_beam_profiles()

        beam_profiles_raw = file_tools\
            .get_beam_profiles_pipeline(current_run=current_run, clip_to_ten_profiles=True)\
            .slice_horizontally(h_min=h_min, h_max=h_max)\
            .slice_vertically(v_min=v_min, v_max=v_max)\
            .change_color_resolution(new_resolution=4095)\
            .get_rounded_beam_profiles()

        beam_profile_imaging.save_beam_profile_image(beam_profiles[image_number, :, :], name='final_profile.png')
        beam_profile_imaging.save_beam_profile_image(beam_profiles_raw[image_number, :, :], name='input_profile.png')
        print(beam_profiles.shape)
    print('elapsed:', time.time() - t)


