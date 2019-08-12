import profile_loading
import json_tools
from cnn import preparatory_tools
import numpy as np
import tensorflow as tf
import datetime
import cnn

if __name__ == '__main__':
    metadata_dict = json_tools.import_json_as_dict('../metadata/meta_test_1.json')
    (x_train, y_train), (x_test, y_test) = profile_loading.get_train_test_split_data(metadata_dict,
                                                                                     label_name='experimental_combo',
                                                                                     path_to_data='../preprocessed_data/beam_profiles_run_{}_raw_small.npy',
                                                                                     runs=[0, 1, 2, 3])

    y_train_1h = preparatory_tools.one_hot(y_train, 2)
    y_test_1h = preparatory_tools.one_hot(y_test, 2)


    model = cnn.get_model(x_train.shape[-2:])
    model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.01),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # print model layers
    # model.summary()
    lr_decay_callback = tf.keras.callbacks.LearningRateScheduler(cnn.cnn_tools.lr_decay, verbose=True)


    BATCH_SIZE = 20
    steps_per_epoch = 100 // BATCH_SIZE  # 60,000 items in this dataset
    log_dir = "../logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)
    history = model.fit(x_train, y_train_1h, batch_size=BATCH_SIZE, steps_per_epoch=steps_per_epoch, epochs=100,
                        validation_data=(x_test, y_test_1h), validation_steps=1,
                        callbacks=[lr_decay_callback, tensorboard_callback])


