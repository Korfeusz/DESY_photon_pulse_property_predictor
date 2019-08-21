import json_tools


def add_autoencoder_run_to_metadata(metadata_filename, indices, model_filename, code_filename, encoder_file):
    metadata_dict = json_tools.import_json_as_dict(metadata_filename)
    for i, index in enumerate(indices):
        train_test_contents = metadata_dict[index]['autoencoder']['train_test']
        metadata_dict[index]['autoencoder'] = {'train_test': train_test_contents,
                                               'model_file': model_filename,
                                               'code_file': code_filename,
                                               'encoder_file': encoder_file,
                                               'code_index': i}
    json_tools.dump_dict_to_json(metadata_filename, metadata_dict, indent=2)
