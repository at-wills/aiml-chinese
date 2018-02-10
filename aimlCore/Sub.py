#!coding:utf-8
import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

sub_dict = {}
regex = None


def init():
    global regex
    f = open('source/subs')
    for line in f:
        o, d = line.split(' ')
        sub_dict[o.decode('utf-8')] = d.decode('utf-8')
    f.close()
    regex = re.compile('(%s)' % '|'.join(map(re.escape, sub_dict.keys())))


def sub(text):
    global sub_dict
    global regex
    return regex.sub(lambda mo: sub_dict[mo.string[mo.start():mo.end()]], text)


if __name__ == '__main__':
    import os
    os.chdir('..')
    print os.getcwd()
    i = raw_input('test>>')
    print sub(i)
