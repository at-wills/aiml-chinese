# coding=utf-8
import jieba
import re


# 去除中文标点符号
def deal_punctuation(text):
    s = re.sub('[·！￥……（）——【】、“”‘’；：《》，。？〈〉～]+'.decode("utf-8"), ' '.decode('utf-8'),
               text.decode('utf-8'))
    return s


# 载入自定义词典
jieba.load_userdict('cutSentence/user-dict/dict.txt')


# todo 现在只有分词，需要进行分句
def cut_sentence(input_sentence):
    input_sentence = deal_punctuation(input_sentence)
    cut_list = jieba.cut(input_sentence)
    return ' '.join(cut_list)
