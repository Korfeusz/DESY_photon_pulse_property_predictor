import matplotlib.pyplot as plt


def visualise_results(x_test, decoded_images, n=10):
    plt.figure(figsize=(20, 4))
    shape = x_test.shape[1:3]
    for i in range(n):
        ax = plt.subplot(2, n, i + 1)
        plt.imshow(x_test[i].reshape(*shape), cmap=plt.cm.jet)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        ax = plt.subplot(2, n, i + 1 + n)
        plt.imshow(decoded_images[i].reshape(*shape), cmap=plt.cm.jet)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    plt.show()
