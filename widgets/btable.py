'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 245838515@qq.com
@software: HMS
@file: btable.py
@time: 2019-1-7 17:03
@desc:
'''

from .bwidget import *


class TableView(QTableView):

    def __init__(self,parent=None):
        super(TableView,self).__init__(parent)