import file_tools


def get_beam_profiles_from_dict(run_input):
    with file_tools.get_run(run_number=run_input['run_number']) as current_run:
        pipeline = file_tools \
            .get_beam_profiles_pipeline(current_run=current_run, clip_to_profiles=run_input['profiles_range']) \
            .slice_horizontally(h_min=run_input['slice']['horizontal']['min'],
                                h_max=run_input['slice']['horizontal']['max']) \
            .slice_vertically(v_min=run_input['slice']['vertical']['min'], v_max=run_input['slice']['vertical']['max']) \
            .remove_background_by_intensity_fraction(cut_off_level=run_input['background_cut_off']) \
            .opening() \
            .rescale_images(horizontal_scale=run_input['horizontal_scaling_factor'])
        if run_input['shifting']['type'] == 'highest_intensity':
            return pipeline.shift_to_highest_intensity(fraction=run_input['shifting']['fraction']) \
                .change_color_resolution(new_resolution=run_input['final_color_resolution']) \
                .get_rounded_beam_profiles()
        elif run_input['shifting']['type'] == 'center_of_mass':
            return pipeline.shift_to_center_of_mass() \
                .change_color_resolution(new_resolution=run_input['final_color_resolution']) \
                .get_rounded_beam_profiles()


def get_raw_beam_profiles_from_dict(run_input):
    with file_tools.get_run(run_number=run_input['run_number']) as current_run:
        return file_tools \
            .get_beam_profiles_pipeline(current_run=current_run, clip_to_profiles=run_input['profiles_range']) \
            .slice_horizontally(h_min=run_input['slice']['horizontal']['min'],
                                h_max=run_input['slice']['horizontal']['max']) \
            .slice_vertically(v_min=run_input['slice']['vertical']['min'], v_max=run_input['slice']['vertical']['max']) \
            .get_rounded_beam_profiles()
