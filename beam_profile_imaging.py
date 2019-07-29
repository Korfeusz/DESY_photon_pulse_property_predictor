import matplotlib.pyplot as plt
import numpy as np


def save_beam_profile_image(beam_profile, name='save_test.png'):
    plt.imsave(name,
               beam_profile,
               cmap=plt.cm.jet)


# def show_images(images, rows=1):
#     n_images = len(images)
#     fig = plt.figure()
#     for n, image in enumerate(images):
#         a = fig.add_subplot(rows, np.ceil(n_images / float(rows)), n + 1)
#         a.axis('off')
#         plt.imshow(image, cmap=plt.cm.jet)
#     plt.show()


def show_images(images, rows=1, title='test', saveas=None):
    n_images = len(images)
    fig = plt.figure()
    for n, image in enumerate(images):
        a = fig.add_subplot(rows, np.ceil(n_images / float(rows)), n + 1)
        a.axis('off')
        if n < np.ceil(n_images / float(rows)):
            a.set_title(str(n), loc='left')
        plt.imshow(image, cmap=plt.cm.jet)
    fig.suptitle(title)
    if saveas:
        plt.savefig(saveas)
    plt.close()


if __name__ == '__main__':
    import beam_profiles_pipeline
    import file_tools

    image_number = 38
    profiles_range = (0, 100)
    h_min, h_max, v_min, v_max = 105, 364, 90, 349
    # h_min, h_max, v_min, v_max = 0, 483, 0, 360
    final_color_resolution = 63
    run_number = 8

    for run_number in range(2):
        with file_tools.get_run(run_number=run_number) as current_run:
            beam_profiles_raw = file_tools \
                .get_beam_profiles_pipeline(current_run=current_run, clip_to_profiles=False) \
                .slice_horizontally(h_min=h_min, h_max=h_max) \
                .slice_vertically(v_min=v_min, v_max=v_max) \
                .get_rounded_beam_profiles()

            image_number = beam_profiles_raw.shape[0]
            for low_bound in range(0, image_number, 100):
                print(low_bound)
                beam_profiles_print = beam_profiles_raw[low_bound:(low_bound + 100), :, :]
                title = 'Run: {}, Profiles num: {}:{}'.format(run_number, low_bound, (low_bound + 100))
                savetitle = 'run_{}_profiles_{}_{}.png'.format(run_number, low_bound, (low_bound + 100))
                show_images(beam_profiles_print, rows=10, title=title, saveas=savetitle)

