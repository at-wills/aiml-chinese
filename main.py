# coding=utf-8
from aimlCore import Kernel
import os
import jieba
from textrank4zh import TextRank4Keyword
# 在此处引入，用于直接生成 unfold 文件
import unfold_shorts

jieba.load_userdict('source/user-dict')
alice = Kernel()
alice.learn('source/startup.xml')

# 此处需要切换目录
path = 'source'
os.chdir(path)

alice.respond('LOAD ALICE')

tr4w = TextRank4Keyword()


def keywords(sentence):
    tr4w.analyze(text=sentence, lower=True, window=2)
    key_words = ''
    for words in tr4w.words_no_filter:
        i = 0
        while i < len(words):
            # 如果你需要替换
            if words[i] == '不是':
                words[i] = '不'
            # 如果你需要删除
            if words[i] == '很' or words[i] == '非常':
                del words[i]
                i -= 1
            i += 1
        key_words += ' '.join(words)
    # print colored('关键词提取结果：', 'blue'), colored(key_words, 'blue')
    print '关键词提取结果：', key_words
    return key_words


def ask_api(input_words):
    input_words = keywords(input_words)
    response = alice.respond(input_words)
    return response


def talk():
    while 1:
        user_input = raw_input('输入>>')
        user_input = keywords(user_input)
        response = alice.respond(user_input)
        print response


# only called by split-test.py
def reload_user_dict(last_dict):
    for i in last_dict:
        jieba.del_word(i)
    jieba.load_userdict('user-dict')


if __name__ == '__main__':
    talk()
