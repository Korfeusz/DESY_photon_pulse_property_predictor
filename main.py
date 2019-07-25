import file_tools
import beam_profile_imaging

if __name__ == '__main__':
    image_number = 3
    run_number = 3

    current_run = file_tools.get_run(run_number=run_number)
    beam_profiles = file_tools\
        .get_beam_profiles_pipeline(current_run=current_run, clip_to_ten_profiles=True) \
        .slice_horizontally(h_min=0, h_max=483)\
        .slice_vertically(v_min=0, v_max=648)\
        .change_color_resolution(new_resolution=63)\
        .get_rounded_beam_profiles()

    beam_profile_imaging.save_beam_profile_image(beam_profiles[image_number, :, :], name='save_test.png')
    print(beam_profiles.shape)

    current_run.close()
# z = A * np.exp(-(((xv - ux)**2)/(2 * sx**2) + ((yv - uy)**2)/(2 * sy**2)))
# np.corrcoef(z)