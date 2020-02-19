import os
import random
import cv2


def gen_train():
    # 生成训练集
    base_dir = 'data'
    data_dir = os.path.join(base_dir, 'data')
    file_names = os.listdir(data_dir)
    indexes = random.sample(range(len(file_names)), 4000)
    dir = os.path.join(base_dir, 'photos/train')
    if not os.path.exists(dir):
        os.mkdir(dir)
    for index in indexes:
        name = file_names[index]
        source = os.path.join(data_dir, name)
        target = os.path.join(dir, name)
        img = cv2.imread(source)
        img = cv2.resize(img, None, fx=0.1, fy=0.1)
        cv2.imwrite(target, img)


def gen_valid():
    # 生成验证集
    base_dir = 'data'
    data_dir = os.path.join(base_dir, 'data')
    file_names = os.listdir(data_dir)
    indexes = random.sample(range(len(file_names)), 1000)
    dir = os.path.join(base_dir, 'photos/valid')
    if not os.path.exists(dir):
        os.mkdir(dir)
    for index in indexes:
        name = file_names[index]
        source = os.path.join(data_dir, name)
        target = os.path.join(dir, name)
        img = cv2.imread(source)
        img = cv2.resize(img, None, fx=0.1, fy=0.1)
        cv2.imwrite(target, img)


def gen_test():
    # 生成测试集
    base_dir = 'data'
    data_dir = os.path.join(base_dir, 'data')
    file_names = os.listdir(data_dir)
    dir = os.path.join(base_dir, 'photos/test')
    if not os.path.exists(dir):
        os.mkdir(dir)
    for name in file_names:
        source = os.path.join(data_dir, name)
        target = os.path.join(dir, name)
        img = cv2.imread(source)
        img = cv2.resize(img, None, fx=0.1, fy=0.1)
        cv2.imwrite(target, img)


if __name__ == '__main__':
    gen_train()
    gen_valid()
    gen_test()
