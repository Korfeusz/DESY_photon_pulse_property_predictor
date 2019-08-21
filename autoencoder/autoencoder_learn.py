import tensorflow as tf
from autoencoder.model import get_autoencoder
from cnn.save_and_load_profiles import load_profiles
from autoencoder.data_import import cut_data_to_size
import numpy as np
import matplotlib.pyplot as plt
from cnn.cnn_tools import lr_decay
import json_tools
import cnn_evaluation

if __name__ == '__main__':
    # (x_train, _), (x_test, _) = load_profiles()

    metadata_dict = json_tools.import_json_as_dict('../metadata/metadata_1.json')
    data_storage_filename='/beegfs/desy/user/brockhul/preprocessed_data/beam_profiles_run_{}_raw_lowcolor_downsized.npy'
    all_data = cnn_evaluation.get_all_uncorrupted_beam_profiles(data_storage_filename=data_storage_filename,
                                                   metadata_dict=metadata_dict)
    np.random.shuffle(all_data)
    x_train = all_data[:-1000, :, :]
    x_test = all_data[-1000:, :, :]
    final_shape = (16, 16)
    x_train = cut_data_to_size(x_train, image_shape=final_shape)
    x_test = cut_data_to_size(x_test, image_shape=final_shape)

    train_shape = x_train.shape
    test_shape = x_test.shape
    x_train = x_train.astype('float16') / np.max(np.max(x_train, axis=1), axis=1).reshape((train_shape[0], 1, 1))
    x_test = x_test.astype('float16') / np.max(np.max(x_test, axis=1), axis=1).reshape((test_shape[0], 1, 1))

    train_shape = x_train.shape
    test_shape = x_test.shape

    input_img, encoded, decoded = get_autoencoder(train_shape[-2:])

    autoencoder = tf.keras.models.Model(input_img, decoded)

    autoencoder.summary()

    # autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

    autoencoder.compile(optimizer=tf.keras.optimizers.Adam(lr=0.01),
                        loss='binary_crossentropy')

    x_train = np.reshape(x_train, (train_shape[0], train_shape[1], train_shape[2], 1))
    x_test = np.reshape(x_test, (test_shape[0], test_shape[1], test_shape[2], 1))

    lr_decay_callback = tf.keras.callbacks.LearningRateScheduler(lr_decay, verbose=True)

    autoencoder.fit(x_train, x_train,
                    epochs=50,
                    batch_size=512,
                    shuffle=True,
                    validation_data=(x_test, x_test),
                    callbacks=[tf.keras.callbacks.TensorBoard(log_dir="../logs/autoencoder/")
                            ])

    decoded_imgs = autoencoder.predict(x_test)

    n = 10
    plt.figure(figsize=(20, 4))
    for i in range(n):
        # display original
        ax = plt.subplot(2, n, i + 1)
        plt.imshow(x_test[i].reshape(*final_shape), cmap=plt.cm.jet)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # display reconstruction
        ax = plt.subplot(2, n, i + 1 + n)
        plt.imshow(decoded_imgs[i].reshape(*final_shape), cmap=plt.cm.jet)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    plt.show()