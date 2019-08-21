import tensorflow as tf
from autoencoder.model import get_autoencoder
from autoencoder.data_import import get_train_test_split_data
from autoencoder.autoencoder_visualisation import visualise_random_results
import numpy as np
import matplotlib.pyplot as plt
from cnn.cnn_tools import lr_decay
import json_tools

if __name__ == '__main__':
    # (x_train, _), (x_test, _) = load_profiles()

    metadata_dict = json_tools.import_json_as_dict('../metadata/metadata_1.json')
    data_storage_filename='/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_lowcolor_downsized.npy'
    final_shape = (16, 16)
    (x_train, _), (x_test, _) = get_train_test_split_data(data_storage_filename, metadata_dict, normalize=True,
                                                          cut_to=final_shape, reshape=True)


    input_img, encoded, decoded = get_autoencoder(x_train.shape[1:3])
    autoencoder = tf.keras.models.Model(input_img, decoded)
    autoencoder.summary()

    # autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

    autoencoder.compile(optimizer=tf.keras.optimizers.Adam(lr=0.01),
                        loss='binary_crossentropy')

    lr_decay_callback = tf.keras.callbacks.LearningRateScheduler(lr_decay, verbose=True)

    autoencoder.fit(x_train, x_train,
                    epochs=3,
                    batch_size=512,
                    shuffle=True,
                    validation_data=(x_test, x_test),
                    callbacks=[tf.keras.callbacks.TensorBoard(log_dir="../logs/autoencoder/")])

    decoded_imgs = autoencoder.predict(x_test)

    visualise_random_results(x_test, decoded_imgs, n=10)