import tensorflow as tf
from autoencoder.model import get_autoencoder
from autoencoder.data_import import get_train_test_split_data, create_autoencoder_label
from autoencoder.autoencoder_visualisation import visualise_results
from autoencoder.run_saving import add_autoencoder_run_to_metadata
import numpy as np
import json_tools


def lr_decay(epoch):
    return 0.01 * np.power(0.95, epoch)


if __name__ == '__main__':
    metadata_file = 'metadata/metadata.json'
    data_storage_filename = '/beegfs/desy/user/brockhul/preprocessed_data_2/beam_profiles_run_{}_raw_downsized.npy'
    final_shape = (32, 32)
    model_name = 'autoencoder_tst'
    codes_save = '/beegfs/desy/user/brockhul/autoencoder_codes/{}.npy'.format(model_name)
    model_save = 'model/{}.h5'.format(model_name)
    encoder_save = 'model/{}_encoder.h5'.format(model_name)
    log_dir = 'logs/autoencoder/'

    metadata_dict = json_tools.import_json_as_dict(metadata_file)
    create_autoencoder_label(data_storage_filename, metadata_file, fraction_of_train=0.8)

    (x_train, train_indices), (x_test, test_indices), (all_profiles, all_indices) = get_train_test_split_data(
        data_storage_filename, metadata_dict,
        normalize=True,
        cut_to=final_shape, reshape=True)

    input_img, encoded, decoded = get_autoencoder(x_train.shape[1:3])
    autoencoder = tf.keras.models.Model(input_img, decoded)
    autoencoder.summary()
    autoencoder.compile(optimizer=tf.keras.optimizers.Adam(lr=0.01),
                        loss='mean_squared_error')

    lr_decay_callback = tf.keras.callbacks.LearningRateScheduler(lr_decay, verbose=True)

    autoencoder.fit(x_train, x_train,
                    epochs=20,
                    batch_size=512,
                    shuffle=True,
                    validation_data=(x_test, x_test),
                    callbacks=[tf.keras.callbacks.TensorBoard(log_dir=log_dir), lr_decay_callback])

    decoded_images = autoencoder.predict(x_test)
    visualise_results(x_test, decoded_images, n=10)


    encoder = tf.keras.models.Model(input_img, encoded)
    encoded_images = encoder.predict(all_profiles)
    np.save(codes_save, encoded_images)
    autoencoder.save(model_save)
    encoder.save(encoder_save)
    add_autoencoder_run_to_metadata(metadata_file, code_filename=codes_save,
                                    model_filename=model_save,
                                    indices=all_indices,
                                    encoder_file=encoder_save)
