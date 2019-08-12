import profile_loading
import json_tools
from cnn import preparatory_tools
import numpy as np
import tensorflow as tf
import datetime

if __name__ == '__main__':
    metadata_dict = json_tools.import_json_as_dict('../metadata/meta_test_1.json')
    (x_train, y_train), (x_test, y_test) = profile_loading.get_train_test_split_data(metadata_dict,
                                                                                     label_name='experimental_combo',
                                                                                     path_to_data='../preprocessed_data/beam_profiles_run_{}_raw_small.npy',
                                                                                     runs=[0, 1, 2, 3])
    shape_0, shape_1 = x_train.shape[-2:]
    y_train_1h = preparatory_tools.one_hot(y_train, 2)
    y_test_1h = preparatory_tools.one_hot(y_test, 2)
    x_train_reshaped = np.reshape(x_train, (-1, shape_0, shape_1, 1))
    x_test_reshaped = np.reshape(x_test, (-1, shape_0, shape_1, 1))

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Reshape(input_shape=(shape_0, shape_1,), target_shape=(shape_0, shape_1, 1)),

            tf.keras.layers.Conv2D(kernel_size=3, filters=12, use_bias=False, padding='same'),
            tf.keras.layers.BatchNormalization(center=True, scale=False),
            tf.keras.layers.Activation('relu'),

            tf.keras.layers.Conv2D(kernel_size=6, filters=24, use_bias=False, padding='same', strides=2),
            tf.keras.layers.BatchNormalization(center=True, scale=False),
            tf.keras.layers.Activation('relu'),

            tf.keras.layers.Conv2D(kernel_size=6, filters=32, use_bias=False, padding='same', strides=2),
            tf.keras.layers.BatchNormalization(center=True, scale=False),
            tf.keras.layers.Activation('relu'),

            tf.keras.layers.Flatten(),

            tf.keras.layers.Dense(200, use_bias=False),
            tf.keras.layers.BatchNormalization(center=True, scale=False),
            tf.keras.layers.Activation('relu'),

            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(2, activation='softmax')
        ])

    model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.01),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # print model layers
    model.summary()


    # lr decay function
    def lr_decay(epoch):
        return 0.01 * np.power(0.666, epoch)


    # lr schedule callback
    lr_decay_callback = tf.keras.callbacks.LearningRateScheduler(lr_decay, verbose=True)


    BATCH_SIZE = 50
    steps_per_epoch = 100 // BATCH_SIZE  # 60,000 items in this dataset
    print("Steps per epoch: ", steps_per_epoch)

    log_dir = "../logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

    history = model.fit(x_train, y_train_1h, steps_per_epoch=steps_per_epoch, epochs=2,
                        validation_data=(x_test, y_test_1h), validation_steps=1,
                        callbacks=[lr_decay_callback, tensorboard_callback])


