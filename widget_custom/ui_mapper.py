'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: ui_mapper.py
@time: 2019-1-23 9:21
@desc: 控件与数据模型绑定，用于生成增伤改查界面
'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDateTime,QDate,QTime
from decimal import Decimal
from datetime import datetime as type_datetime, date as type_date, time as type_time

# 获取控件的值
def widget_get_value(widget):
    '''
    :param widget: Qt控件
    :return:
    '''
    if isinstance(widget,(QLineEdit,QLabel,QDateEdit,QTimeEdit,QDateTimeEdit)):
        return widget.text()
    elif isinstance(widget,(QTextEdit,QPlainTextEdit)):
        return widget.toPlainText()
    elif isinstance(widget,(QSpinBox,QDoubleSpinBox)):
        return widget.value()
    elif isinstance(widget,QCheckBox):
        return {False:'0',True:'1'}.get(widget.isChecked(),'0')
    elif isinstance(widget,QComboBox):
        return widget.currentText()
    # 文件控件
    elif isinstance(widget,FileWidget):
        return widget.get_bytes()

    else:
        return None

# 设置控件的值
def widget_set_value(widget,value):
    '''
    :param widget: Qt控件
    :param value: Qt控件的值
    :return:
    '''
    if isinstance(widget,(QLineEdit,QLabel)):
        widget.setText(value)
    elif isinstance(widget,QDateEdit):
        widget.setDate(QDate().fromString(value, 'yyyy-MM-dd'))
    elif isinstance(widget,QTimeEdit):
        widget.setTime(QTime().fromString(value),'HH:mm:ss')
    elif isinstance(widget,QDateTimeEdit):
        widget.setDateTime(QDateTime().fromString(value,'yyyy-MM-dd HH:mm:ss'))
    elif isinstance(widget,(QTextEdit,QPlainTextEdit)):
        widget.setPlainText(value)
    elif isinstance(widget,QSpinBox):
        widget.setValue(int(value))
    elif isinstance(widget,QDoubleSpinBox):
        widget.setValue(float(value))
    elif isinstance(widget,QCheckBox):
        widget.setChecked(bool(int(value)))
    elif isinstance(widget,QComboBox):
        widget.setCurrentText(value)

# 根据数据库模型生成控件模型
def create_widget(pytype,pylength,isnull=False,iskey=False,isauto=False,default=0):
    '''
    :param pytype: 列类型
    :param pylength: 列长度
    :param isnull: 是否可以为空,True 表示不允许为空
    :return: widget
    '''
    if pytype == str:
        if pylength==None:
            widget = QPlainTextEdit()
        elif pylength==1:
            widget = QCheckBox()
            widget.setChecked(bool(int(default)))
        else:
            widget = QLineEdit()
            widget.setMaxLength(pylength)
            widget.setReadOnly(iskey)
            if isnull:
                widget.setPlaceholderText("允许空")
            else:
                widget.setPlaceholderText("不允许空")
    elif pytype == int:
        widget = QSpinBox()
        widget.setDisabled(iskey)
    elif pytype == Decimal:
        widget = QDoubleSpinBox()
    elif pytype == float:
        widget = QDoubleSpinBox()
    elif pytype == type_datetime:
        widget = QDateTimeEdit()
    elif pytype == type_date:
        widget = QDateEdit(QDate.currentDate())
        widget.setCalendarPopup(True)
        widget.setDisplayFormat("yyyy-MM-dd")
    elif pytype == type_time:
        widget = QDateEdit()
        widget.setDisplayFormat("HH:mm:ss")
    elif pytype == bytes:
        # 二进制
        widget = FileWidget()
    else:
        return

    return widget

# 文件读取控件
class FileWidget(QWidget):

    def __init__(self,parent=None):
        super(FileWidget,self).__init__(parent)
        self.initUI()
        self.btn_open_file.clicked.connect(self.setOpenFileName)

    def initUI(self):
        lt_main = QHBoxLayout()
        self.le_file = QLineEdit()
        self.le_file.setReadOnly(True)
        self.btn_open_file = QPushButton('选择文件')
        lt_main.addWidget(self.le_file)
        lt_main.addWidget(self.btn_open_file)
        self.setLayout(lt_main)

    def setOpenFileName(self):
        fileName, _ = QFileDialog.getOpenFileName(self,
                "QFileDialog.getOpenFileName()", self.le_file.text(),
                "All Files (*);;Word 2003 Files (*.doc);;Word 2007/2010 Files (*.docx);;Text Files (*.txt)")
        if fileName:
            self.le_file.setText(fileName)

    def get_bytes(self):
        if not self.le_file.text():
            return
        import zipfile
        f = zipfile.ZipFile('archive.zip', 'w', zipfile.ZIP_DEFLATED)
        f.write(self.le_file.text())
        f.close()
        with open('archive.zip',"rb") as f:
            return f.read()