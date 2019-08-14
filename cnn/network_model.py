import tensorflow as tf


def get_model(image_shape):
    shape_0, shape_1 = image_shape
    return tf.keras.Sequential(
            [
                tf.keras.layers.Reshape(input_shape=(shape_0, shape_1,), target_shape=(shape_0, shape_1, 1)),

                tf.keras.layers.Conv2D(kernel_size=3, filters=6, use_bias=False, padding='same'),
                tf.keras.layers.BatchNormalization(center=True, scale=False),
                tf.keras.layers.Activation('relu'),

                tf.keras.layers.Conv2D(kernel_size=6, filters=6, use_bias=False, padding='same', strides=2),
                tf.keras.layers.BatchNormalization(center=True, scale=False),
                tf.keras.layers.Activation('relu'),

                # tf.keras.layers.Conv2D(kernel_size=6, filters=32, use_bias=False, padding='same', strides=2),
                # tf.keras.layers.BatchNormalization(center=True, scale=False),
                # tf.keras.layers.Activation('relu'),

                tf.keras.layers.Flatten(),

                tf.keras.layers.Dense(20, use_bias=False),
                tf.keras.layers.BatchNormalization(center=True, scale=False),
                tf.keras.layers.Activation('relu'),

                tf.keras.layers.Dropout(0.3),
                tf.keras.layers.Dense(2, activation='softmax')
            ])
