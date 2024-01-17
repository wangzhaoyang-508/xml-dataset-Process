import xml.etree.ElementTree as ET
from tqdm import tqdm
import os


def remove_object_by_name(xml_file, target_name):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    remove = 0
    objects_to_remove = []

    for obj in root.findall('object'):
        name_element = obj.find('name')
        if name_element is not None and name_element.text == target_name:
            objects_to_remove.append(obj)

    for obj in objects_to_remove:
        root.remove(obj)
        remove = remove+1        # 记录一个删了多少个

    tree.write(xml_file)
    return remove


xml_file_path = r'I:\比赛\比赛训练数据总11月15日王朝阳整理\Annotations'  # 替换为实际的 XML 文件路径
target_name = '050101041'  # 替换为要删除的目标名称

remove_num = 0
for xml in tqdm(os.listdir(xml_file_path)):
    if xml.endswith('.xml'):
        # print(xml)
        remove_num = remove_num + remove_object_by_name(xml_file_path + '/' + xml, target_name)
    else:
        continue
print('完成，共删除', remove_num, '个', target_name)
