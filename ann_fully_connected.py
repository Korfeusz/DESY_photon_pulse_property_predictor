import tensorflow as tf
import numpy as np
import time
import math
from google.colab import drive
import json

def one_hot(data, num_classes):
    length = data.shape[0]
    one_hot = np.zeros((length, num_classes))
    one_hot[np.arange(length), data] = 1
    return one_hot

def next_batch(remaining_set, training_set, batch_size=64):
    x, y = remaining_set
    length = x.shape[0]
    if batch_size > length:
        return (x, y), training_set
    mask = np.zeros(length, dtype=np.bool)
    idx = np.random.choice(length, batch_size, replace=False)
    mask[idx] = True
    x_batch = x[mask]
    x_rest = x[~mask]
    y_batch = y[mask]
    y_rest = y[~mask]
    return (x_batch, y_batch), (x_rest, y_rest)

dataset = 'mnist'
if dataset == 'mnist':
  (x_train, y_train), (x_test, y_test) =  tf.keras.datasets.mnist.load_data()
elif dataset == 'fashion':
  (x_train, y_train), (x_test, y_test) =  tf.keras.datasets.fashion_mnist.load_data()
y_train_1h = one_hot(y_train, 10)
y_test_1h = one_hot(y_test, 10)
x_train_reshaped = np.reshape(x_train, (-1, 28, 28, 1)) / np.max(x_train)
x_test_reshaped = np.reshape(x_test, (-1, 28, 28, 1)) / np.max(x_test)

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
    weights.append(tf.Variable(tf.truncated_normal(shape=[3, 3, w1, w2] ,stddev=0.1)))
    biases.append(tf.Variable(tf.ones([w2])/10))
    x = tf.nn.conv2d(x, weights[-1], strides=[1, 1, 1, 1], padding='SAME')
    x = tf.nn.bias_add(x, biases[-1])
    x = tf.nn.relu(x)
    layers.append(tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],padding='SAME'))
    x = layers[-1]
  return layers

def reshape_convolution_output(convolution_channels, convolution_layers):
  num_layers = len(convolution_channels) - 1
  out_im_size = 4*4
  flattened_out = tf.reshape(convolution_layers[-1], [-1, out_im_size* convolution_channels[-1]])
  return flattened_out

def get_layers(layer_structure, flat_input, dropout_structure):
  weights = []
  biases = []
  layer_out_wo_activation = []
  weight_structure = list(zip(layer_structure, layer_structure[1:]))
  for w1, w2 in weight_structure:
    weights.append(tf.Variable(tf.truncated_normal([w1, w2] ,stddev=0.1)))
    biases.append(tf.Variable(tf.ones([w2])/10))
    layer_out_wo_activation.append(tf.matmul(flat_input, weights[-1]) + biases[-1])
    flat_input = layer_out_wo_activation[-1]
  layer_out = [tf.nn.relu(x) for x in layer_out_wo_activation[:-1]]
  layer_out.append(layer_out_wo_activation[-1])
  layer_out = make_dropout(layer_out, dropout_structure=dropout_structure)
  return layer_out

# # Convolution + 200 + 100 + dropout 2x - tst 1
# layer_structure = [4*4*128, 200, 100, 10]
# convolution_channels = [1, 32, 64, 128]
# dropout_structure = {'rate': [0.25, 0.25], 'layer': [1, 2]}
# # Convolution + 200 + 100 + dropout 1x - tst 2
# layer_structure = [4*4*128, 200, 100, 10]
# convolution_channels = [1, 32, 64, 128]
# dropout_structure = {'rate': [0.25], 'layer': [1]}
# Convolution + 200 +100 - tst 3
# layer_structure = [4*4*128, 200, 100, 10]
# convolution_channels = [1, 32, 64, 128]
# dropout_structure = {'rate': [], 'layer': []}

# # Convolution + 20 - tst 4
# layer_structure = [4*4*128, 20, 10]
# convolution_channels = [1, 32, 64, 128]
# dropout_structure = {'rate': [], 'layer': []}

# # 200 + 100 + 50 - tst 5
# layer_structure = [784, 200, 100, 50, 10]
# convolution_channels = None
# dropout_structure = {'rate': [], 'layer': []}
# 200 + 100- tst 6
# layer_structure = [784, 200, 100, 10]
# convolution_channels = None
# dropout_structure = {'rate': [], 'layer': []}
# # 20 + 10- tst 7
# layer_structure = [784, 20, 10, 10]
# convolution_channels = None
# dropout_structure = {'rate': [], 'layer': []}
# # 200 + 100 + dropout (lub 200 100 50) - tst 8
# layer_structure = [784, 200, 100, 10]
# convolution_channels = None
# dropout_structure = {'rate': [0.7], 'layer': [1]}

# # Convolution + 200 + 100 + dropout - tst 10
layer_structure = [4*4*128, 200, 100, 10]
convolution_channels = [1, 32, 64, 128]
dropout_structure = {'rate': [0.5], 'layer': [1]}

if convolution_channels is not None:
  X = tf.placeholder(tf.float32, [None, 28, 28, 1])
  Y_labels = tf.placeholder(tf.float32, [None, 10])
  convolution_layers = get_convolutional_layers(convolution_channels, X)
  convolution_flat_out = reshape_convolution_output(convolution_channels, convolution_layers)
  y_layers = get_layers(layer_structure=layer_structure, flat_input=convolution_flat_out, dropout_structure=dropout_structure)
else:
  X = tf.placeholder(tf.float32, [None, 28, 28, 1])
  X_flat = tf.reshape(X, [-1, 784])
  Y_labels = tf.placeholder(tf.float32, [None, 10])
  y_layers = get_layers(layer_structure=layer_structure, flat_input=X_flat, dropout_structure=dropout_structure)

"""Info o softmax_cross_entropy

WARNING: This op expects unscaled logits, since it performs a softmax on logits internally for efficiency. Do not call this op with the output of soft
max, as it will produce incorrect results.
"""

step = tf.Variable(0, trainable=False)
learning_rate = 0.0001 + tf.train.exponential_decay(0.003, step, 2000, 1/math.e)    
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=Y_labels, logits=y_layers[-1]))
train_step  = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cross_entropy, global_step=step)
is_correct = tf.equal(tf.argmax(y_layers[-1], 1), tf.argmax(Y_labels, 1))
accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))

remaining_set = (x_train_reshaped, y_train_1h)
test_data = {X: x_test_reshaped, Y_labels: y_test_1h}

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

test_accuracies = []
test_cross_entropies = []
train_accuracies = []
train_cross_entropies = []
iteration_numbers = []
start_time = time.time()
for i in range(10000):
    (batch_X, batch_Y), remaining_set = next_batch(remaining_set, (x_train_reshaped, y_train_1h), batch_size=100)
    train_data={X: batch_X, Y_labels: batch_Y}
    sess.run(train_step, feed_dict=train_data)
    if (i + 1) % 100 == 0 or i == 0:
        test_acc, test_cross_entropy = sess.run([accuracy, cross_entropy], feed_dict=test_data)
        train_acc, train_cross_entropy = sess.run([accuracy, cross_entropy], feed_dict=train_data)
        test_accuracies.append(test_acc)
        test_cross_entropies.append(test_cross_entropy)
        train_accuracies.append(train_acc)
        train_cross_entropies.append(train_cross_entropy)
        iteration_numbers.append(i)
    if (i + 1) % 500 == 0 or i == 0:
        print('iteration: {}, train: a: {}, c: {}, test: a: {}, c: {}, time: {}s'.format(i + 1, train_acc, train_cross_entropy,
                                                                                         test_acc, test_cross_entropy, (time.time() - start_time)))

a_, c_ = sess.run([accuracy, cross_entropy], feed_dict=test_data)
a, c = sess.run([accuracy, cross_entropy], feed_dict=train_data)
print('train: a: {}, c: {}, test: a: {}, c: {}, total time: {}'.format(a_, c_, a, c,  (time.time() - start_time)))

"""Data Save"""

def to_float(lst):
  return [float(x) for x in lst]

experiment_info = {
    'dataset': dataset,
    'layer_structure': layer_structure,
    'convolution_structure': convolution_channels,
    'test_accuracies': to_float(test_accuracies),
    'test_cross_entropies': to_float(test_cross_entropies),
    'train_accuracies': to_float(train_accuracies),
    'train_cross_entropies': to_float(train_cross_entropies),
    'iteration_numbers': iteration_numbers,
    'dropout_structure': dropout_structure  
}

test_num = 11
filename = 'testno_{}.json'.format(test_num)
with open('/content/gdrive/My Drive/ml_zmad/{}'.format(filename), 'w') as f:
  json.dump(experiment_info, fp=f)

"""Visualisation"""

import matplotlib.pyplot as plt

filename = 'testno_11'

with open('/content/gdrive/My Drive/ml_zmad/{}.json'.format(filename), 'r') as f:
  runData = json.load(f)

train_accuracy = runData['train_accuracies']
test_accuracy = runData['test_accuracies']
train_cross_entropy = runData['train_cross_entropies']
test_cross_entropy = runData['test_cross_entropies']
iterations = runData['iteration_numbers']

plt.plot(iterations, train_accuracy, label="train")
plt.plot(iterations, test_accuracy, label="test")
plt.plot()

plt.grid()
plt.xlabel("Iteration [-]")
plt.ylabel("Accuracy [-]")
plt.title("Accuracies")
plt.legend()
plt.savefig('/content/gdrive/My Drive/ml_zmad/{}_accuracies_all.png'.format(filename))
plt.show()

start = 2
plt.plot(iterations[start:-1], train_accuracy[start:-1], label="train")
plt.plot(iterations[start:-1], test_accuracy[start:-1], label="test")
plt.plot()

plt.grid()
plt.xlabel("Iteration [-]")
plt.ylabel("Accuracy [-]")
plt.title("Accuracies")
plt.legend()
plt.savefig('/content/gdrive/My Drive/ml_zmad/{}_accuracies_zoom.png'.format(filename))
plt.show()

plt.plot(iterations, train_cross_entropy, label="train")
plt.plot(iterations, test_cross_entropy, label="test")
plt.plot()

plt.grid()
plt.xlabel("Iteration [-]")
plt.ylabel("Cross Entropy [-]")
plt.title("Cross Entropies")
plt.legend()
plt.savefig('/content/gdrive/My Drive/ml_zmad/{}_crossentropies_all.png'.format(filename))
plt.show()

start = 2
plt.plot(iterations[start:-1], train_cross_entropy[start:-1], label="train")
plt.plot(iterations[start:-1], test_cross_entropy[start:-1], label="test")
plt.plot()

plt.grid()
plt.xlabel("Iteration [-]")
plt.ylabel("Cross Entropy [-]")
plt.title("Cross Entropies")
plt.legend()
plt.savefig('/content/gdrive/My Drive/ml_zmad/{}_crossentropies_zoom.png'.format(filename))
plt.show()

max(train_accuracy)

max(test_accuracy)

test_accuracy[-1]

train_accuracy[-1]

