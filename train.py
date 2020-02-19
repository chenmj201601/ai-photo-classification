import datetime
import paddle.fluid as fluid
import numpy as np
from reader import data_loader
from figure_utils import draw_figure
from vggnet import VGG

NUM_EPOCH = 30
BATCH_SIZE = 20


def train(model, train_dir, valid_dir, tagging_file):
    with fluid.dygraph.guard():
        print('start training ... ')
        begin = datetime.datetime.now()
        model.train()
        epoch_num = NUM_EPOCH
        all_acc = []
        all_val_acc = []
        all_loss = []
        all_val_loss = []
        # 定义优化器
        opt = fluid.optimizer.Momentum(learning_rate=0.001, momentum=0.9)
        # 定义数据读取器，训练数据读取器和验证数据读取器
        train_loader = data_loader(train_dir, tagging_file, batch_size=BATCH_SIZE, mode='train')
        valid_loader = data_loader(valid_dir, tagging_file, batch_size=BATCH_SIZE, mode='valid')
        for epoch in range(epoch_num):
            accuracies = []
            losses = []
            for batch_id, data in enumerate(train_loader()):
                x_data, y_data = data
                img = fluid.dygraph.to_variable(x_data)
                label = fluid.dygraph.to_variable(y_data)
                logits = model(img)
                # 二分类问题，计算精度
                pred = fluid.layers.sigmoid(logits)
                pred2 = pred * (-1.0) + 1.0
                pred = fluid.layers.concat([pred2, pred], axis=1)
                acc = fluid.layers.accuracy(pred, fluid.layers.cast(label, dtype='int64'))
                loss = fluid.layers.sigmoid_cross_entropy_with_logits(logits, label)
                avg_loss = fluid.layers.mean(loss)
                if batch_id % 50 == 0:
                    print("epoch: {}, batch_id: {}, loss is: {}".format(epoch, batch_id, avg_loss.numpy()))
                # 反向传播，更新权重，清除梯度
                avg_loss.backward()
                opt.minimize(avg_loss)
                model.clear_gradients()
                accuracies.append(acc.numpy())
                losses.append(loss.numpy())
            print("[train] accuracy/loss: {}/{}".format(np.mean(accuracies), np.mean(losses)))
            all_acc.append(np.mean(accuracies))
            all_loss.append(np.mean(losses))

            # 每5轮过后保存模型参数
            if (epoch % 5 == 0) or (epoch == epoch_num - 1):
                fluid.save_dygraph(model.state_dict(), 'photo_clf_{}'.format(epoch))

            model.eval()
            accuracies = []
            losses = []
            for batch_id, data in enumerate(valid_loader()):
                x_data, y_data = data
                img = fluid.dygraph.to_variable(x_data)
                label = fluid.dygraph.to_variable(y_data)
                logits = model(img)
                pred = fluid.layers.sigmoid(logits)
                pred2 = pred * (-1.0) + 1.0
                pred = fluid.layers.concat([pred2, pred], axis=1)
                acc = fluid.layers.accuracy(pred, fluid.layers.cast(label, dtype='int64'))
                loss = fluid.layers.sigmoid_cross_entropy_with_logits(logits, label)
                accuracies.append(acc.numpy())
                losses.append(loss.numpy())
            print("[validation] accuracy/loss: {}/{}".format(np.mean(accuracies), np.mean(losses)))
            all_val_acc.append(np.mean(accuracies))
            all_val_loss.append(np.mean(losses))

            # 绘图，每5轮绘制一个趋势图
            if (epoch % 5 == 0) or (epoch == epoch_num - 1):
                count = len(all_acc)
                if count > 2:
                    sub_all_acc = all_acc[2:]
                    sub_all_val_acc = all_val_acc[2:]
                    sub_all_loss = all_loss[2:]
                    sub_all_val_loss = all_val_loss[2:]
                    draw_figure(sub_all_acc, sub_all_val_acc, sub_all_loss, sub_all_val_loss)

            model.train()

        end = datetime.datetime.now()
        seconds = (end - begin).seconds
        print("finished. total cost {}".format(datetime.timedelta(seconds=seconds)))


if __name__ == '__main__':
    train_dir = 'data/photos/train'
    valid_dir = 'data/photos/valid'
    tagging_file = 'data/photos/tagging.xml'
    with fluid.dygraph.guard():
        model = VGG('vgg')
    train(model, train_dir, valid_dir, tagging_file)
