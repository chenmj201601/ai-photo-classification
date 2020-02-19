import cv2
import numpy as np
import os


# 对读入的图像数据进行预处理
def transform_img(img):
    # 将图片尺寸缩放道 224x224
    img = cv2.resize(img, (224, 224))
    # 读入的图像数据格式是[H, W, C]
    # 使用转置操作将其变成[C, H, W]
    img = np.transpose(img, (2, 0, 1))
    img = img.astype('float32')
    # 将数据范围调整到[-1.0, 1.0]之间
    img = img / 255.
    img = img * 2.0 - 1.0
    return img


# 照片缩放
def resize_img(source_dir, target_dir):
    file_names = os.listdir(source_dir)
    for file_name in file_names:
        source = os.path.join(source_dir, file_name)
        target = os.path.join(target_dir, file_name)
        img = cv2.imread(source)
        # img = cv2.resize(img, (224, 224))
        img = cv2.resize(img, None, fx=0.2, fy=0.2)
        cv2.imwrite(target, img)


if __name__ == '__main__':
    source_dir = 'data/photos/valid'
    target_dir = 'data/photos/valid_resize'
    os.makedirs(target_dir)
    resize_img(source_dir, target_dir)
