import cv2
import paddle.fluid as fluid
import argparse
from image_uitls import transform_img
from vggnet import VGG


def parse_args():
    parser = argparse.ArgumentParser("Prediction Parameters")
    parser.add_argument(
        '--weight_file',
        type=str,
        default='photo_clf_10',
        help='the path of model parameters')
    parser.add_argument(
        '--test_picture',
        type=str,
        default='data/photos/test/IMG_20171229_113113.jpg',
        help='the test picture')
    args = parser.parse_args()
    return args


args = parse_args()
WEIGHT_FILE = args.weight_file
TEST_PICTURE = args.test_picture


# 定义预测方法
def pred(model, params_file_path, test_picture):
    with fluid.dygraph.guard():
        img = cv2.imread(test_picture)
        img = transform_img(img)
        img = img.reshape(1, 3, 224, 224)
        model_state_dict, _ = fluid.load_dygraph(params_file_path)
        model.load_dict(model_state_dict)
        model.eval()
        img = fluid.dygraph.to_variable(img)
        logits = model(img)
        result = fluid.layers.sigmoid(logits).numpy()
        print("result is: {}".format(result))
        score = result[0][0]
        label = 1 if score >= 0.5 else 0
        label_name = 'Me' if score >= 0.5 else 'None'
        print("test picture is [{}]{}, the score is {}".format(label, label_name, score))


if __name__ == '__main__':
    param_file_path = WEIGHT_FILE
    test_picture = TEST_PICTURE
    with fluid.dygraph.guard():
        model = VGG('vgg')
    pred(model, param_file_path, test_picture)
