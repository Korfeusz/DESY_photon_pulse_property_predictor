import file_tools
import beam_profile_imaging

if __name__ == '__main__':
    image_number = 20
    run_number = 3
    desired_color_bits = 63
    horizontal_min, horizontal_max = 0, 230
    vertical_min, vertical_max = 0, 200

    beam_profile = file_tools.get_beam_profiles_pipeline(run_number=run_number)\
        .slice_horizontally(h_min=horizontal_min, h_max=horizontal_max)\
        .slice_vertically(v_min=vertical_min, v_max=vertical_max)\
        .change_color_resolution(desired_color_bits)\
        .get_rounded_beam_profiles()

    beam_profile_imaging.save_beam_profile_image(beam_profile[10, :, :], name='save_test.png')
    print(beam_profile.shape)
