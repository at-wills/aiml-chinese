# -*- coding: utf-8 -*-
import web
import os
import sys   
reload(sys)
sys.setdefaultencoding('utf-8')
from main import ask_api
import re
import time
flag = 0
urls = (
    '/(.+)', 'index',
    '/', 'search'
)

class search:

    def GET(self):
        print(os.getcwd())
        render = web.template.render('../templates/')
        return render.search()

class index:

    def GET(self, query):
        
        render = web.template.render('../templates/')
        anses = []
        answer = ask_api(query)
        anses.append({'answer':answer})

        return render.index(anses, query)

if __name__ == "__main__":
	app = web.application(urls,globals())
	app.run()

