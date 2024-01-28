# 文档说明

对使用labelimg标注好的xml文件进行处理：

* xml_main.py 调用
   * check.py
   * converter.py
*  xml_replace_label.py    重命名指定类别
*  remove_class.py          移除指定类，可搭配功能4使用
*  json2xml.py         新增功能，将.json格式的标签文件转换为多个xml文件

**部分功能需要**：.xml与.jpg文件在同一个文件夹内



> 功能1：统计文件夹内的文件数量，读取xml文件中的类别和各个样本的个数。
> ```python
> python xml_main.py your/files/path
> ```


> 功能2：检查文件夹内xml文件和对应的图片名称是否对应，将不对应的文件移出至"./path/save/abnormal"
> ```python
> python xml_main.py your/files/path --check_xml ./path/save/abnormal
> ```


>功能3：将文件夹中的PNG png JPG JPEG jpeg统一换为jpg格式   
>
>```python
>python xml_main.py your/files/path --jpg=True
>```


>功能4：将没有物体标注信息的xml文件及对应图片剪切掉
>
>```python
>python xml_main.py your/files/path  --clean  ./path/save
>```


>功能5：检查文件夹内的重复图片
>
>```python
>python xml_main.py your/files/path  --duplicate  ./path/save
>```


>功能6：将xml文件转化为标准的voc格式训练集，手动输入训练集比率（默认test=val）
>默认生成在./voc2012/路径下
>
>```python
>python xml_main.py your/files/path --xml2voc=0.7
>```


>功能7：将功能6生成的voc格式数据集转化为yolo格式数据集（注意需要一个空路径！）
>```python
> python xml_main.py your/files/path --voc2yolo ./path/save/yolo
> ```


>功能8：将功能6生成的voc格式数据集转化为coco格式数据集（注意需要一个空路径！）
>```python
> python xml_main.py your/files/path --voc2coco ./path/save/coco
>```





