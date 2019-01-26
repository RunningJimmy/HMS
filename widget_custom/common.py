'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: common.py
@time: 2019-1-25 12:57
@version：0.1
@desc: 
'''
from widget_base import *
import os,sys

# 资源文件位置
def root_dir(name):
    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    return "%s%s" %(dirname,name)

def icon_dir(name):
    return os.path.join(root_dir(r"\resource\image"),name)

def sheetstyle_dir(name):
    return os.path.join(root_dir(r"\resource\style"),name)

def tmp_dir(name):
    return os.path.join(root_dir(r"\tmp"), name)

class Icon(QIcon):

    def __init__(self,name):
        super(Icon,self).__init__()
        self.addPixmap(QPixmap(icon_dir(name)),QIcon.Normal,QIcon.On)

class GroupBox(QGroupBox):

    def __init__(self,*__args):
        super(GroupBox,self).__init__(*__args)
        self.setFlat(True)
        self.setFont(QFont("宋体",10))

class HBoxLayout(QHBoxLayout):

    def __init__(self,parent=None):
        super(HBoxLayout,self).__init__(parent)
        self.setContentsMargins(0,10,0,0)

class VBoxLayout(QVBoxLayout):
    def __init__(self, parent=None):
        super(VBoxLayout, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)