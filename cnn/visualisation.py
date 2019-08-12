#
# """Visualisation"""
#
# import matplotlib.pyplot as plt
#
# filename = 'testno_11'
#
# with open('/content/gdrive/My Drive/ml_zmad/{}.json'.format(filename), 'r') as f:
#     runData = json.load(f)
#
# train_accuracy = runData['train_accuracies']
# test_accuracy = runData['test_accuracies']
# train_cross_entropy = runData['train_cross_entropies']
# test_cross_entropy = runData['test_cross_entropies']
# iterations = runData['iteration_numbers']
#
# plt.plot(iterations, train_accuracy, label="train")
# plt.plot(iterations, test_accuracy, label="test")
# plt.plot()
#
# plt.grid()
# plt.xlabel("Iteration [-]")
# plt.ylabel("Accuracy [-]")
# plt.title("Accuracies")
# plt.legend()
# plt.savefig('/content/gdrive/My Drive/ml_zmad/{}_accuracies_all.png'.format(filename))
# plt.show()
#
# start = 2
# plt.plot(iterations[start:-1], train_accuracy[start:-1], label="train")
# plt.plot(iterations[start:-1], test_accuracy[start:-1], label="test")
# plt.plot()
#
# plt.grid()
# plt.xlabel("Iteration [-]")
# plt.ylabel("Accuracy [-]")
# plt.title("Accuracies")
# plt.legend()
# plt.savefig('/content/gdrive/My Drive/ml_zmad/{}_accuracies_zoom.png'.format(filename))
# plt.show()
#
# plt.plot(iterations, train_cross_entropy, label="train")
# plt.plot(iterations, test_cross_entropy, label="test")
# plt.plot()
#
# plt.grid()
# plt.xlabel("Iteration [-]")
# plt.ylabel("Cross Entropy [-]")
# plt.title("Cross Entropies")
# plt.legend()
# plt.savefig('/content/gdrive/My Drive/ml_zmad/{}_crossentropies_all.png'.format(filename))
# plt.show()
#
# start = 2
# plt.plot(iterations[start:-1], train_cross_entropy[start:-1], label="train")
# plt.plot(iterations[start:-1], test_cross_entropy[start:-1], label="test")
# plt.plot()
#
# plt.grid()
# plt.xlabel("Iteration [-]")
# plt.ylabel("Cross Entropy [-]")
# plt.title("Cross Entropies")
# plt.legend()
# plt.savefig('/content/gdrive/My Drive/ml_zmad/{}_crossentropies_zoom.png'.format(filename))
# plt.show()
#
# max(train_accuracy)
#
# max(test_accuracy)
#
# test_accuracy[-1]
#
# train_accuracy[-1]
