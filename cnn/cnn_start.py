# import tensorflow as tf
# import numpy as np
# import time
# import math
# import json
# import profile_loading
# import json_tools
#
#
# if __name__ == '__main__':
#     metadata_dict = json_tools.import_json_as_dict('metadata/meta_test_1.json')
#     (x_train, y_train), (x_test, y_test) = profile_loading.get_train_test_split_data(metadata_dict,
#                                                                                      label_name='experimental_combo',
#                                                                                      path_to_data='preprocessed_data/beam_profiles_run_{}_raw_small.npy',
#                                                                                      runs=[0, 1, 2, 3])
#     y_train_1h = one_hot(y_train, 2)
#     y_test_1h = one_hot(y_test, 2)
#     x_train_reshaped = np.reshape(x_train, (-1, 28, 28, 1)) / np.max(x_train)
#     x_test_reshaped = np.reshape(x_test, (-1, 28, 28, 1)) / np.max(x_test)
#
#
#
#
#
# step = tf.Variable(0, trainable=False)
# learning_rate = 0.0001 + tf.train.exponential_decay(0.003, step, 2000, 1 / math.e)
# cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=Y_labels, logits=y_layers[-1]))
# train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cross_entropy, global_step=step)
# is_correct = tf.equal(tf.argmax(y_layers[-1], 1), tf.argmax(Y_labels, 1))
# accuracy = tf.reduce_mean(tf.cast(is_correct, tf.float32))
#
# remaining_set = (x_train_reshaped, y_train_1h)
# test_data = {X: x_test_reshaped, Y_labels: y_test_1h}
#
# init = tf.global_variables_initializer()
# sess = tf.Session()
# sess.run(init)
#
# test_accuracies = []
# test_cross_entropies = []
# train_accuracies = []
# train_cross_entropies = []
# iteration_numbers = []
# start_time = time.time()
# for i in range(10000):
#     (batch_X, batch_Y), remaining_set = next_batch(remaining_set, (x_train_reshaped, y_train_1h), batch_size=100)
#     train_data = {X: batch_X, Y_labels: batch_Y}
#     sess.run(train_step, feed_dict=train_data)
#     if (i + 1) % 100 == 0 or i == 0:
#         test_acc, test_cross_entropy = sess.run([accuracy, cross_entropy], feed_dict=test_data)
#         train_acc, train_cross_entropy = sess.run([accuracy, cross_entropy], feed_dict=train_data)
#         test_accuracies.append(test_acc)
#         test_cross_entropies.append(test_cross_entropy)
#         train_accuracies.append(train_acc)
#         train_cross_entropies.append(train_cross_entropy)
#         iteration_numbers.append(i)
#     if (i + 1) % 500 == 0 or i == 0:
#         print('iteration: {}, train: a: {}, c: {}, test: a: {}, c: {}, time: {}s'.format(i + 1, train_acc,
#                                                                                          train_cross_entropy,
#                                                                                          test_acc, test_cross_entropy,
#                                                                                          (time.time() - start_time)))
#
# a_, c_ = sess.run([accuracy, cross_entropy], feed_dict=test_data)
# a, c = sess.run([accuracy, cross_entropy], feed_dict=train_data)
# print('train: a: {}, c: {}, test: a: {}, c: {}, total time: {}'.format(a_, c_, a, c, (time.time() - start_time)))
#
