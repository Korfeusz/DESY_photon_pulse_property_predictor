import numpy as np
import beam_profiles_preprocessing
import json_tools

import imaging_tools

if __name__ == '__main__':
    run_numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    for run_number in run_numbers:
        print('Run number: {} started'.format(run_number))
        run_input = json_tools.import_json_as_dict('run_inputs/run_input_{}.json'.format(run_number))
        beam_profiles_preprocessing.store_run_input_in_json(run_inputs_file='metadata/run_inputs.json',
                                                            run_input=run_input, indent=2)
        # beam_profiles = beam_profiles_preprocessing.get_beam_profiles_from_dict(run_input)
        # beam_profiles_raw = beam_profiles_preprocessing.get_raw_beam_profiles_from_dict(run_input)
        downsized_raw_beam_profiles = beam_profiles_preprocessing.get_raw_beam_profiles_from_dict(run_input, downsize=8)

        # np.save('{}/{}/beam_profiles_run_{}_raw'.format('/beegfs/desy/user/brockhul', 'preprocessed_data', run_number), beam_profiles_raw)
        # np.save('{}/{}/beam_profiles_run_{}'.format('/beegfs/desy/user/brockhul', 'preprocessed_data', run_number), beam_profiles)
        np.save('{}/{}/beam_profiles_run_{}_raw_downsized'.format('/beegfs/desy/user/brockhul', 'preprocessed_data',
                                                                  run_number), downsized_raw_beam_profiles)

        imaging_tools.show_beam_profile(downsized_raw_beam_profiles, 1000)
        print(downsized_raw_beam_profiles.shape)
