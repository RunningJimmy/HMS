from main.model import *
from widgets.LineEdit import *
from widgets.cwidget import *
from utils import gol
from utils import *


class Login_UI(QDialog):

    def __init__(self,parent=None):
        super(Login_UI,self).__init__(parent)
        self.initParas()
        self.initUI()

    def initParas(self):
        # 验证方式
        self.login_title = gol.get_value('login_title', '明州体检')
        self.lgoin_width = gol.get_value('login_width',500)
        self.login_height = gol.get_value('login_height',400)
        self.login_bg = file_ico("login.png")
        self.login_style = "font: 75 14pt \"微软雅黑\";" \
                      "color:  rgb(45, 135, 66);" \
                      "background-image: url(:/resource/image/login.png);"
        self.login_font = "font: 75 8pt;color:  #CD0000"
        # 获取用户名
        self.session = gol.get_value("tjxt_session_local")
        self.log = gol.get_value("log")

    def initUI(self):
        self.setWindowTitle(self.login_title)
        self.setFixedSize(self.lgoin_width,self.login_height)
        self.setWindowIcon(Icon("mztj"))
        self.setStyleSheet(self.login_style)
        self.setWindowFlags(Qt.FramelessWindowHint)     #窗口模式，去掉标题栏

        # 给窗体再加一个widget控件，对widget设置背景图片
        self.widget=QWidget(self)
        self.widget.setFixedSize(self.lgoin_width,self.login_height)
        palette=QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(self.login_bg)))
        self.widget.setPalette(palette)
        self.widget.setAutoFillBackground(True)

        lt_main = QVBoxLayout(self)
        lt_main.setAlignment(Qt.AlignCenter)
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignRight)
        layout.setFormAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        # 用户ID
        self.lb_user_id   = LineEdit(None,"", LineEdit.SUCCESS_STYLE)
        regx=QRegExp("[a-zA-Z0-9]+$")
        validator=QRegExpValidator(regx,self.lb_user_id)
        self.lb_user_id.setValidator(validator)              #根据正则做限制，只能输入数字
        self.lb_user_id.setMaximumWidth(200)
        # self.lb_user_id.setFocusPolicy(Qt.ClickFocus)
        # 用户姓名
        self.lb_user_name = LineEdit(None,"", LineEdit.SUCCESS_STYLE)
        self.lb_user_name.setDisabled(True)
        self.lb_user_name.setMaximumWidth(200)
        # 用户密码
        self.lb_user_pd = LineEdit(None,"", LineEdit.SUCCESS_STYLE)
        self.lb_user_pd.setMaximumWidth(200)
        self.lb_user_pd.setEchoMode(QLineEdit.Password)
        # 是否自动填充
        self.is_rem=QCheckBox("记住最近登录")
        self.is_rem.setStyleSheet(self.login_font)
        # 进入主界面还是接口界面
        self.is_equip=QCheckBox("进入设备接口")
        self.is_equip.setStyleSheet(self.login_font)

        # 版本号
        self.lb_version = QLabel(self)
        self.lb_version.setText('当前版本：%s' %str(gol.get_value('system_version', '读取失败')))
        self.lb_version.setStyleSheet(self.login_font)
        self.lb_version.setGeometry(QRect(400, 360, 100, 30))

        if not gol.get_value('login_auto_record',0):
            self.is_rem.setChecked(False)
        else:
            self.is_rem.setChecked(True)
            # 自动填充最近登录信息
            self.lb_user_id.setText(str(gol.get_value('login_user_id', 'BSSA')))
            self.lb_user_name.setText(gol.get_value('login_user_name', '管理员'))

        if not gol.get_value('system_is_equip',0):
            self.is_equip.setChecked(False)
        else:
            self.is_equip.setChecked(True)

        ######################添加布局##########################################
        layout0 = QHBoxLayout()
        layout0.addWidget(self.is_rem)
        layout0.addWidget(self.is_equip)
        layout0.addStretch()
        login_user = "                       "
        layout.addWidget(QLabel(""))
        layout.addRow(QLabel("账户："), self.lb_user_id)
        layout.addRow(login_user,self.lb_user_name)
        layout.addRow(QLabel("密码："), self.lb_user_pd)
        layout.addRow(QLabel(""), layout0)
        layout.setHorizontalSpacing(10)
        layout.setVerticalSpacing(10)

        self.buttonBox=QDialogButtonBox()
        self.buttonBox.addButton("登录",QDialogButtonBox.YesRole)
        self.buttonBox.addButton("取消", QDialogButtonBox.NoRole)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.buttons()[0].setEnabled(False)
        # 失去焦点
        # self.buttonBox.buttons()[0].setFocusPolicy(Qt.ClickFocus)
        # self.buttonBox.buttons()[1].setFocusPolicy(Qt.NoFocus)

        # 对登录进行限制
        if self.lb_user_name.text():
            self.buttonBox.buttons()[0].setEnabled(True)
        else:
            self.buttonBox.buttons()[0].setEnabled(False)

        self.lb_user_id.textEdited.connect(self.set_empty)
        self.lb_user_id.editingFinished.connect(self.user_get)
        self.is_equip.stateChanged.connect(self.on_equip_change)
        self.buttonBox.accepted.connect(self.login)
        self.buttonBox.rejected.connect(self.reject)

        lt_main.addSpacing(30)
        lt_main.addLayout(layout)
        lt_main.addSpacing(20)
        lt_main.addWidget(self.buttonBox)
        self.setLayout(lt_main)

    def on_equip_change(self,p_int):
        gol.set_value("system_is_equip",p_int)

    def user_get(self):
        user_id = self.lb_user_id.text()
        if not user_id:
            mes_about(self,"请输入账户！")
            return
        try:
            result = self.session.query(MT_TJ_USER).filter(MT_TJ_USER.xtsb=='101',MT_TJ_USER.yhdm==user_id).scalar()
            if result:
                self.lb_user_name.setText(str2(result.yhmc))
                self.buttonBox.buttons()[0].setEnabled(True)
        except Exception as e:
            mes_about(self,"读取数据库失败！错误信息：%s" %e)

    def set_empty(self,p_str):
        self.lb_user_id.setText(p_str.upper())
        self.lb_user_name.setText("")
        self.buttonBox.buttons()[0].setEnabled(False)

    # 验证密码
    def login(self):
        _user_id=self.lb_user_id.text()
        _user_name = self.lb_user_name.text()
        _user_pwd=self.lb_user_pd.text()
        if not _user_id:
            mes_about("请输入账户！！")
            return
        try:
            result = self.session.query(MT_TJ_USER).filter(MT_TJ_USER.xtsb == '101', MT_TJ_USER.yhdm == _user_id).filter(or_(MT_TJ_USER.yhkl==_user_pwd,MT_TJ_USER.yhkl==None)).scalar()
        except Exception as e:
            mes_about(self,"从数据库中验收密码失败！错误信息：%s" %e)
            return
        if not result:
            mes_warn(self, "您输入的账户:%s,密码:%s，有误！\n请确认后重新登陆！" % (_user_id, _user_pwd))
            return
        results = self.session.query(MT_TJ_YGQSKS).filter(MT_TJ_YGQSKS.yggh == _user_id).all()
        ksbms = [result.ksbm.rstrip() for result in results]
        gol.set_value('login_user_ksbms', ksbms)
        gol.set_value('login_user_id',_user_id)
        gol.set_value('login_user_name', _user_name)
        gol.set_value('login_user_pwd', _user_pwd)
        gol.set_value('login_time', cur_datetime())
        ############### 写入配置 #########################
        if self.is_rem.isChecked():
            auto_record = 1
        else:
            auto_record = 0
        if self.is_equip.isChecked():
            is_equip = 1
        else:
            is_equip = 0
        login={
            "auto_record":auto_record,
            "user_id":_user_id,
            "user_name":_user_name
        }
        system={
            "is_equip":is_equip
        }
        config_write("custom.ini", "login", login)
        config_write("custom.ini", "system", system)
        self.log.info('写入配置(custom.ini)文件成功')
        self.log.info("用户：%s(%s) 登陆成功！" %(_user_name,_user_id))
        # 写入登录记录，获取主键ID
        login_obj = MT_TJ_LOGIN(
            login_id = _user_id,
            login_name =_user_name,
            login_area = gol.get_value('login_area', ''),
            login_ip = gol.get_value('host_ip', ''),
            login_host = gol.get_value('host_name', ''),
            login_in = gol.get_value('login_time', '')
        )
        try:
            self.session.add(login_obj)
            # 先写入数据库，但是不提交 ,此时可获取自增ID
            self.session.flush()
            gol.set_value('login_lid', login_obj.lid)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            mes_about(self, '执行发生错误：%s' % e)
            return
        # 跳转
        self.accept()





if __name__=="__main__":
    from utils.envir import *
    set_env()
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    ui = Login_UI()
    ui.show()
    ui.exec_()