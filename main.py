# coding=utf-8
from aimlCore import Kernel
import os
import codecs
from textrank4zh import TextRank4Keyword

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
    for words in tr4w.words_no_stop_words:
        key_words += ' '.join(words)
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

if __name__ == '__main__':
    talk()
