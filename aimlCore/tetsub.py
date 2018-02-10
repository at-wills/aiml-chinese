import Sub
import os

os.chdir('..')
Sub.init()
print Sub.sub(raw_input('>>').decode('utf-8'))
