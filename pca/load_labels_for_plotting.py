
def load_labels(metadata_dict, indices, label_name):
    for index in indices:
        if 'label' in metadata_dict[index] and label_name in metadata_dict[index]['label']:
            yield metadata_dict[index]['label'][label_name]['value']