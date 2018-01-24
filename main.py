# coding=utf-8
from aimlCore import Kernel
import os

alice = Kernel()
alice.learn('source/startup.xml')

# 此处需要切换目录
path = 'source'
os.chdir(path)

alice.respond('LOAD ALICE')

while 1:
    user_input = raw_input('输入>>')
    response = alice.respond(user_input)
    print response
