import file_tools
import beam_profile_imaging

if __name__ == '__main__':
    image_number = 20
    run_number = 3
    desired_color_bits = 63
    horizontal_min, horizontal_max = 0, 230
    vertical_min, vertical_max = 0, 200

    beam_profile = file_tools.get_beam_profile_creator(run_number=run_number, profile_number=image_number)\
        .slice_horizontally(h_min=horizontal_min, h_max=horizontal_max)\
        .slice_vertically(v_min=vertical_min, v_max=vertical_max)\
        .change_color_resolution(desired_color_bits)\
        .get_rounded_beam_profile()

    beam_profile_imaging.save_beam_profile_image(beam_profile, name='save_test.png')
    print(beam_profile.max())