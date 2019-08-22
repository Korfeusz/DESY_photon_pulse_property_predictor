import tensorflow as tf




def get_autoencoder(image_shape):
    shape_0, shape_1 = image_shape
    input_img = tf.keras.layers.Input(shape=(shape_0, shape_1, 1))

    x = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', padding='same')(input_img)
    x = tf.keras.layers.MaxPooling2D((2, 2), padding='same')(x)
    # x = tf.keras.layers.BatchNormalization(center=True, scale=True)(x)
    tf.keras.layers.Dropout(0.2),

    x = tf.keras.layers.Conv2D(8, (3, 3), activation='relu', padding='same')(x)
    x = tf.keras.layers.MaxPooling2D((2, 2), padding='same')(x)
    tf.keras.layers.Dropout(0.2),

    x = tf.keras.layers.Conv2D(4, (3, 3), activation='relu', padding='same')(x)
    encoded = tf.keras.layers.MaxPooling2D((2, 2), padding='same')(x)

    x = tf.keras.layers.Conv2D(4, (3, 3), activation='relu', padding='same')(encoded)

    x = tf.keras.layers.UpSampling2D((2, 2))(x)
    x = tf.keras.layers.Conv2D(8, (3, 3), activation='relu', padding='same')(x)

    x = tf.keras.layers.UpSampling2D((2, 2))(x)
    x = tf.keras.layers.Conv2D(16, (3, 3), activation='relu', padding='same')(x)

    # x = tf.keras.layers.BatchNormalization(center=True, scale=True)(x)
    x = tf.keras.layers.UpSampling2D((2, 2))(x)
    decoded = tf.keras.layers.Conv2D(1, (3, 3), activation='sigmoid', padding='same')(x)

    return input_img, encoded, decoded


