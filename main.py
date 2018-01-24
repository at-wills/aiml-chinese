# coding=utf-8
from aimlCore import Kernel
from cutSentence import cutter
import os

alice = Kernel()
alice.learn('source/startup.xml')

# 此处需要切换目录
path = 'source'
os.chdir(path)

alice.respond('LOAD ALICE')


def ask_api(input_words):
    input_words = cutter.cut_sentence(input_words).encode('utf-8')
    response = alice.respond(input_words)
    return response


def talk():
    while 1:
        user_input = raw_input('输入>>')
        user_input = cutter.cut_sentence(user_input).encode('utf-8')
        response = alice.respond(user_input)
        print response

talk()
