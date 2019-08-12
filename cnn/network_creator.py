import tensorflow as tf


def make_dropout(layers, dropout_structure):
    for rate, i in zip(dropout_structure['rate'], dropout_structure['layer']):
        layers[i] = tf.nn.dropout(layers[i], rate=rate)
    return layers


def get_convolutional_layers(convolution_channels, image_input):
    layers = []
    weights = []
    biases = []
    x = image_input
    weight_structure = list(zip(convolution_channels, convolution_channels[1:]))
    for w1, w2 in weight_structure:
        weights.append(tf.Variable(tf.truncated_normal(shape=[3, 3, w1, w2], stddev=0.1)))
        biases.append(tf.Variable(tf.ones([w2]) / 10))
        x = tf.nn.conv2d(x, weights[-1], strides=[1, 1, 1, 1], padding='SAME')
        x = tf.nn.bias_add(x, biases[-1])
        x = tf.nn.relu(x)
        layers.append(tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME'))
        x = layers[-1]
    return layers
#
#
# def reshape_convolution_output(convolution_channels, convolution_layers):
#     num_layers = len(convolution_channels) - 1
#     out_im_size = 4 * 4
#     flattened_out = tf.reshape(convolution_layers[-1], [-1, out_im_size * convolution_channels[-1]])
#     return flattened_out
#
#
# def get_layers(layer_structure, flat_input, dropout_structure):
#     weights = []
#     biases = []
#     layer_out_wo_activation = []
#     weight_structure = list(zip(layer_structure, layer_structure[1:]))
#     for w1, w2 in weight_structure:
#         weights.append(tf.Variable(tf.truncated_normal([w1, w2], stddev=0.1)))
#         biases.append(tf.Variable(tf.ones([w2]) / 10))
#         layer_out_wo_activation.append(tf.matmul(flat_input, weights[-1]) + biases[-1])
#         flat_input = layer_out_wo_activation[-1]
#     layer_out = [tf.nn.relu(x) for x in layer_out_wo_activation[:-1]]
#     layer_out.append(layer_out_wo_activation[-1])
#     layer_out = make_dropout(layer_out, dropout_structure=dropout_structure)
#     return layer_out
#
# if convolution_channels is not None:
#     X = tf.placeholder(tf.float32, [None, 28, 28, 1])
#     Y_labels = tf.placeholder(tf.float32, [None, 10])
#     convolution_layers = get_convolutional_layers(convolution_channels, X)
#     convolution_flat_out = reshape_convolution_output(convolution_channels, convolution_layers)
#     y_layers = get_layers(layer_structure=layer_structure, flat_input=convolution_flat_out,
#                           dropout_structure=dropout_structure)
# else:
#     X = tf.placeholder(tf.float32, [None, 28, 28, 1])
#     X_flat = tf.reshape(X, [-1, 784])
#     Y_labels = tf.placeholder(tf.float32, [None, 10])
#     y_layers = get_layers(layer_structure=layer_structure, flat_input=X_flat, dropout_structure=dropout_structure)
