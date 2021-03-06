import tensorflow as tf
import datetime
import cnn
import json_tools
import constants


if __name__ == '__main__':
    data_save_directory= constants.cnn_train_test_split_data_directory
    metadata_dict = json_tools.import_json_as_dict(constants.metadata_file)

    label_name = 'combination_label'
    path_to_profiles = constants.preprocessed_beam_profiles_directory + '/beam_profiles_run_{}_raw_downsized.npy'
    save_model_as = constants.cnn_model_saveas
    (x_train, y_train), (x_test, y_test) = cnn.save_and_load_profiles.load_train_test_split_data(data_save_directory,
                                                                                                 metadata_dict,
                                                                                                 label_name,
                                                                                                 path_to_profiles)

    y_train_1h = cnn.preparatory_tools.one_hot(y_train, 2)
    y_test_1h = cnn.preparatory_tools.one_hot(y_test, 2)

    model = cnn.get_model(x_train.shape[-2:])
    model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.01),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])
    model.summary()
    lr_decay_callback = tf.keras.callbacks.LearningRateScheduler(cnn.cnn_tools.lr_decay, verbose=True)

    BATCH_SIZE = 64
    steps_per_epoch = x_train.shape[0] // BATCH_SIZE
    log_dir = constants.cnn_log_dir + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
    history = model.fit(x_train, y_train_1h, batch_size=BATCH_SIZE, steps_per_epoch=steps_per_epoch,
                        epochs=8,
                        validation_data=(x_test, y_test_1h), validation_steps=1,
                        callbacks=[lr_decay_callback, tensorboard_callback])

    model.save(save_model_as)
