import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET
from image_uitls import transform_img


def load_tagging(tagging_file):
    tree = ET.parse(tagging_file)
    taggings = tree.findall('Photo')
    tagging_dict = {}
    for i, tagging in enumerate(taggings):
        name = tagging.find('Name').text
        tag = int(tagging.find('Tagging').text)
        tagging_dict[name] = {'name': name, 'tag': tag}
    return tagging_dict


def data_loader(data_dir, tagging_file, batch_size=10, mode='train'):
    tagging_dict = load_tagging(tagging_file)
    file_names = os.listdir(data_dir)

    def reader():
        if mode == 'train':
            np.random.shuffle(file_names)
        batch_imgs = []
        batch_labels = []
        for file_name in file_names:
            name = file_name

            try:
                img = cv2.imread(os.path.join(data_dir, file_name))
                img = transform_img(img)
            except Exception:
                print("read image fail.{}".format(name))
                continue

            label = 0
            tagging = tagging_dict.get(name)
            if tagging is not None:
                label = tagging['tag']
            batch_imgs.append(img)
            batch_labels.append(label)
            if len(batch_imgs) == batch_size:
                img_array = np.array(batch_imgs).astype('float32')
                labels_array = np.array(batch_labels).astype('float32').reshape(-1, 1)
                yield img_array, labels_array
                batch_imgs = []
                batch_labels = []
        if len(batch_imgs) > 0:
            img_array = np.array(batch_imgs).astype('float32')
            labels_array = np.array(batch_labels).astype('float32').reshape(-1, 1)
            yield img_array, labels_array

    return reader


if __name__ == '__main__':
    data_dir = 'data/photos/train'
    tagging_file = 'data/photos/tagging.xml'
    train_loader = data_loader(data_dir, tagging_file)
    train_img, train_label = next(train_loader())
    print(train_img.shape)
    print(train_label.shape)
