'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: mztj
@file: tools.py
@time: 2019-1-11 8:24
@desc: 
'''

import time

def cur_datetime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))