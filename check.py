import os
import shutil
import hashlib
from tqdm import tqdm
from tabulate import tabulate
import xml.etree.ElementTree as ET


# 读取.xml文件中的信息，输入参数为第一步读取的字典
# 取入参字典中的'xml'键，对应的路径列表，逐一读取。
# 返回keydict,键是类别名，值是对应的object数量
def count_xml(xml_list):
    print('Counting xml files objects...... ')
    labeldict = {}
    for xml_flie in tqdm(xml_list['xml']):
        tree = ET.parse(xml_flie)
        root = tree.getroot()
        for obj in root.findall("object"):
            # if obj.find('name').text not in labeldict.keys():
            if obj.find('name').text not in labeldict.keys():
                labeldict[obj.find('name').text] = 1
                # print(xml_flie)
            else:
                labeldict[obj.find('name').text] += 1
    keydict = dict(sorted(labeldict.items(), key=lambda x: x[1]))
    print("Finished！！！")
    print("%d classes and %d objects in total, Label Name and it's counts are:" % (len(keydict), sum(keydict.values())))
    table = {'class name': keydict.keys(), 'number': keydict.values()}
    print(tabulate(table, headers='keys', tablefmt='fancy_grid', showindex=True))
    # print(keydict)
    return keydict


# 检查.xml文件和.jpg文件是否对应
# path是异常文件的保存路径，file_groups是一个字典。键为后缀名，值为一个列表，存放对应的文件
def check_xml(path, file_groups):
    # 如果文件存在，先删了
    if os.path.exists(path):
        shutil.rmtree(path)

    print('Checking...... The abnormal files will be stored in:', path)
    xml_set = set()
    jpg_set = set()
    for xml in file_groups.get('xml'):
        xml_set.add(xml.split('.')[0])
    for jpg in file_groups.get('jpg'):
        jpg_set.add(jpg.split('.')[0])

    # 对比，如果非空，创建文件夹，移动文件
    diff_xml = xml_set - jpg_set  # xml多
    diff_jpg = jpg_set - xml_set
    while len(diff_xml) == 0 and len(diff_jpg) == 0:
        return print("xml与jpg文件完全对应，未进行任何操作！")

    if len(diff_xml) != 0:
        os.makedirs(path+'/xml')
        for xml in diff_xml:
            shutil.move(xml+'.xml', path+'/xml')
    if len(diff_jpg) != 0:          # 注意不能用elif
        os.makedirs(path + '/jpg')
        for jpg in diff_jpg:
            shutil.move(jpg + '.jpg', path + '/jpg')
    return print('共移动', len(diff_xml)+len(diff_jpg), '个文件')


def xml_clean(path, save_path):
    num = 0
    os.makedirs(save_path)
    for xml in os.listdir(path):
        if xml.endswith('.xml'):
            xml_file = os.path.join(path, xml)
            tree = ET.parse(xml_file)
            root = tree.getroot()

            if len(root.findall('object')) == 0:
                # os.makedirs(save_path)
                # os.remove(xml_file)
                # os.remove(xml_file[:-3] + "jpg")
                shutil.move(xml_file, save_path)
                num += 1
                shutil.move(xml_file[:-3] + 'jpg', save_path)
                num += 1
                print(f"Deleted {xml_file}")

    return print('Remove xml and images to', save_path, 'total are:', num)


def mv_dup(imgpath, save_path):
    # 创建一个字典，用于存储文件内容的哈希值和文件路径
    hash_dict = {}
    num = 0      # 重复的图像
    for root, _, files in os.walk(imgpath):
        for file in tqdm(files):
            # print(file)
            if file.endswith(".jpg"):
                file_path = os.path.join(root, file)
                # print(file_path)

                # 计算文件的哈希值
                with open(file_path, "rb") as f:
                    file_content = f.read()
                    file_hash = hashlib.md5(file_content).hexdigest()

                # 检查是否有相同哈希值的文件
                if file_hash in hash_dict:
                    print(f"Duplicate files: {file_path} and {hash_dict[file_hash]}")
                    shutil.move(file_path, save_path)
                    shutil.move(file_path[:-3] + 'xml', save_path)
                    print("save_path", save_path)
                    num += 1
                else:
                    # 将哈希值和文件路径添加到字典
                    hash_dict[file_hash] = file_path
    return print('Remove duplicatel images and its xml to', save_path, 'images total are:', num)
