import os
import cv2
import paddle.fluid as fluid
import argparse
from image_uitls import transform_img
from vggnet import VGG
from reader import load_tagging


def parse_args():
    parser = argparse.ArgumentParser("Evaluation Parameters")
    parser.add_argument(
        '--weight_file',
        type=str,
        default='photo_clf_10',
        help='the path of model parameters')
    args = parser.parse_args()
    return args


args = parse_args()
WEIGHT_FILE = args.weight_file


def eval(model, params_file_path, test_dir, tagging_file):
    tagging_dict = load_tagging(tagging_file)
    num_correct = 0
    num_incorrect = 0
    num_total = 0
    incorrect_pics = []
    with fluid.dygraph.guard():
        model_state_dict, _ = fluid.load_dygraph(params_file_path)
        model.load_dict(model_state_dict)
        model.eval()
        file_names = os.listdir(test_dir)
        for name in file_names:
            real_label = 0
            tagging = tagging_dict.get(name)
            if tagging is not None:
                real_label = 1 if tagging['tag'] == 101 else 0
            test_picture = os.path.join(test_dir, name)
            img = cv2.imread(test_picture)
            img = transform_img(img)
            img = img.reshape(1, 3, 224, 224)
            img = fluid.dygraph.to_variable(img)
            logits = model(img)
            result = fluid.layers.sigmoid(logits).numpy()
            score = result[0][0]
            label = 1 if score >= 0.5 else 0
            if label == real_label:
                num_correct += 1
            else:
                num_incorrect += 1
                incorrect_pics.append({
                    'name': name,
                    'predict': label,
                    'real': real_label
                })
            num_total += 1

    correct_rate = num_correct / (num_total * 1.0)
    print("total:{} num_correct:{} num_incorrect={} correct_rate={}".format(num_total,
                                                                            num_correct,
                                                                            num_incorrect,
                                                                            correct_rate))
    for pic in incorrect_pics:
        print("name:{} predict:{} real:{}".format(pic['name'], pic['predict'], pic['real']))


if __name__ == '__main__':
    param_file_path = WEIGHT_FILE
    with fluid.dygraph.guard():
        model = VGG('vgg')

    test_dir = 'data/photos/test'
    tagging_file = 'data/photos/tagging.xml'
    eval(model, param_file_path, test_dir, tagging_file)
