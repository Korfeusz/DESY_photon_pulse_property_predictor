import file_tools
import beam_profile_imaging
import time

if __name__ == '__main__':
    image_number = 0
    t = time.time()
    with file_tools.get_run(run_number=3) as current_run:
        beam_profiles = file_tools\
            .get_beam_profiles_pipeline(current_run=current_run, clip_to_ten_profiles=False) \
            .slice_horizontally(h_min=115, h_max=335)\
            .slice_vertically(v_min=100, v_max=320)\
            .remove_background(number_of_lowest_colors=4, masking_color_resolution=15)\
            .opening()\
            .change_color_resolution(new_resolution=63)\
            .get_rounded_beam_profiles()

        beam_profile_imaging.save_beam_profile_image(beam_profiles[image_number, :, :], name='save_test.png')
        print(beam_profiles.shape)
    print('elapsed:', time.time() - t)
# z = A * np.exp(-(((xv - ux)**2)/(2 * sx**2) + ((yv - uy)**2)/(2 * sy**2)))
# np.corrcoef(z)

