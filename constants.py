BEAM_PROFILE_COLOR_RESOLUTION = 4095
NUMBER_OF_RUNS = 9
MOCK = False
experiment_data_directory = '/asap3/flash/gpfs/fl21/2019/data/11007852/raw/hdf/by-run/'
beam_profiles_path = 'uncategorised/FLASH2_USER1/FLASH.FEL/FL2.CAM01/FL2_CE_YAG_DET4/dset'

preprocessed_beam_profiles_directory = '/beegfs/desy/user/brockhul/preprocessed_data_2'
run_input_file_template = 'run_inputs/run_input_{}.json'
run_inputs_save_file = 'metadata/run_inputs.json'
metadata_file = 'metadata/metadata.json'
experiment_name = '0'

cnn_train_test_split_data_directory = '/beegfs/desy/user/brockhul/cnn_train_test_split_data/'
cnn_model_saveas = 'model/model_less_in_dense.h5'
cnn_log_dir = 'logs/fit/'

autoencoder_model_name = 'autoencoder_tst'
autoencoder_codes_save = '/beegfs/desy/user/brockhul/autoencoder_codes/{}.npy'.format(autoencoder_model_name)
autoencoder_model_save = 'model/{}.h5'.format(autoencoder_model_name)
encoder_save = 'model/{}_encoder.h5'.format(autoencoder_model_name)
autoencoder_log_dir = 'logs/autoencoder/'