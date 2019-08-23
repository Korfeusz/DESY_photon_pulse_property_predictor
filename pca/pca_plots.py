import colorsys
import numpy as np
from matplotlib import cm as cm, pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_scatter(principal_components, labels, axes=(0, 1), title=None, sort_colors=False, save=None):
    n = len(set(labels))
    rgb = cm.rainbow(np.linspace(0.0, 1.0, n))
    if sort_colors:
        sorting_dict = dict([(x, y) for x, y in zip(sorted(set(labels)), range(len(set(labels))))])
        rgb = [rgb[sorting_dict[x]] for x in set(labels)]
    for i, label in enumerate(set(labels)):
        mask = labels == label
        plt.scatter(principal_components[mask, axes[0]], principal_components[mask, axes[1]], c=rgb[i], s=0.1,
                    label=label, alpha=0.5)

    plt.title(title)
    plt.legend(markerscale=30)
    if save is not None:
        plt.savefig(save)
    plt.show()


def plot_scatter_continuous(principal_components, continuous_labels, title=None, save=None):
    rgb = cm.rainbow(np.linspace(0.0, 1.0, len(continuous_labels)))
    sorting_dict = dict([(x, y) for x, y in zip(sorted(continuous_labels), range(len(continuous_labels)))])
    rgb = [rgb[sorting_dict[x]] for x in continuous_labels]
    plt.scatter(principal_components[:, 0], principal_components[:, 1], c=rgb, s=0.2)
    plt.title(title)
    if save is not None:
        plt.savefig(save)
    plt.show()


def plot_scatter_3d(principal_components, labels):
    n = len(set(labels))
    hsv = [(x * 1.0 / n, 0.5, 0.5) for x in range(n)]
    rgb = list(map(lambda x: colorsys.hsv_to_rgb(*x), hsv))
    fig = plt.figure()
    ax = Axes3D(fig)
    for i, label in enumerate(set(labels)):
        mask = labels == label
        ax.scatter(principal_components[mask, 0], principal_components[mask, 1], principal_components[mask, 2],
                   c=rgb[i], s=1)
