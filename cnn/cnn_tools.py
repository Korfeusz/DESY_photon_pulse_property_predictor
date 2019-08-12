def lr_decay(epoch):
    return 0.01 * np.power(0.666, epoch)