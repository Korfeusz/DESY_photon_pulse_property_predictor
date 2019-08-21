import tensorflow as tf
from autoencoder.model import get_autoencoder
from autoencoder.data_import import get_train_test_split_data
from autoencoder.autoencoder_visualisation import visualise_random_results
from autoencoder.run_saving import add_autoencoder_run_to_metadata
import numpy as np
from cnn.cnn_tools import lr_decay
import json_tools

if __name__ == '__main__':
    # (x_train, _), (x_test, _) = load_profiles()
    metadata_file = '../metadata/metadata_1.json'
    metadata_dict = json_tools.import_json_as_dict(metadata_file)
    data_storage_filename = '/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_downsized.npy'
    final_shape = (32, 32)
    (x_train, train_indices), (x_test, test_indices), (all_profiles, all_indices) = get_train_test_split_data(
        data_storage_filename, metadata_dict,
        normalize=True,
        cut_to=final_shape, reshape=True)

    input_img, encoded, decoded = get_autoencoder(x_train.shape[1:3])
    autoencoder = tf.keras.models.Model(input_img, decoded)
    autoencoder.summary()

    # autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

    autoencoder.compile(optimizer=tf.keras.optimizers.Adam(lr=0.01),
                        loss='binary_crossentropy')

    lr_decay_callback = tf.keras.callbacks.LearningRateScheduler(lr_decay, verbose=True)

    autoencoder.fit(x_train, x_train,
                    epochs=50,
                    batch_size=512,
                    shuffle=True,
                    validation_data=(x_test, x_test),
                    callbacks=[tf.keras.callbacks.TensorBoard(log_dir="../logs/autoencoder/")])

    decoded_images = autoencoder.predict(x_test)

    visualise_random_results(x_test, decoded_images, n=10)

    model_name = 'test_autoencoder'
    codes_save = '/beegfs/desy/user/brockhul/autoencoder_codes/{}.npy'.format(model_name)
    model_save = '../model/{}.h5'.format(model_name)
    encoder_save = '../model/{}_encoder.h5'.format(model_name)
    encoder = tf.keras.models.Model(input_img, encoded)
    encoded_images = encoder.predict(all_profiles)
    np.save(codes_save, encoded_images)
    autoencoder.save(model_save)
    encoder.save(encoder_save)
    add_autoencoder_run_to_metadata(metadata_file, code_filename=codes_save,
                                    model_filename=model_save,
                                    indices=all_indices,
                                    encoder_file=encoder_save)

