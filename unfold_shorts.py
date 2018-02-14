# coding=utf-8
# 这个函数的作用：我们定义一种标签，存在于文件：file.aiml
# <category> <pattern> <fold><or>1</or><or>2</or></fold> </pattern> ... </category>
# 该文件经过此函数处理，生成文件：file-unfold.aiml
# 内容为
# <category> <pattern> 1 </pattern> ... </category>
# <category> <pattern> 2 </pattern> ... </category>

import os
from copy import deepcopy
from lxml import etree
import itertools

# 目标文件
unfold_list = ['source/emotion.aiml', 'source/sport.aiml']


def read_tree(in_file):
    _tree = etree.parse(in_file)
    return _tree


def write_xml(_tree, in_file):
    out_file = in_file[:-5] + '-unfold.aiml'
    _tree.write(out_file, encoding='utf-8', xml_declaration=True)


class Patter:
    # things： 'str' foldNode 'str' foldNode 'str'
    def __init__(self, pattern):
        self.things = []
        if pattern.find('fold') is None:
            if pattern.find('or') is not None:
                print 'wrong syntax'
                return
            self.things.append(pattern.text)
        else:
            folds = pattern.findall('fold')
            folds_num = len(folds)
            for i in xrange(folds_num):
                fold = folds[i]
                if i == 0:
                    pattern_text = fold.xpath('preceding-sibling::text()')
                    if len(pattern_text) != 0:
                        pattern_text = pattern_text[0].encode('utf-8').decode('utf-8')
                else:
                    pattern_text = fold.xpath('//text()[count(preceding-sibling::fold)=$count]', count=i)
                    if len(pattern_text) != 0:
                        pattern_text = pattern_text[0].encode('utf-8').decode('utf-8')
                if len(pattern_text) != 0:
                    self.things.append(pattern_text)
                self.things.append(fold)
                if i == folds_num - 1:
                    last_pattern_text = fold.xpath('following-sibling::text()')
                    if len(last_pattern_text) != 0:
                        last_pattern_text = last_pattern_text[0].encode('utf-8').decode('utf-8')
                        self.things.append(last_pattern_text)

    # return a list containing all or.text
    @staticmethod
    def unfold_or(self, fold):
        allowed_chars = set(' ' + '\n')
        if fold.text is not None:
            if set(fold.text) > allowed_chars:
                # 其实能做，不过…… (｀・ω・´)
                print 'error: not support fold tag with text!'
        or_list = []
        for _or in fold.findall('or'):
            or_list.append(_or.text)
        return or_list

    # return a list containing all unfolded patterns in only str
    def get_str_patterns(self):
        str_patterns = []
        l = len(self.things)
        for i in xrange(l):
            item = self.things[i]
            if type(item) is unicode:
                self.things[i] = [item]
            else:
                self.things[i] = self.unfold_or(self, item)
        for i in itertools.product(*self.things, repeat=1):
            str_patterns.append(' '.join(i))
        return str_patterns


def unfold_category(_category):
    if _category.find('pattern') is None or _category.find('pattern').find('fold') is None:
        return False, None
    pattern = _category.find('pattern')
    str_patterns = Patter(pattern).get_str_patterns()
    categories = []
    for str_pattern in str_patterns:
        category_copy = deepcopy(_category)
        new_pattern = etree.Element('pattern')
        new_pattern.text = str_pattern
        pattern = category_copy.find('pattern')
        pattern.addnext(new_pattern)
        category_copy.remove(pattern)
        categories.append(category_copy)
    return True, categories


tree = read_tree(unfold_list[0])
root = tree.getroot()
for category in root.iter('category'):
    is_unfolded, new_categories = unfold_category(category)
    if is_unfolded:
        root.remove(category)
        for new_category in new_categories:
            root.append(new_category)

write_xml(tree, unfold_list[0])
print 'done'
