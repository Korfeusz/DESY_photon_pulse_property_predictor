import file_tools
import json_tools
import numpy as np

def get_beam_profiles_from_dict(run_input):
    with file_tools.get_run(run_number=run_input['run_number']) as current_run:
        pipeline = file_tools \
            .get_beam_profiles_pipeline(current_run=current_run, profiles_list=run_input['profiles_range']) \
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
            .get_beam_profiles_pipeline(current_run=current_run, profiles_list=run_input['profiles_range']) \
            .slice_horizontally(h_min=run_input['slice']['horizontal']['min'],
                                h_max=run_input['slice']['horizontal']['max']) \
            .slice_vertically(v_min=run_input['slice']['vertical']['min'], v_max=run_input['slice']['vertical']['max']) \
            .get_rounded_beam_profiles()


def get_specific_raw_beam_profiles(run_input, unsorted_index_list):
    run_input['profiles_range'] = np.array(unsorted_index_list)[np.argsort(unsorted_index_list)]
    return get_raw_beam_profiles_from_dict(run_input)


def get_beam_profiles_from_json(filename):
    run_input = json_tools.import_json_as_dict(filename)
    return get_beam_profiles_from_dict(run_input)


def get_raw_beam_profiles_from_json(filename):
    run_input = json_tools.import_json_as_dict(filename)
    return get_raw_beam_profiles_from_dict(run_input)


def store_run_input_in_json(run_inputs_file, run_input, indent):
    run_inputs_dict = json_tools.import_json_as_dict(run_inputs_file)
    run_inputs_dict.setdefault(run_input['experiment_name'], {})
    run_inputs_dict[run_input['experiment_name']] = run_input
    json_tools.dump_dict_to_json(run_inputs_file, run_inputs_dict, indent)
