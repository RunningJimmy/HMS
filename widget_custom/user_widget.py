'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: user_widget.py
@time: 2019-2-8 16:06
@version：0.1
@desc: 用户相关控件
'''


import ctypes
from .common import *

#用户信息窗口
class UserInfoWidget(QWidget):

    def __init__(self,parent=None):
        super(UserInfoWidget,self).__init__(parent)
        self.initUI()

    def initUI(self):
        lt_main = FlowLayout()
        self.user = OrderedDict([
            ("tjbh", "体检编号"),
            ("xm", "姓名"),
            ("xb", "性别"),
            ("nl", "年龄"),
            ("sjhm", "手机号"),
            ("sfzh", "身份证号"),
            ("depart", "部门"),
            ("dwmc", "单位名称"),

        ])
        self.setLayout(lt_main)

# 身份证
class UserRowWidget(QWidget):

    def __init__(self,lable_txt:str,lable_widget:QWidget):
        super(UserRowWidget,self).__init__()
        lt_main = HBoxLayout()
        lt_main.addWidget(UserLabel(lable_txt))
        lt_main.addWidget(lable_widget)
        lt_main.addStretch()
        self.setLayout(lt_main)

# 用户标签值
class UserLabelEdit(QLineEdit):
    # 读模式下的样式
    read_style = '''
        QLineEdit {
            border: none;
            border-bottom: 1px solid rgb(0, 0, 0);
            font-size: 11pt ; 
            color: rgb(0, 85, 255);
            text-align:left;
            background: transparent;
        }
        '''
    # 写模式下的样式
    write_style = '''
        QLineEdit {
            border: none;
            border-bottom: 1px solid rgb(0, 0, 0);
            font-size: 11pt ; 
            color: rgb(0, 85, 255);
            text-align:left;
            background: rgb(255, 255, 255);
        }
        QLineEdit:hover {
            border: 1px solid blue;  
        }
        '''
        # 鼠标悬停时，我们将编辑框的边框设置为蓝色

    def __init__(self,parent=None):
        super(UserLabelEdit,self).__init__(parent)
        self.setStyleSheet(self.read_style)
        self.setReadOnly(True)
        self.editingFinished.connect(self.on_edit_finished)

    # 双击编辑
    def mouseDoubleClickEvent(self, QMouseEvent):
        self.setReadOnly(False)
        self.setStyleSheet(self.write_style)

    # 完成编辑
    def on_edit_finished(self):
        self.setStyleSheet(self.read_style)
        self.setReadOnly(True)

# 用户标签
class UserLabel(QLabel):

    def __init__(self,*args):
        super(UserLabel,self).__init__(*args)
        self.setStyleSheet('''QLabel {
        border:none;
        border: 0px solid rgb(0, 0, 0);
        margin-bottom:1px;
        text-align:right;
        }''')
        self.setFixedWidth(60)

# 文本搜索控件
class SearchLabel(UserLabelEdit):

    singal_search = pyqtSignal(str)
    # 控件中文名，控件英文名即objectName
    cname = None

    def __init__(self,parent=None):
        super(SearchLabel,self).__init__(parent)
        action_serach = self.addAction(Icon('查询'), QLineEdit.TrailingPosition)
        action_serach.triggered.connect(self.on_action_serach)

    def on_action_serach(self):
        self.singal_search.emit(self.text())

# 身份证 控件，待读卡，刷选功能
class UserCardId(SearchLabel):

    cname = '身份证号：'

    def __init__(self,parent=None):
        super(UserCardId,self).__init__(parent)
        self.setFixedWidth(200)
        action_read = self.addAction(Icon('身份证'),QLineEdit.LeadingPosition)
        action_read.triggered.connect(self.on_action_read)
        # 简单验证 身份证号码为15位或者18位，15位时全为数字，18位前17位为数字，最后一位是校验位，可能为数字或字符X
        validator = QRegExpValidator(QRegExp("(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)"), self)
        self.setValidator(validator)  # 根据正则做限制，只能输入数字和X

    def on_action_read(self):
        dialog = ReadCardIdDialog()
        dialog.exec_()

# 体检编号
class UserTJBH(SearchLabel):

    cname = '体检编号：'

    def __init__(self, parent=None):
        super(UserTJBH, self).__init__(parent)
        self.setFixedWidth(100)
        validator = QRegExpValidator(QRegExp("[0-9]+$"), self)
        self.setValidator(validator)  # 根据正则做限制，只能输入数字

    # 双击编辑
    def mouseDoubleClickEvent(self, QMouseEvent):
        pass

# 姓名
class UserName(SearchLabel):

    cname = '姓名：'

    def __init__(self, parent=None):
        super(UserName, self).__init__(parent)
        self.setFixedWidth(80)

# 手机号码
class UserPhone(SearchLabel):

    cname = '手机号码：'

    def __init__(self, parent=None):
        super(UserPhone, self).__init__(parent)
        self.setFixedWidth(150)
        validator = QRegExpValidator(QRegExp("^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$"), self)
        self.setValidator(validator)  # 根据正则做限制，只能输入数字

# 搜索控件，用于快速检索，业务系统常用的
class SearchLine(QLineEdit):

    singal_search = pyqtSignal(str,str)

    style = ''' 
        QLineEdit {
            border: 0px solid rgb(41, 57, 85);   /* 边框1px宽，颜色为深紫色 */
            border-radius: 3px;  /* 给定3px边框圆角 */
            background: white;   /* 背景色定为白色吧 */
            selection-background-color: green; /* 这个属性设定文本选中时的文本背景色 */
            font-size: 10pt ;  /* 文本的大小 */
        }

        QLineEdit:hover {
            border: 1px solid blue;  /* 鼠标悬停时，我们将编辑框的边框设置为蓝色 */
        }
    '''
    # 控件中文名，控件英文名即objectName
    cname = None

    def __init__(self, parent=None):
        super(SearchLine, self).__init__(parent)
        # 点击按钮查询
        action_serach = self.addAction(Icon('查询'), QLineEdit.TrailingPosition)
        action_serach.triggered.connect(self.on_action_serach)
        # 回车查询
        self.returnPressed.connect(self.on_action_serach)
        self.setStyleSheet(self.style)

    def on_action_serach(self):
        self.singal_search.emit(self.objectName(),self.text())

# 搜索控件 -> 体检编号
class SearchByTJBH(SearchLine):

    cname = '体检编号：'

    def __init__(self, parent=None):
        super(SearchByTJBH, self).__init__(parent)
        self.setObjectName('tjbh')
        self.setPlaceholderText("输体检编号检索")
        validator = QRegExpValidator(QRegExp("[0-9]+$"), self)
        self.setValidator(validator)  # 根据正则做限制，只能输入数字

# 搜索控件 -> 姓名
class SearchByName(SearchLine):

    cname = '姓    名：'

    def __init__(self, parent=None):
        super(SearchByName, self).__init__(parent)
        self.setObjectName('xm')
        self.setPlaceholderText("输姓名检索")

# 搜索控件 -> 手机号码
class SearchByPhone(SearchLine):

    cname = '手机号码：'

    def __init__(self, parent=None):
        super(SearchByPhone, self).__init__(parent)
        self.setObjectName('sjhm')
        self.setPlaceholderText("输手机号码检索")
        validator = QRegExpValidator(QRegExp("^1([38][0-9]|4[579]|5[0-3,5-9]|6[6]|7[0135678]|9[89])\d{8}$"), self)
        self.setValidator(validator)  # 根据正则做限制，只能输入数字

# 搜索控件 -> 身份证
class SearchByCardId(SearchLine):

    cname = '身份证号：'

    def __init__(self, parent=None):
        super(SearchByCardId, self).__init__(parent)
        self.setObjectName('sfzh')
        self.setPlaceholderText("输身份证号检索")
        # 输入验证
        validator = QRegExpValidator(QRegExp("(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)"), self)
        self.setValidator(validator)  # 根据正则做限制，只能输入数字和X
        # 读卡搜索
        action_read = self.addAction(Icon('身份证'), QLineEdit.LeadingPosition)
        action_read.triggered.connect(self.on_action_read)

    def on_action_read(self):
        dialog = ReadCardIdDialog()
        dialog.signal_cardid.connect(self.on_search)
        dialog.exec_()

    def on_search(self,cardid:str):
        self.setText(cardid)
        self.on_action_serach()

# 搜索窗口，多种
class QuickSearchWidget(QWidget):

    singal_set_data = pyqtSignal(dict)
    singal_get_data = pyqtSignal(str,str)

    def __init__(self,parent=None):
        super(QuickSearchWidget,self).__init__(parent)
        self.initUI()
        self.initSignal()

    # 绑定信号槽
    def initSignal(self):
        self.singal_set_data.connect(self.setSearchData)
        for widget in self.search_widgets:
            widget.singal_search.connect(self.getSearchData)
        # self.search_tjbh.singal_search.connect(self.getSearchData)
        # self.search_name.singal_search.connect(self.getSearchData)
        # self.search_phone.singal_search.connect(self.getSearchData)
        # self.search_cardid.singal_search.connect(self.getSearchData)

    # 初始化界面
    def initUI(self):
        self.search_widgets = []
        self.search_tjbh = SearchByTJBH()
        self.search_name = SearchByName()
        self.search_phone = SearchByPhone()
        self.search_cardid = SearchByCardId()
        self.search_widgets.append(self.search_tjbh)
        self.search_widgets.append(self.search_name)
        self.search_widgets.append(self.search_phone)
        self.search_widgets.append(self.search_cardid)
        lt_main = QGridLayout()
        ###################基本信息  第一行##################
        lt_main.addWidget(QLabel(self.search_tjbh.cname), 0, 0, 1, 1)
        lt_main.addWidget(self.search_tjbh, 0, 1, 1, 1)
        lt_main.addWidget(QLabel(self.search_name.cname), 0, 2, 1, 1)
        lt_main.addWidget(self.search_name, 0, 3, 1, 1)
        ###################基本信息  第二行##################
        lt_main.addWidget(QLabel(self.search_phone.cname), 1, 0, 1, 1)
        lt_main.addWidget(self.search_phone, 1, 1, 1, 1)
        lt_main.addWidget(QLabel(self.search_cardid.cname), 1, 2, 1, 1)
        lt_main.addWidget(self.search_cardid, 1, 3, 1, 2)
        # lt_main.setHorizontalSpacing(10)  # 设置水平间距
        # lt_main.setVerticalSpacing(10)  # 设置垂直间距
        # lt_main.setContentsMargins(10, 10, 10, 10)  # 设置外间距
        lt_main.setColumnStretch(6, 1)  # 设置列宽，添加空白项的
        self.setLayout(lt_main)

    # 设置数据
    def setSearchData(self,data:dict):
        for widget in self.search_widgets:
            widget.setText(data.get(widget.objectName(),''))
        # self.search_tjbh.setText(data.get(self.search_tjbh.objectName(),''))
        # self.search_name.setText(data.get(self.search_name.objectName(), ''))
        # self.search_phone.setText(data.get(self.search_phone.objectName(), ''))
        # self.search_cardid.setText(data.get(self.search_cardid.objectName(), ''))

    # 读取数据
    def getSearchData(self,obj_name:str,obj_value:str):
        self.singal_get_data.emit(obj_name,obj_value)

# 身份证字体 绝对定位
class CardIdLable(QLabel):

    def __init__(self,parent,left:int,top:int, width:int, height:int):
        super(CardIdLable,self).__init__(parent)
        self.setGeometry(QRect(left,top, width, height))
        self.setStyleSheet('''font: 75 14pt \"微软雅黑\";color: rgb(255, 0, 0);''')

class CardIdLable2(QTextEdit):

    def __init__(self,parent,left:int,top:int, width:int, height:int):
        super(CardIdLable2,self).__init__(parent)
        self.setGeometry(QRect(left,top, width, height))
        self.setStyleSheet('''font: 75 14pt \"微软雅黑\";color: rgb(255, 0, 0);''')

# 读取身份证显示界面
class ReadCardIdDialog(QDialog):

    # 自定义 信号，封装对外使用  身份证号、姓名
    sendIdCard = pyqtSignal(str,str)
    # 只传输身份证号
    signal_cardid = pyqtSignal(str)

    widget_style = '''
        font: 75 14pt \"微软雅黑\";
        background-image: url(:/resource/image/sfzback.png);'''

    def __init__(self,parent=None):
        super(ReadCardIdDialog,self).__init__(parent)
        self.setWindowTitle('明州体检')
        self.setFixedSize(498,394)
        self.setStyleSheet(self.widget_style)
        self.initUI()
        # 特殊变量
        self.read_card_thread = None
        self.readidcard()
        # 绑定信号槽
        self.buttonBox.accepted.connect(self.on_sure)
        self.buttonBox.rejected.connect(self.close)

    def initUI(self):
        # 给窗体再加一个widget控件，对widget设置背景图片
        self.widget=QWidget(self)
        self.widget.setFixedSize(498,394)
        palette=QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(icon_dir("sfzback.png"))))
        self.widget.setPalette(palette)
        self.widget.setAutoFillBackground(True)
        # 采用绝对位置 控件组
        self.lb_user_name = CardIdLable(self,110, 62, 61, 21)               # 姓名
        self.lb_user_sex = CardIdLable(self,110, 84, 31, 21)                # 性别
        self.lb_user_nation = CardIdLable(self,190, 86, 31, 21)             # 名族
        self.lb_user_birth = CardIdLable(self,110, 111, 101, 16)            # 出生
        self.lb_user_addr = CardIdLable(self,110, 134, 311, 16*4)             # 地址
        self.lb_user_card = CardIdLable(self,172, 180, 271, 16)             # 身份证号
        self.lb_user_qfjg = CardIdLable(self, 130, 220, 271, 16)            # 签发机关
        self.lb_user_yxqx = CardIdLable(self, 130, 247, 271, 16)            # 有效期限
        self.lb_user_zxzz = CardIdLable(self, 130, 268, 311, 21)            # 最新住址
        # 消息 ：错误信息
        self.lb_message = CardIdLable(self, 10, 360, 281, 21)
        self.lb_message.setText('请放卡...')
        # 按钮框
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.addButton("确定",QDialogButtonBox.YesRole)
        self.buttonBox.addButton("取消", QDialogButtonBox.NoRole)
        self.buttonBox.setGeometry(QRect(320, 345, 100, 50))
        #self.buttonBox.setCenterButtons(True)

    def readidcard(self):
        if not self.read_card_thread:
            self.read_card_thread = ReadCardIdThread()
        self.read_card_thread.signalPost.connect(self.setData, type=Qt.QueuedConnection)
        self.read_card_thread.signalError.connect(self.showMes, type=Qt.QueuedConnection)
        self.read_card_thread.start()

    def setData(self,data:list):
        self.lb_user_name.setText(data[0])
        self.lb_user_sex.setText(data[1])
        self.lb_user_nation.setText(data[2])
        self.lb_user_birth.setText(data[3])
        self.lb_user_addr.setText(data[4])
        self.lb_user_addr.setWordWrap(True)
        self.lb_user_addr.setAlignment(Qt.AlignTop)
        self.lb_user_card.setText(data[5])
        self.lb_user_qfjg.setText(data[6])
        self.lb_user_qfjg.adjustSize()
        self.lb_user_yxqx.setText(data[7])
        self.lb_user_zxzz.setText(data[8])

    # 确定
    def on_sure(self):
        self.sendIdCard.emit(self.lb_user_card.text(),self.lb_user_name.text())
        self.signal_cardid.emit(self.lb_user_card.text())
        self.accept()
        self.close()

    def showMes(self,message:str):
        self.lb_message.setText(message)

    def closeEvent(self, *args, **kwargs):
        try:
            if self.read_card_thread:
                self.read_card_thread.stop()
                self.read_card_thread = None
        except Exception as e:
            print(e)
        super(ReadCardIdDialog, self).closeEvent(*args, **kwargs)

class ReadCardIdThread(QThread):

    # 定义信号,定义参数为str类型
    signalError = pyqtSignal(str)     # 错误信息
    signalPost = pyqtSignal(list)     # 更新界面
    signalExit = pyqtSignal()

    def __init__(self):
        super(ReadCardIdThread,self).__init__()
        self.tmp_file_wz = os.path.join(os.environ["TMP"], 'chinaidcard\wz.txt')
        self.tmp_file_zp = os.path.join(os.environ["TMP"], 'chinaidcard\zp.bmp')
        self.c_obj = ReadCardId()
        self.runing = True

    def stop(self):
        self.runing = False

    def run(self):
        while self.runing:
            if self.c_obj.dll_obj:
                open_state = self.c_obj.open()
                if open_state == 1:
                    legal_state = self.c_obj.legal()
                    if legal_state == 1:
                        if self.c_obj.read(4) == 1:
                            user_info = open(self.tmp_file_wz).read().split('\n')
                            self.signalPost.emit(user_info)
                            os.remove(self.tmp_file_wz)
                            os.remove(self.tmp_file_zp)
                            self.signalError.emit('读卡成功！')
                        else:
                            self.signalError.emit('读卡失败！')
                    elif legal_state == 2:
                        self.signalError.emit('请重新放卡...')
                    elif legal_state == 3:
                        self.signalError.emit('选卡失败！')
                    else:
                        self.signalError.emit('初始化失败！')
                else:
                    self.signalError.emit('动态库加载失败/端口打开失败！')
            else:
                self.signalError.emit('动态库加载失败！')

            time.sleep(0.3)

# 载入动态库->初始化->卡认证->读卡->关闭连接
class ReadCardId(object):

    def __init__(self,dll_name="termb.dll",port_type='usb'):
        '''
        :param port_type: 连接用USB口/串口。port：连接串口（COM1~COM16）或USB口(1001~1016)
        :param dll_name: 动态库名字，带文件路径，默认根目录
        '''
        self.ports = list(range(1,17))+list(range(1001,1017))
        # if port_type == 'usb':
        #     self.ports = range(1001, 1017)
        # else:
        #     self.ports = range(1, 17)

        # 加载动态库
        try:
            self.dll_obj = ctypes.windll.LoadLibrary(dll_name)
            # self.dll_obj = ctypes.WinDLL("termb.dll")
        except Exception as e:
            print('未找到身份证读卡器驱动DLL：%s' % dll_name)
            self.dll_obj = None

        # 卡连接状态
        self.is_conn=None

    # 本函数用于PC与华视电子第二代居民身份证阅读器的连接
    def open(self):
        '''
        :return:
            # 值   意义
            # 1   正确
            # 2   端口打开失败
            # 0   动态库加载失败
        '''
        for port in self.ports:
            if self.dll_obj.CVR_InitComm(port)==1:
                self.is_conn = True
                return True
        else:
            return False

    # 本函数用于关闭PC到阅读器的连接
    def close(self):
        '''
        :return:
            # 值   意义
            # 1   正确
            # 0   错误
        '''
        if self.is_conn:
            self.dll_obj.CVR_CloseComm()

    # 本函数用于读卡器和卡片之间的合法身份确认。卡认证循环间隔大于300ms。
    # 若卡片放置后发生认证错误时，应移走卡片重新放置。
    def legal(self):
        '''
        :return:
            # 值   意义  说明
            # 1   正确  卡片认证成功
            # 2   错误  寻卡失败
            # 3   错误  选卡失败
            # 0   错误  初始化失败
        '''

        return self.dll_obj.CVR_Authenticate()


    # 本函数用于通过阅读器从第二代居民身份证中读取相应信息。
    # 卡认证成功以后才可做读卡操作，读卡完毕若继续读卡应移走二代证卡片重新放置做卡认证。
    def read(self,active:int):
        # '''
        # :param active:
        #     参数名  含义                     取值范围
        #     active  临时目录中保存哪些文件   见取值说明
        #     ############################################
        #     取值说明：
        #         值	意义
        #         1	wz.txt，xp.wlt，zp.bmp，fp.dat
        #         2	wz.txt，xp.wlt，fp.dat
        #         4	wz.txt，zp.bmp，fp.dat
        #     ############################################
        #     文件说明：
        #         文件名	意义
        #         wz.txt	身份证基本信息，如姓名、性别等
        #         xp.wlt	加密的头像数据
        #         zp.bmp	解密的头像数据
        #         fp.dat	指纹数据，若无指纹则该文件大小仍为1024字节，每个字节均为0
        #     #############################################
        #     1、wz.txt文件格式
        #     读卡成功后在临时目录下生成wz.txt（文字信息）和zp.bmp（照片信息）
        #     临时目录跟当前登录用户名称有关，如C:\Users\mac\AppData\Local\Temp\chinaidcard
        #     wz.txt内容示例如下：
        #     张红叶
        #     女
        #     汉
        #     19881118
        #     河北省邯郸市临漳县称勾镇称勾东村复兴路25号
        #     130423198811184328
        #     临漳县公安局
        #     20110330-20210330
        #
        # :return:
        #         值	意义
        #         1	正确
        #         0	错误
        #         99	异常
        # '''
        return self.dll_obj.CVR_Read_Content(active)


    # 读卡至内存
    def read2(self):
        self.dll_obj.CVR_ReadBaseMsg()