'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: table.py
@time: 2019-1-23 14:02
@version：0.1
@desc: 标准表格和定制表格
'''
from .common import *

class TableWidget(QTableWidget):

    def __init__(self,heads:dict,parent=None):
        super(TableWidget,self).__init__(parent)
        self.initDefaultConfig()

        self.setColumnCount(len(heads))                    # 添加行头 必须先设置 setColumnCount
        self.setHorizontalHeaderLabels(heads.values())
        self.heads = heads

    # 默认配置
    def initDefaultConfig(self):
        self.setShowGrid(True)
        self.setSortingEnabled(True)                                # 字符串排序功能
        self.setFrameShape(QFrame.NoFrame)                          # 设置无边框
        self.verticalHeader().setVisible(False)                     # 列表头
        # self.setFocusPolicy(Qt.NoFocus) #取消选中单元格时的虚线框
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)      # 表格内容不能编辑
        self.setSelectionBehavior(QAbstractItemView.SelectRows)     # 选中一行
        self.setAlternatingRowColors(True)                          # 使用行交替颜色
        self.setStyleSheet("QTableCornerButton::section{background-color:white;}")
        self.keys = None
        # 鼠标跟踪功能
        # self.setMouseTracking(True)
        # self.cellEntered.connect(self.MouseTrackItem)

    # 公共实现，载入数据
    def load(self,datas:list,heads=None):
        # 查询前，关闭排序，避免显示空白，BUG
        self.setSortingEnabled(False)
        if not heads:
            heads = self.heads
            # 保留原来的行，清空内容
            self.clearContents()
        else:
            self.heads = heads
            # 连行头一起清空
            self.clear()
        self.setRowCount(0)  # 清空行
        self.setColumnCount(len(heads))
        self.setHorizontalHeaderLabels(heads.values())  # 行表头

        # 具体实现逻辑
        self.load_set(datas,heads)
        # 恢复公共设置
        self.setSortingEnabled(True)  # 查询后设置True，开启排序

    # 子控件 继承具体实现
    def load_set(self,datas,head):
        pass

    # 选择了哪些行
    def selectRows(self):
        '''
        :return: list
        '''
        return list(set([item.row() for item in self.selectedItems()]))

    # 获取选中行的某列值
    def selectRowsValue(self,key):
        '''
        :param key: 关键字
        :return: list
        '''
        return [self.getItemValueOfKey(row,key) for row in self.selectRows()]

    # 获取已选择行的关键字的值
    def selectRowsValueOfInt(self,key):
        tmp = []
        for row in self.selectRows():
            value = self.getItemValueOfKey(row,key)
            if value.isdigit():
                tmp.append(int(value))
        return tmp

    # 获取单行的字典 {col:value,......,colx:valuex,.....}
    def curSelectRow2Dict(self,*args):
        return self.selectRow2Dict(self.currentRow(),args)

    # 获取某行的 整行值
    def selectRow2Dict(self,row:int, *args):
        '''
        :param row: 行
        :param args:
        :return: dict
        '''
        if self.keys:
            keys = self.keys
        elif args:
            keys = args
        else:
            keys = self.heads.keys()

        return dict([(key, self.itemValueOfKey(row,key)) for key in keys])

    #获取某行某列值
    def itemValue(self,row:int,col:int):
        return self.item(row,col).text()

    #获取当前行某列值
    def curItemValue(self,col:int):
        return self.item(self.currentRow(),col).text()

    # 根据key获取某行某列的值
    def itemValueOfKey(self,row:int,key:str):
        return self.itemValue(row,list(self.heads.keys()).index(key))

    # 根据key获取当前行某列的值
    def curItemValueOfKey(self,key:str):
        return self.itemValue(self.currentRow(),list(self.heads.keys()).index(key))

    # 获取某行最后一列值
    def lastItemValue(self,row:int):
        return self.itemValue(row,len(self.heads)-1)

    # 获取某行最后一列值
    def curLastItemValue(self):
        return self.itemValue(self.currentRow(),len(self.heads)-1)

    def lastCol(self):
        return len(self.heads)-1

    # 根据key 获取某行列的值
    def setItemValueOfKey(self,row:int,key:str,value:str,color=None):
        col = list(self.heads.keys()).index(key)
        self.item(row, col).setText(value)
        if isinstance(color,QColor):
            self.item(row, col).setBackground(color)

    # 根据key 获取当前行列的值
    def setCurItemValueOfKey(self,key:str,value:str,color=None):
        col = list(self.heads.keys()).index(key)
        self.item(self.currentRow(),col).setText(value)
        if isinstance(color,QColor):
            self.item(self.currentRow(), col).setBackground(color)

    # 设置某列宽
    def setColWidth(self, key, p_int:None):
        if key in self.heads.keys():
            col = list(self.heads.keys()).index(key)
            if p_int==None:
                # 自适应
                self.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeToContents)
                # self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch) #第二列扩展
            else:
                # 固定宽度
                self.setColumnWidth(col,p_int)

    # 设置多列宽
    def setColsWidth(self,widths:dict):
        if widths:
            for key,value in widths.items():
                self.setColWidth(key,value)
        else:
            # 设置列适应大小
            self.resizeColumnsToContents()

        def setKeys(self, keys):
            self.keys = keys

    # 插入一行 实现
    def insert(self, data,**kwargs):
        '''
        :param data: 行数据，字典或者列表
        :param is_first: 是否插入首行
        :param font: 字体
        :return:
        '''
        if kwargs.get('is_first',None):
            self.insertRow(0)
            row = 0
        else:
            self.insertRow(self.rowCount())
            row = self.rowCount()-1

        if isinstance(data, dict):
            for col_index, col_name in enumerate(self.heads.keys()):
                item = QTableWidgetItem(data[col_name])
                self.setItem(row, col_index, item)
        elif isinstance(data, list):
            for col_index, col_value in enumerate(data):
                item = QTableWidgetItem(col_value)
                self.setItem(row, col_index, item)

    def allData(self):
        '''
        :return: list
        '''
        if not self.rowCount():
            return
        return [self.selectRow2Dict(row) for row in range(self.rowCount())]

    # 鼠标跟踪功能
    def MouseTrackItem(self,row, col):
        self.setStyleSheet("selection-background-color:lightblue;") #选中项的颜色
        self.setCurrentCell(row, QItemSelectionModel.Select)  #设置该行为选中项

    # 第一列加选择框
    # for(int i = 0; i < 10; ++i)
    # {
    #     QStandardItem *item = new QStandardItem();
    #     item->setCheckable(true);
    #     item->setCheckState(Qt::Unchecked);
    #     m_pModel->setItem(i, 0, item);
    # }

    # # 导出数据，对表格数据聚合
    # def export(self):
    #     datas = self.allData()
    #     if not datas:
    #         mes_about(self, '没有内容！')
    #         return
    #     filename = self.setSaveFileName()
    #     if not filename:
    #         return
    #     df = pd.DataFrame(data=datas)
    #     df.to_excel(filename, columns=self.heads, index=False)
    #     mes_about(self, "导出完成！")
    #
    # def setSaveFileName(self):
    #     fileName, _ = QFileDialog.getSaveFileName(self, "保存文件",desktop(),"Excel 2007 Files (*.xlsx)",options=QFileDialog.DontUseNativeDialog)
    #     if fileName:
    #         return '%s.xlsx' % fileName