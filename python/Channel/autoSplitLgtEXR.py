import nuke
import string
import random


def generate_random_str(length=6):
    """
    生成随机字符串
    :param length:
    :return:
    """
    chars = string.ascii_letters + string.digits  # 包含大小写字母和数字
    return ''.join(random.choices(chars, k=length))


def is_read_node():
    """函数1：判断选中的节点是否为Read节点"""
    selected_nodes = nuke.selectedNodes()

    # 检查是否选中了节点
    if len(selected_nodes) == 0:
        raise ValueError("错误：未选中任何节点！")

    # 检查选中的节点是否为Read节点
    read_node = selected_nodes[0]
    if read_node.Class() != "Read":
        raise ValueError("错误：选中的节点不是Read节点！")

    # 获取该节点下游连接的所有节点
    downstream_nodes = read_node.dependent()

    if len(downstream_nodes) > 0:
        raise ValueError("错误：下游已存在节点！")

    return read_node


def get_rgba_channels(read_node):
    """函数2：获取选中Read节点的所有RGBA_前缀通道信息"""
    # 获取节点的所有通道
    channels = read_node.channels()
    lgt_channels = []

    # 找出所有以RGBA_开头的通道
    for channel in channels:
        # 通道格式为"layer.channel"，我们只关心层名
        parts = channel.split('.')
        if len(parts) == 2:
            layer_name = parts[0]
            if layer_name.startswith('RGBA_') and layer_name not in lgt_channels:
                lgt_channels.append(layer_name)

    # 按通道名排序以确保一致性
    lgt_channels.sort()

    return lgt_channels


def create_dots_layout(read_node, lgt_channels):
    """函数3：创建Dot节点布局"""
    lgt_channels_num = len(lgt_channels) - 1

    # 获取Read节点的位置
    read_x = read_node.xpos()
    read_y = read_node.ypos()
    read_width = read_node.screenWidth()

    # 计算中心Dot节点的位置（Read节点下方200像素，x轴居中）
    center_dot_x = read_x + (read_width / 2) - 5  # Dot节点宽度约为10，居中调整
    center_dot_y = read_y + 200

    # 创建中心Dot节点
    center_dot = nuke.nodes.Dot()
    center_dot.setXYpos(int(center_dot_x), int(center_dot_y))

    # 连接中心Dot到Read节点
    center_dot.setInput(0, read_node)

    dots_list = []

    # 创建左侧Dot节点链
    left_dots = []
    for i in range(lgt_channels_num):
        dot_x = center_dot_x - (lgt_channels_num - i) * 300  # 从左边最远开始
        dot_y = center_dot_y

        dot = nuke.nodes.Dot()
        dot.setXYpos(int(dot_x), int(dot_y))
        left_dots.append(dot)

    # 连接左侧Dot节点链（从左到右连接）
    for i in range(len(left_dots)):
        if i == 0:
            # 第一个节点连接到中心Dot
            left_dots[i].setInput(0, center_dot)
        else:
            # 后续节点连接前一个左侧节点
            left_dots[i].setInput(0, left_dots[i - 1])

    # 创建右侧Dot节点链（2个节点）
    right_dots = []
    for i in range(2):
        dot_x = center_dot_x + (i + 1) * 300  # 从中心向右
        dot_y = center_dot_y

        dot = nuke.nodes.Dot()
        dot.setXYpos(int(dot_x), int(dot_y))
        right_dots.append(dot)

    # 连接右侧Dot节点链（从右到左连接）
    for i in range(len(right_dots)):
        if i == 0:
            # 第一个右侧节点连接到中心Dot
            right_dots[i].setInput(0, center_dot)
        else:
            # 后续节点连接前一个右侧节点
            right_dots[i].setInput(0, right_dots[i - 1])

    # 构建完整的dots_list（从左到右顺序）
    dots_list.extend(left_dots)  # 左侧节点
    dots_list.append(center_dot)  # 中心节点
    dots_list.extend(right_dots)  # 右侧节点

    return dots_list


def create_shuffle_nodes(dots_list, lgt_channels):
    """函数4：基于Dot节点创建Shuffle节点"""
    lgt_channels_num = len(lgt_channels)
    shuffle_nodes = []

    # 处理左侧的Shuffle节点（对应RGBA通道）
    random_str = generate_random_str()
    for i in range(lgt_channels_num):
        dot_node = dots_list[i]
        channel_name = lgt_channels[i]

        # 计算Shuffle节点位置
        shuffle_x = dot_node.xpos() - 34  # xpos减少34
        shuffle_y = dot_node.ypos() + 200  # 下方200像素

        # 创建Shuffle节点
        shuffle_node = nuke.nodes.Shuffle()
        shuffle_node.setXYpos(int(shuffle_x), int(shuffle_y))
        shuffle_node.setInput(0, dot_node)

        # 设置Shuffle节点属性
        shuffle_node['in'].setValue(channel_name)
        shuffle_node['postage_stamp'].setValue(True)

        shuffle_node['name'].setValue(channel_name + '_' + random_str)

        # 设置RGBA映射
        shuffle_node['red'].setValue('red')
        shuffle_node['green'].setValue('green')
        shuffle_node['blue'].setValue('blue')
        shuffle_node['alpha'].setValue('alpha')

        shuffle_nodes.append(shuffle_node)

    # 创建Remove节点（右侧第一个Dot）
    remove_dot = dots_list[lgt_channels_num]  # 右侧第一个Dot

    remove_x = remove_dot.xpos() - 34
    remove_y = remove_dot.ypos() + 200

    remove_node = nuke.nodes.Remove()
    remove_node.setXYpos(int(remove_x), int(remove_y))
    remove_node.setInput(0, remove_dot)

    remove_node['operation'].setValue('remove')
    remove_node['channels'].setValue('rgb')
    remove_node['postage_stamp'].setValue(True)
    remove_node['name'].setValue('remove_rgb_' + random_str)

    shuffle_nodes.append(remove_node)

    # 创建Depth Shuffle节点（右侧第二个Dot）
    depth_dot = dots_list[lgt_channels_num + 1]  # 右侧第二个Dot

    depth_x = depth_dot.xpos() - 34
    depth_y = depth_dot.ypos() + 200

    depth_shuffle = nuke.nodes.Shuffle()
    depth_shuffle.setXYpos(int(depth_x), int(depth_y))
    depth_shuffle.setInput(0, depth_dot)

    depth_shuffle['in'].setValue('depth')
    depth_shuffle['postage_stamp'].setValue(True)
    depth_shuffle['name'].setValue('Z_depth_' + random_str)

    # 设置深度通道映射（Z到RGBA）
    depth_shuffle['red'].setValue('Z')
    depth_shuffle['green'].setValue('Z')
    depth_shuffle['blue'].setValue('Z')
    depth_shuffle['alpha'].setValue('Z')

    shuffle_nodes.append(depth_shuffle)

    return shuffle_nodes


def create_merge_network(shuffle_nodes, lgt_channels):
    """函数5：创建合并节点网络"""
    lgt_channels_num = len(lgt_channels)

    # 1. 创建左侧合并网络（RGBA通道合并）
    if lgt_channels_num > 0:
        # 2.1 第一个Shuffle节点下方的Dot节点
        first_shuffle = shuffle_nodes[0]
        s_dot_left_x = first_shuffle.xpos() + 34
        s_dot_left_y = first_shuffle.ypos() + 600

        s_dot_left = nuke.nodes.Dot()
        s_dot_left.setXYpos(int(s_dot_left_x), int(s_dot_left_y))
        s_dot_left.setInput(0, first_shuffle)

        # 2.2 如果有多个RGBA通道，创建Merge节点链
        if lgt_channels_num >= 2:
            current_merge = None

            for i in range(1, lgt_channels_num + 1):
                shuffle_node = shuffle_nodes[i]
                merge_x = shuffle_node.xpos()
                merge_y = shuffle_node.ypos() + 600

                merge_node = nuke.nodes.Merge2()
                merge_node.setXYpos(int(merge_x), int(merge_y))
                merge_node.setInput(0, shuffle_node)  # A输入

                # 设置Merge属性
                merge_node['operation'].setValue('plus')
                merge_node['A'].setValue('rgb')  # 去掉alpha通道
                merge_node['name'].setValue('merge_plus_{}'.format(i))

                if i == 1:
                    # 第一个Merge节点的B输入连接到s_dot_left
                    merge_node.setInput(1, s_dot_left)
                else:
                    # 后续Merge节点的B输入连接到前一个Merge节点
                    merge_node.setInput(1, current_merge)

                current_merge = merge_node

            # 保存最终的Merge节点
            s_merge_final = current_merge if lgt_channels_num > 1 else s_dot_left
        else:
            s_merge_final = s_dot_left

    # 3. 创建ColorCorrect节点（连接Remove节点）
    remove_node = shuffle_nodes[lgt_channels_num]  # Remove节点
    cc_x = s_merge_final.xpos()
    cc_y = s_merge_final.ypos() + 200

    s_cc_left1 = nuke.nodes.ColorCorrect()
    s_cc_left1.setXYpos(int(cc_x), int(cc_y))
    s_cc_left1.setInput(0, s_merge_final)
    s_cc_left1['name'].setValue('color_correct_remove')

    # 4. 创建Grade节点（连接Depth Shuffle节点）
    depth_node = shuffle_nodes[lgt_channels_num + 1]  # Depth Shuffle节点
    grade_x = depth_node.xpos()
    grade_y = depth_node.ypos() + 600

    s_grade_left1 = nuke.nodes.Grade()
    s_grade_left1.setXYpos(int(grade_x), int(grade_y))
    s_grade_left1.setInput(0, depth_node)

    # 设置Grade参数
    s_grade_left1['white'].setValue(0.005)
    s_grade_left1['multiply'].setValue(0.1)
    s_grade_left1['name'].setValue('grade_depth')

    # 5. 创建Dot节点（Grade节点下方）
    grade_dot_x = s_grade_left1.xpos() + 34
    grade_dot_y = s_grade_left1.ypos() + 400

    s_dot_left1 = nuke.nodes.Dot()
    s_dot_left1.setXYpos(int(grade_dot_x), int(grade_dot_y))
    s_dot_left1.setInput(0, s_grade_left1)

    # 6. 创建Copy节点
    copy_x = s_cc_left1.xpos()
    copy_y = s_cc_left1.ypos() + 200

    s_copy_left1 = nuke.nodes.Copy()
    s_copy_left1.setXYpos(int(copy_x), int(copy_y))
    s_copy_left1.setInput(1, s_dot_left1)  # A输入（深度数据）
    s_copy_left1.setInput(0, s_cc_left1)  # B输入（颜色数据）

    # 设置Copy通道映射：rgba.red -> depth.Z
    s_copy_left1['from0'].setValue('rgba.red')
    s_copy_left1['to0'].setValue('depth.Z')
    s_copy_left1['name'].setValue('copy_depth_data')

    # 7. 创建最终的Dot节点
    final_dot_x = s_copy_left1.xpos() + 34
    final_dot_y = s_copy_left1.ypos() + 400

    final_dot = nuke.nodes.Dot()
    final_dot.setXYpos(int(final_dot_x), int(final_dot_y))
    final_dot.setInput(0, s_copy_left1)


def main():
    try:
        # 函数1：检查选中的节点是否为Read节点
        read_node = is_read_node()

        # 函数2：获取RGBA通道信息
        lgt_channels = get_rgba_channels(read_node)
        print("找到{}个RGBA通道: {}".format(len(lgt_channels), lgt_channels))

        # 函数3：创建Dot节点布局
        dots_list = create_dots_layout(read_node, lgt_channels)
        print("创建了{}个Dot节点".format(len(dots_list)))

        # 函数4：创建Shuffle节点
        shuffle_nodes = create_shuffle_nodes(dots_list, lgt_channels)

        # 函数5：创建合并网络
        create_merge_network(shuffle_nodes, lgt_channels)
        print("节点网络生成完成！")

    except Exception as e:
        nuke.message("执行过程中出现错误: {}".format(str(e)))
