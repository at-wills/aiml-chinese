# coding=utf-8
# 此程序用于进行分词测试
import main

last_dict = []


def read_dict():
    f = open('user-dict')
    for line in f:
        last_dict.append(line.split(' ')[0])
    f.close()


read_dict()
while 1:
    i = raw_input('测试输入（输入“reload”重载词典）>>')
    if i == 'reload':
        main.reload_user_dict(last_dict)
        read_dict()
    else:
        main.keywords(i)
