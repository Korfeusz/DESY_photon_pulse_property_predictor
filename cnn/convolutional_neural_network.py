from cnn import preparatory_tools
import tensorflow as tf
import datetime
import cnn

if __name__ == '__main__':
    (x_train, y_train), (x_test, y_test) = cnn.save_and_load_profiles.load_profiles()


    y_train_1h = preparatory_tools.one_hot(y_train, 2)
    y_test_1h = preparatory_tools.one_hot(y_test, 2)


    model = cnn.get_model(x_train.shape[-2:])
    model.compile(optimizer=tf.keras.optimizers.Adam(lr=0.01),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    # print model layers
    # model.summary()
    lr_decay_callback = tf.keras.callbacks.LearningRateScheduler(cnn.cnn_tools.lr_decay, verbose=True)


    BATCH_SIZE = 64
    steps_per_epoch = x_train.shape[0] // BATCH_SIZE  # 60,000 items in this dataset
    log_dir = "../logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + '_test_4_huge'
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir)

    history = model.fit(x_train, y_train_1h, batch_size=BATCH_SIZE, steps_per_epoch=steps_per_epoch,
                        epochs=25,
                        validation_data=(x_test, y_test_1h), validation_steps=1,
                        callbacks=[lr_decay_callback, tensorboard_callback])

    model.save('../model/model_1.h5')
