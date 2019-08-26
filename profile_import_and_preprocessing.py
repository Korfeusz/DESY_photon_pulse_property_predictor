import numpy as np
import beam_profiles_preprocessing
import json_tools
import constants

if __name__ == '__main__':
    directory = constants.preprocessed_beam_profiles_directory
    run_input_file_template = constants.run_input_file_template
    run_inputs_save_file = constants.run_inputs_save_file
    run_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    for run_number in run_numbers:
        print('Run number: {} started'.format(run_number))
        run_input = json_tools.import_json_as_dict(run_input_file_template.format(run_number))
        beam_profiles_preprocessing.store_run_input_in_json(run_inputs_file=run_inputs_save_file,
                                                            run_input=run_input, indent=2)

        beam_profiles = beam_profiles_preprocessing.get_beam_profiles_from_dict(run_input)
        beam_profiles_raw = beam_profiles_preprocessing.get_raw_beam_profiles_from_dict(run_input)
        downsized_raw_beam_profiles = beam_profiles_preprocessing.get_raw_beam_profiles_from_dict(run_input, downsize=8)

        np.save('{}/beam_profiles_run_{}{}'.format(directory, run_number, '_raw'),
                beam_profiles_raw)
        np.save('{}/beam_profiles_run_{}{}'.format(directory, run_number, ''), beam_profiles)
        np.save('{}/beam_profiles_run_{}{}'.format(directory, run_number, '_raw_downsized'),
                downsized_raw_beam_profiles)
