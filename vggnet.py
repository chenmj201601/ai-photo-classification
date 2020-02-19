import paddle.fluid as fluid
from paddle.fluid.dygraph.nn import Conv2D, Pool2D, FC


# 定义vgg块，包含多层卷积和1层2x2的最大池化层
class vgg_block(fluid.dygraph.Layer):
    def __init__(self, name_scope, num_convs, num_channels):
        """
        num_convs, 卷积层的数目
        num_channels, 卷积层的输出通道数，在同一个Incepition块内，卷积层输出通道数是一样的
        """
        super(vgg_block, self).__init__(name_scope)
        self.conv_list = []
        for i in range(num_convs):
            conv_layer = self.add_sublayer('conv_' + str(i), Conv2D(self.full_name(),
                                                                    num_filters=num_channels, filter_size=3, padding=1,
                                                                    act='relu'))
            self.conv_list.append(conv_layer)
        self.pool = Pool2D(self.full_name(), pool_stride=2, pool_size=2, pool_type='max')

    def forward(self, x):
        for item in self.conv_list:
            x = item(x)
        return self.pool(x)


class VGG(fluid.dygraph.Layer):
    def __init__(self, name_scope, conv_arch=((2, 64),
                                              (2, 128), (3, 256), (3, 512), (3, 512))):
        super(VGG, self).__init__(name_scope)
        self.vgg_blocks = []
        iter_id = 0
        # 添加vgg_block
        # 这里一共5个vgg_block，每个block里面的卷积层数目和输出通道数由conv_arch指定
        for (num_convs, num_channels) in conv_arch:
            block = self.add_sublayer('block_' + str(iter_id),
                                      vgg_block(self.full_name(), num_convs, num_channels))
            self.vgg_blocks.append(block)
            iter_id += 1
        self.fc1 = FC(self.full_name(),
                      size=4096,
                      act='relu')
        self.drop1_ratio = 0.5
        self.fc2 = FC(self.full_name(),
                      size=4096,
                      act='relu')
        self.drop2_ratio = 0.5
        self.fc3 = FC(self.full_name(),
                      size=1,
                      )

    def forward(self, x):
        for item in self.vgg_blocks:
            x = item(x)
        x = fluid.layers.dropout(self.fc1(x), self.drop1_ratio)
        x = fluid.layers.dropout(self.fc2(x), self.drop2_ratio)
        x = self.fc3(x)
        return x
