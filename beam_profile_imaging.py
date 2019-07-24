import matplotlib.pyplot as plt


def save_beam_profile_image(beam_profile, name='save_test.png'):
    plt.imsave(name,
               beam_profile,
               cmap=plt.cm.jet)
