import json
import os
from xml.etree.ElementTree import Element, SubElement, tostring, ElementTree


def convert_json_to_xml(json_data, output_folder):
    # idx是索引 data是数据
    i = 0
    for data in enumerate(json_data):
        xmlname = os.path.splitext(data[1]['name'])[0]+'.xml'
        xml_path = os.path.join(output_folder, xmlname)
        print(data)
        if os.path.exists(xml_path):
            # 如果已经存在对应的xml文件，只需要添加object即可
            tree = ElementTree()
            tree.parse(xml_path)
            root = tree.getroot()

            # 创建新的 object 元素
            object_elem = SubElement(root, 'object')
            name = SubElement(object_elem, 'name')
            # name.text = str(data[1]['category'])
            name.text = str(data[1]['defect_name'])

            pose = SubElement(object_elem, 'pose')
            pose.text = 'Unspecified'

            truncated = SubElement(object_elem, 'truncated')
            truncated.text = '0'

            difficult = SubElement(object_elem, 'difficult')
            difficult.text = '0'

            # 采用+0.5的方式使其由向下取整变为四舍五入
            bndbox = SubElement(object_elem, 'bndbox')
            xmin = SubElement(bndbox, 'xmin')
            xmin.text = str(int(data[1]['bbox'][0] + 0.5))
            ymin = SubElement(bndbox, 'ymin')
            ymin.text = str(int(data[1]['bbox'][1] + 0.5))
            xmax = SubElement(bndbox, 'xmax')
            xmax.text = str(int(data[1]['bbox'][2] + 0.5))
            ymax = SubElement(bndbox, 'ymax')
            ymax.text = str(int(data[1]['bbox'][3] + 0.5))

            tree.write(xml_path)
        else:
            # 如果不存在对应的xml文件，需要创建根元素
            annotation = Element('annotation')

            # 添加元素到根元素
            folder = SubElement(annotation, 'folder')
            folder.text = 'temp'

            filename = SubElement(annotation, 'filename')
            filename.text = str(data[1]['name'])

            path = SubElement(annotation, 'path')
            path.text = str(data[1]['name'])

            source = SubElement(annotation, 'source')         # SubElement用于在 XML 元素中创建子元素
            database = SubElement(source, 'database')
            database.text = 'Unknown'

            size = SubElement(annotation, 'size')
            width = SubElement(size, 'width')
            # width.text = str(data[1]['image_width'])
            width.text = str(2446)
            height = SubElement(size, 'height')
            # height.text = str(data[1]['image_height'])
            height.text = str(1000)
            depth = SubElement(size, 'depth')
            depth.text = '3'

            segmented = SubElement(annotation, 'segmented')
            segmented.text = '0'

            object_elem = SubElement(annotation, 'object')
            name = SubElement(object_elem, 'name')
            # name.text = str(data[1]['category'])
            name.text = str(data[1]['defect_name'])

            pose = SubElement(object_elem, 'pose')
            pose.text = 'Unspecified'

            truncated = SubElement(object_elem, 'truncated')
            truncated.text = '0'

            difficult = SubElement(object_elem, 'difficult')
            difficult.text = '0'

            # 采用+0.5的方式使其由向下取整变为四舍五入
            bndbox = SubElement(object_elem, 'bndbox')
            xmin = SubElement(bndbox, 'xmin')
            xmin.text = str(int(data[1]['bbox'][0]+0.5))
            ymin = SubElement(bndbox, 'ymin')
            ymin.text = str(int(data[1]['bbox'][1]+0.5))
            xmax = SubElement(bndbox, 'xmax')
            xmax.text = str(int(data[1]['bbox'][2]+0.5))
            ymax = SubElement(bndbox, 'ymax')
            ymax.text = str(int(data[1]['bbox'][3]+0.5))

            # 创建XML文件
            xml_data = tostring(annotation)
            fname = str(os.path.splitext(os.path.basename(data[1]['name']))[0]) + '.xml'
            # print(fname)
            xml_file_path = os.path.join(output_folder, fname)   # -------------------str(data['name'])
            with open(xml_file_path, 'wb') as f:
                f.write(xml_data)


if __name__ == "__main__":
    # 将 'your_json_file.json' 替换为实际的JSON文件路径
    json_file_path = './anno.json'

    # 将 'output_folder' 替换为所需的输出文件夹路径
    output_folder = './butrain2xml'

    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    convert_json_to_xml(json_data, output_folder)

