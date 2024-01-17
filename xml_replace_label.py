import os.path
import xml.dom.minidom

# path为需要替换标签的目标文件夹
path = r'I:\比赛\1031原始数据\样本库下载异物、鸟巢\异物\JPEGImages'
old_label = '666_jkxl_gt_bt_tdsh'  # 被替换标签
new_label = '010101071'   # 新标签


files = os.listdir(path)  # 得到文件夹下所有文件名称
print('------------开始替换标签名称！--------------')
for xmlFile in files:  # 遍历原标签文件夹
    if xmlFile.split('.')[-1] != 'xml':  # 如果不是
        continue
    if not os.path.isdir(xmlFile):  # 判断是否是文件夹，不是文件夹才打开
        dom = xml.dom.minidom.parse(os.path.join(path, xmlFile))
        root = dom.documentElement
        # 替换节点，除了name也可以替换为其他节点
        pathNode = root.getElementsByTagName('name')
        print(pathNode)
        print(len(pathNode))
        j = len(pathNode)
        for i in range(j):
            if pathNode[i].firstChild.data == old_label:
                print("替换前的名称为：", pathNode[i].firstChild.data)
                pathNode[i].firstChild.data = new_label
                print("i为:", i)
                print("替换后的名称为：", pathNode[i].firstChild.data)
                i = i + 1
                with open(os.path.join(path, xmlFile), 'w', encoding='utf8') as fh:
                    dom.writexml(fh)

print('------------标签名称替换成功！--------------')
