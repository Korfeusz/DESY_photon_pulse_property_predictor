#
#
# def to_float(lst):
#     return [float(x) for x in lst]
#
#
# experiment_info = {
#     'layer_structure': layer_structure,
#     'convolution_structure': convolution_channels,
#     'test_accuracies': to_float(test_accuracies),
#     'test_cross_entropies': to_float(test_cross_entropies),
#     'train_accuracies': to_float(train_accuracies),
#     'train_cross_entropies': to_float(train_cross_entropies),
#     'iteration_numbers': iteration_numbers,
#     'dropout_structure': dropout_structure
# }
#
# test_num = 11
# filename = 'testno_{}.json'.format(test_num)
# with open('/content/gdrive/My Drive/ml_zmad/{}'.format(filename), 'w') as f:
#     json.dump(experiment_info, fp=f)
