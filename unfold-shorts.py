# coding=utf-8
# 这个函数的作用：我们定义一种标签，存在于文件：file.aiml
# <category> <pattern> <fold><or>1</or><or>2</or></fold> </pattern> ... </category>
# 该文件经过此函数处理，生成文件：file-unfold.aiml
# 内容为
# <category> <pattern> 1 </pattern> ... </category>
# <category> <pattern> 2 </pattern> ... </category>

import os
from copy import deepcopy
# from xml.etree import ElementTree
from lxml import etree

# 目标文件夹
path = 'source'
# 目标文件
unfold_list = ['unfold-test.aiml']
os.chdir(path)


def read_tree(in_file):
    tree = etree.parse(in_file)
    return tree


def write_xml(tree, in_file):
    out_file = in_file[:-5] + '-unfold.aiml'
    tree.write(out_file, encoding='utf-8', xml_declaration=True)


# 将 or 展开到多个 fold
def unfold_or(fold):
    ors_num = len(fold.findall('or'))
    or_list = []
    for index, _or in enumerate(fold.findall('or')):
        or_list.append(_or.text)
    for _or in or_list:
        new_fold = etree.Element('fold')
        new_fold.text = _or
        fold.addnext(new_fold)


def unfold(_category):
    if _category.find('pattern') is None or _category.find('pattern').find('fold') is None:
        return False, None
    # 复制 category
    category_copy = deepcopy(_category)
    pattern = category_copy.find('pattern')
    fold = category_copy.find('pattern').find('fold')
    unfold_or(fold)
    pattern.remove(fold)
    return True, category_copy


tree = read_tree(unfold_list[0])
root = tree.getroot()
for category in root.iter('category'):
    is_unfolded, new_category = unfold(category)
    ever_unfolded = is_unfolded
    # while is_unfolded:
    #     is_unfolded, new_category = unfold(new_category)
    if ever_unfolded:
        root.remove(category)
        root.append(new_category)

write_xml(tree, unfold_list[0])
