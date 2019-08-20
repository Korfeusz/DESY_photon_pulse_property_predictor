

def cut_data_to_size(data, image_shape=(32, 32)):
    return data[:, :image_shape[0], :image_shape[1]]
