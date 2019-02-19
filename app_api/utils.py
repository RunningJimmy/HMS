'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: utils.py
@time: 2019-2-12 9:03
@version：0.1
@desc: 工具箱
'''

import time

def cur_datetime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))