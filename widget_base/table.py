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

# 多行表头，解决方案1：
# 使用一个QTableWidget命名为m_frozonTableWgt作为表头。
# 使用另外一个QTableWidget作为内容显示的表格。
# m_frozonTableWgt隐藏表头、隐藏滚动条、只显示2行的内容表格、显示到内容表格上方、只占据内容表的表头高度、设置ItemDelegate进行重绘。
# 内容表格，显示表头，高度设置成m_frozonTableWgt前两行的高度。

# 多行表头，采用2个表格组合的形式
class ComplexTableWidget(QTableWidget):

    def __init__(self, heads: dict, parent=None):
        super(ComplexTableWidget,self).__init__( heads, parent)

    def initTableHeader(self):
        frozen_table = QTableWidget()
        frozen_table.horizontalHeader().setVisible(False)                   # 表头不可见
        frozen_table.verticalHeader().setVisible(False)                     # 表头不可见
        frozen_table.setShowGrid(False)                                     # 网格线不可见
        frozen_table.setEditTriggers(QAbstractItemView.NoEditTriggers)      # 设置单元格不可编辑
        frozen_table.horizontalHeader().setStretchLastSection(True)         # 最后一个单元格扩展
        frozen_table.setFocusPolicy(Qt.NoFocus)                             # 解决选中虚框问题
        frozen_table.setFrameShape(QFrame.NoFrame)                          # 去除边框

        frozen_table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)      # // 隐藏滚动条
        frozen_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        frozen_table.setHorizontalScrollMode(ScrollPerPixel)

        frozen_table.setItemDelegate(ItemDelegate(0))        # 设置绘画代理（主要在代理中画出来header）

        self.viewport().stackUnder(frozen_table)                #设置窗口层次

        frozen_table.setColumnCount(10)                 # header10列
        frozen_table.setRowCount(2)                     # header2行

        frozen_table.setRowHeight(0, 42)                # 第一行设置高度42px
        frozen_table.setRowHeight(1, 42)                # 第二行设置高度42px

        # 隐藏2行后的行
        for row in range(2,frozen_table.rowCount()):
            frozen_table.setRowHidden(row, True)

    # def updateFrozenTableGeometry(self):
    #     self.frozen_table.setGeometry(frameWidth(),
    #                                   frameWidth(),
    #                                   viewport()->width(),
    #                                               horizontalHeader()->height())

# 某几列冻结的表格
class FreezeTableWidget(QTableView):

    def __init__(self, model):
        super(FreezeTableWidget, self).__init__()
        self.setModel(model)
        self.frozenTableView = QTableView(self)
        self.init()
        self.initSignal()


    def initSignal(self):
        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)
        self.frozenTableView.verticalScrollBar().valueChanged.connect(self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(self.frozenTableView.verticalScrollBar().setValue)

    def init(self):
        self.frozenTableView.setModel(self.model())
        self.frozenTableView.setFocusPolicy(Qt.NoFocus)
        self.frozenTableView.verticalHeader().hide()
        self.frozenTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.viewport().stackUnder(self.frozenTableView)

        self.frozenTableView.setStyleSheet('''
            QTableView { border: none;
                         background-color: #8EDE21;
                         selection-background-color: #999;
            }''')  # for demo purposes

        self.frozenTableView.setSelectionModel(self.selectionModel())
        for col in range(1, self.model().columnCount()):
            self.frozenTableView.setColumnHidden(col, True)
        self.frozenTableView.setColumnWidth(0, self.columnWidth(0))
        self.frozenTableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.frozenTableView.show()
        self.updateFrozenTableGeometry()
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.frozenTableView.setVerticalScrollMode(self.ScrollPerPixel)

    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        if self.logicalIndex == 0:
            self.frozenTableView.setColumnWidth(0, newSize)
            self.updateFrozenTableGeometry()

    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        self.frozenTableView.setRowHeight(logicalIndex, newSize)

    def resizeEvent(self, event):
        super(FreezeTableWidget, self).resizeEvent(event)
        self.updateFrozenTableGeometry()

    def moveCursor(self, cursorAction, modifiers):
        current = super(FreezeTableWidget, self).moveCursor(cursorAction, modifiers)
        if (cursorAction == self.MoveLeft and
                    self.current.column() > 0 and
                    self.visualRect(current).topLeft().x() <
                    self.frozenTableView.columnWidth(0)):
            newValue = (self.horizontalScrollBar().value() +
                        self.visualRect(current).topLeft().x() -
                        self.frozenTableView.columnWidth(0))
            self.horizontalScrollBar().setValue(newValue)
        return current

    def scrollTo(self, index, hint):
        if index.column() > 0:
            super(FreezeTableWidget, self).scrollTo(index, hint)

    def updateFrozenTableGeometry(self):
        self.frozenTableView.setGeometry(
            self.verticalHeader().width() + self.frameWidth(),
            self.frameWidth(), self.columnWidth(0),
            self.viewport().height() + self.horizontalHeader().height())

# 标准表格
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

    # 获取单行的字典 {col:value,......,colx:valuex,.....}
    def selectRow2Dict(self,*args,**kwargs):
        tmp = {}
        if self.keys:
            keys = self.keys
        elif args:
            keys = args
        else:
            keys = self.heads.keys()

        # 特殊处理，字典转换值，以后更新为UserData和ItemData分开取
        for key in keys:
            value = kwargs.get(key, {})
            if value:
                tmp[key] = value.get(self.curItemValueOfKey(key),'0')
            else:
                tmp[key] = self.curItemValueOfKey(key)

        return tmp

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