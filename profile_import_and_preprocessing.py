import numpy as np
import beam_profiles_preprocessing
import json_tools


if __name__ == '__main__':
    run_numbers = [0, 1, 2, 3]
    for run_number in run_numbers:
        print('Run number: {} started'.format(run_number))
        run_input = json_tools.import_json_as_dict('run_inputs/run_input_{}.json'.format(run_number))
        beam_profiles_preprocessing.store_run_input_in_json(run_inputs_file='metadata/run_inputs.json',
                                                            run_input=run_input, indent=2)
        beam_profiles = beam_profiles_preprocessing.get_beam_profiles_from_dict(run_input)
        beam_profiles_raw = beam_profiles_preprocessing.get_raw_beam_profiles_from_dict(run_input)
        np.save('preprocessed_data/beam_profiles_run_{}_raw_small'.format(run_number), beam_profiles_raw)
        np.save('preprocessed_data/beam_profiles_run_{}_small'.format(run_number), beam_profiles)
