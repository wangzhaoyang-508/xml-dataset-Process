import os
import argparse
from converter import xml2voc, voc2yolo, voc2coco, convert2jpg
from check import count_xml, check_xml, xml_clean, mv_dup


def parse_args():
    parser = argparse.ArgumentParser(description='oooooo')
    # 功能1 统计文件夹内的文件数量
    parser.add_argument('path', help='dataset file path')
    # 功能2.检查xml文件和对应的图片名称是否一一对应
    parser.add_argument('--check_xml', help='need save path, Check .xml&.img correspondence, Save abnormal', type=str)
    # 功能3.统一转化.png为.jpg格式
    parser.add_argument('--jpg', help='2 jpg', type=bool)
    # 功能4.检查文件夹内是否存在没有物体标注信息的xml文件及对应图片
    parser.add_argument('--clean', help='need a save path, to save and check removed .xml and .jpg', type=str)
    # 功能5.检查文件夹内是否包含名字不同的重复图片
    parser.add_argument('--duplicate', help='rm img which duplicate', type=str)

    # 功能6.将标注好的xml文件转化为标准的voc格式训练集
    parser.add_argument('--xml2voc', help='need a train_ratio float, build standard VOC2012 datasets', type=float)
    # 功能7.将xml文件（即voc格式数据集）转化为txt文件（即yolo格式数据集）
    parser.add_argument('--voc2yolo', help='need a save path, convert .xml to .txt', type=str)
    # 功能8.将xml文件（即voc格式数据集）转化为json文件（即COCO格式数据集）
    parser.add_argument('--voc2coco', help='need a save path, convert .xml to .json', type=str)

    args = parser.parse_args()
    # print(args)
    return args


# 读取此文件夹中的全部文件，并按后缀分组。
# 返回分组，分组是一个字典，键为后缀，值为路径列表。
def group_files_by_extension(folder_path):
    file_count = 0  # 文件夹中子文件数量
    # 创建一个字典，键为后缀名，值为一个列表，存放对应的文件。
    file_groups = {}
    # 遍历文件夹中的文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_count += 1  # 文件总数+1
            # 获取文件的后缀
            _, extension = os.path.splitext(file)

            # 如果存在后缀
            if extension:
                extension = extension[1:]  # 去除后缀中的点号
                file_path = os.path.join(root, file)
                if extension not in file_groups:
                    file_groups[extension] = []
                file_groups[extension].append(file_path)
    print("文件数量:", file_count)
    print("后缀数量:")
    for extension, count in file_groups.items():
        # print(f".{extension}: {count}")
        print(f".{extension}: {len(count)}")
    return file_groups


def main():
    args = parse_args()
    path = args.path       # 加载数据集文件夹路径
    # path = r"F:\河北工大\苏斌义王世杰赵参参联合数据集\voc2012\JPEGImages"

    file_groups = group_files_by_extension(path)   # 按文件名分组
    # count_xml(file_groups)  # 统计所有xml文件中，目标的类别和个数。

    # 功能1 统计文件夹内的文件数量(默认功能）
    classes = list(count_xml(file_groups).keys())  # 类名列表
    # print(classes)

    # 功能2.检查xml文件和对应的图片名称是否一一对应
    if args.check_xml:
        abnormal_path = args.check_xml
        check_xml(abnormal_path, file_groups)

    # 功能3.将图像统一转化.jpg格式, p为图片路径
    if args.jpg:
        convert2jpg(path)

    # 功能4.检查文件夹内是否存在没有物体标注信息的xml文件及对应图片
    if args.clean:
        save_path = args.clean
        xml_clean(path, save_path)

    # 功能5.检查文件夹内是否包含名字不同的重复图片，将重复的图片及对应xml文件移除到指定路径
    if args.duplicate:
        duplicate_path = args.duplicate
        mv_dup(path, duplicate_path)

    # 功能6.将标注好的xml文件转化为标准的voc格式训练集, 标准化VOC2012数据集(val=test)
    if args.xml2voc:
        train_ratio = args.xml2voc
        xml2voc(file_groups, train_ratio)

    # 功能7.将xml文件（即voc格式数据集）转化为txt文件（即yolo格式数据集）
    if args.voc2yolo:
        save_path = args.voc2yolo
        voc2yolo(save_path, classes)

    # 功能8.将xml文件（即voc格式数据集）转化为json文件（即COCO格式数据集）
    if args.voc2coco:
        save_path = args.voc2coco
        voc2coco(save_path, classes)


if __name__ == '__main__':
    main()
