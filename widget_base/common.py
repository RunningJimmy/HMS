'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: ui.py
@time: 2019-1-23 14:04
@version：0.1
@desc: 公共基础组件，即框架自带的
'''

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import winreg
import os
import time

# 获取桌面地址
def desktop(filename=None):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',)
    path = winreg.QueryValueEx(key, "Desktop")[0]
    if filename:
        return os.path.join(path,filename)
    else:
        return path

def cur_datetime():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(time.time())))

def cur_date():
    return time.strftime("%Y-%m-%d", time.localtime(int(time.time())))

def cur_time():
    return time.strftime("%H:%M:%S", time.localtime(int(time.time())))

def cur_timestamp():
    return time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime(int(time.time())))