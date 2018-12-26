import requests
from .main_ui import *
from .model import *
from utils import gol,config_write
from utils.base import cur_date,cur_datetime,get_system
# 动态模块需加入，打包工具无法检测自省模块，要不然需以源码形式跑
# 采血留样 管理
from lis import SampleManager
# C13/14 管理
from C13 import BreathManager
# 报告管理
from report import ReportManager
# 慢病管理
from mbgl import NCDManager
# 结果录入管理
from result import ResultManager
# 加入VIP 管理
from vip import VipManager
# 加入绩效
from statistics import DN_MeritPay,LoginUserUI,LoginInUI
# 体检登记
from register import RegisterManager
# OA
from app_interface import OaUI,PhoneUI,JHJKGLUI,MediaUI,WJZUI

WindowsTitle="明州体检"
WindowsIcon="mztj"

class TJ_Main_UI(QMainWindow):

    def __init__(self):
        super(TJ_Main_UI, self).__init__()

        #载入参数
        self.initParas()
        # 载入公共组件：菜单栏、工具栏、状态栏
        self.initUI()
        # 载入样式
        with open(self.stylesheet) as f:
            self.setStyleSheet(f.read())
        # 载入当前用户默认界面
        action = self.menuBar().default_action(self.user_menu_sid)
        if action:
            self.openWidget(action)
        else:
            mes_about(self,'用户登录默认界面配置不正确或者未开放，按钮SID是%s' %str(self.user_menu_sid))

        # 绑定信号槽
        self.statusBar().label_clicked.connect(self.on_status_bar_click)
        # 启动自动更新线程
        if self.update_auto:
            self.timer_update_thread = AutoUpdateThread(600)
            self.timer_update_thread.setTask(self.url)
            self.timer_update_thread.signalPost.connect(self.update_mes, type=Qt.QueuedConnection)
            self.timer_update_thread.signalCount.connect(self.online_count_show, type=Qt.QueuedConnection)
            self.timer_update_thread.start()


    # 初始化界面
    def initUI(self):
        self.setWindowTitle(WindowsTitle)
        self.setWindowIcon(Icon(WindowsIcon))
        self.initMenuBar()
        self.initStatusBar()

        self.mdiArea=QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.SubWindowView)                       #子窗口模式
        self.setCentralWidget(self.mdiArea)

    # 初始化参数
    def initParas(self):
        self.log = gol.get_value('log')
        self.stylesheet = file_style(gol.get_value('file_qss','mztj.qss'))
        self.update_auto = gol.get_value('update_auto',True)
        self.update_timer = gol.get_value('update_timer',360)
        self.user_menu_sid = gol.get_value('menu_sid',5001)
        self.login_id = gol.get_value('login_user_id')
        self.session = gol.get_value('tjxt_session_local', '')
        self.login_name = gol.get_value('login_user_name', '')
        self.login_time = gol.get_value('login_time', '')
        sys_version = gol.get_value('system_version', 1.0)
        update_url = gol.get_value('system_update', "http://10.7.200.101:5005/api/version/%s/%s")
        self.url = update_url % (get_system(), sys_version)

    def initStatusBar(self):
        self.setStatusBar(StatusBar())

    def initMenuBar(self):
        self.setMenuBar(MenuBar(self))

    # 状态栏标签被点击
    def on_status_bar_click(self,p1_str):
        if '登录' in p1_str:
            ui = LoginUserUI(self)
            ui.opened.emit()
            ui.exec_()
        elif '在线' in p1_str:
            ui = LoginInUI(self)
            ui.opened.emit(cur_date())
            ui.exec_()
        elif '房间' in p1_str:
            text, ok = QInputDialog.getText(self, '明州体检', '房间名称更改：', QLineEdit.Normal, '')
            if ok and text:
                # 写入配置
                login_cfg={"area":text}
                config_write("custom.ini", "login", login_cfg)
                # 刷新缓存
                gol.set_value('login_area',text)
                # 刷新UI
                self.statusBar().set_lable_text(text)
        elif '版本' in p1_str:
            print("查看版本记录")
        elif '用户' in p1_str:
            text, ok = QInputDialog.getText(self, '明州体检', '密码更改：', QLineEdit.Normal, '')
            if ok and text:
                print(text)

    # 打开中央窗口
    def openWidget(self,action):
        module = action.module
        class_name = action.cls_name   # 必须在上一句后面，因为才赋值
        if module and class_name:
            # if class_name=='DN_MeritPay' and self.login_id=='BSSA':
            #     mes_about(self,"对不起，您没有该功能权限，请联系管理员！")
            #     return
            if not hasattr(self, class_name):
                module_class = getattr(module, class_name)
                setattr(self, class_name, module_class())
                self.mdiArea.addSubWindow(getattr(self, class_name))
                getattr(self, class_name).showMaximized()
                if class_name in ['OaUI','PhonePlatUI','JHJKGLUI','MediaUI','WJZUI']:
                    getattr(self, class_name).load()
            elif getattr(getattr(self, class_name), 'status'): # 窗口被关闭了
                module_class = getattr(module, class_name)
                setattr(self, class_name, module_class())
                self.mdiArea.addSubWindow(getattr(self, class_name))
                getattr(self, class_name).showMaximized()
                if class_name in ['OaUI','PhonePlatUI','JHJKGLUI','MediaUI','WJZUI']:
                    getattr(self, class_name).load()
            # # 未关闭
            getattr(self, class_name).setFocus()
        else:
            mes_about(self,"该模块不存在，请联系管理员！")

    # 注销
    def login_out(self):
        self.close()
        from main.login_ui import Login_UI
        login_ui = Login_UI()
        if login_ui.exec_():
                pass

    def update_mes(self,version,message):
        dialog = UpdateDialog(self)
        dialog.sure_update.connect(self.update_sys)
        dialog.setDatas(version,message)
        dialog.exec_()
        # dialog = mes_warn(self,"系统已有新版本")
        # if dialog != QMessageBox.Yes:
        #     pass
        # 历史版本，优先下载到本地，再提示是否更新，速度更优
        # dialog = mes_warn(self,message)
        # if dialog != QMessageBox.Yes:
        #     pass
        # else:
        #     self.close()
        #     # 启动更新进程
        #     try:
        #         sub_process_name = gol.get_value('main_process_sub', 'autoupdate.exe')
        #         os.popen(sub_process_name)
        #         self.log.info('启动更新进程！')
        #     except Exception as e:
        #         self.log.info('启动更新进程失败，错误信息：%s' %e)

    def update_sys(self):
        # self.close()
        process = QProcess()
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        update_process_name = os.path.join(dirname, 'autoupdate.exe')
        # print(update_process_name)
        try:
            process.startDetached(update_process_name)
            print("准备更新程序，启动更新进程！")
            # log.info("准备更新程序，启动更新进程！")
            sys.exit(0)
            # os._exit()
        except Exception as e:
            print("准备更新程序，启动更新进程失败，错误信息：%s" % e)
            # log.info("准备更新程序，启动更新进程失败，错误信息：%s" % e)
            return

    # 定时刷新登录用户、在线用户
    def online_count_show(self,p1_int,p2_int):
        self.statusBar().on_login_info_show(p1_int,p2_int)

    def closeEvent(self, QEvent):
        button = mes_warn(self, "温馨提示：您确认退出系统吗？")
        if button != QMessageBox.Yes:
            QEvent.ignore()
            return
        else:
            QEvent.accept()
        try:
            self.session.query(MT_TJ_LOGIN).filter(MT_TJ_LOGIN.login_id == self.login_id,
                                                   MT_TJ_LOGIN.lid == gol.get_value('login_lid',0)
                                                   ).update({
                MT_TJ_LOGIN.login_out:cur_datetime()
            })
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            mes_about(self, '执行发生错误：%s' % e)

        super(TJ_Main_UI, self).closeEvent(QEvent)
        try:
            if hasattr(self, 'SampleManager'):
                getattr(self, 'SampleManager').close()
        except Exception as e:
            self.log.info("关闭时发生错误：%s " %e)

        QThread.currentThread().quit()
        self.log.info("用户：%s(%s) 退出成功！" % (gol.get_value('login_user_name', '未知'), gol.get_value('login_user_id', ''),))


# 自动检测更新包线程
class AutoUpdateThread(QThread):

    # 定义信号,定义参数为str类型
    signalPost = pyqtSignal(str, str)     # 更新界面
    signalCount = pyqtSignal(int, int)  # 更新界面
    signalExit = pyqtSignal()

    def __init__(self,timer=360):
        super(AutoUpdateThread, self).__init__()
        self.running = False
        self.timer = timer
        self.session = gol.get_value("tjxt_session_local")

    def setTask(self,url):
        self.url = url
        self.running = True
        self.count = 0

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            if self.count==0:
                try:
                    print("请求")
                    response = requests.get(self.url)
                    if response.status_code == 200:
                        describe = response.json()['describe']
                        version = response.json()['version']
                        self.signalPost.emit(str(version),describe)
                except Exception as e:
                    print(e)

            # count_login = 0
            # count_online = 0
            count_login = self.session.query(func.count(distinct(MT_TJ_LOGIN.login_id))).filter(MT_TJ_LOGIN.login_in >= cur_date()).scalar()
            count_online = self.session.query(func.count(distinct(MT_TJ_LOGIN.login_id))).filter(MT_TJ_LOGIN.login_in >= cur_date(),
                                                                                                 MT_TJ_LOGIN.login_out==None).scalar()
            self.signalCount.emit(count_login,count_online)

            time.sleep(30)
            if self.count==30:
                self.count = 0
            else:
                self.count = self.count + 1
            # time.sleep(self.timer)

# 程序错误监控线程
class MonitorThread(QThread):

    # 定义信号,定义参数为str类型
    signalPost = pyqtSignal(str,str)     # 更新界面
    signalExit = pyqtSignal()

    def __init__(self,timer=1):
        super(MonitorThread, self).__init__()
        self.running = False
        self.timer = timer

    def stop(self):
        self.running = False

    def run(self):
        pass
        # observer = Observer()


class UpdateDialog(QDialog):

    sure_update = pyqtSignal()

    def __init__(self,parent=None):
        super(UpdateDialog,self).__init__(parent)
        self.setWindowIcon(Icon('mztj'))
        self.setWindowTitle('明州体检')
        self.setFixedSize(500,400)
        # self.setWindowFlags(Qt.FramelessWindowHint)  # 窗口模式，去掉标题栏
        self.initUI()
        self.setBackgroundImage()
        # 信号槽
        self.buttonBox.accepted.connect(self.on_btn_update)
        self.buttonBox.rejected.connect(self.reject)

    def initUI(self):
        lt_main = QVBoxLayout()
        ######## 更新内容 #########################
        self.gp_top = QGroupBox('更新内容')
        lt_top = QHBoxLayout()
        self.tb_up_describe = QTextBrowser()
        self.tb_up_describe.setStyleSheet('''font: 75 12pt '微软雅黑';color: rgb(0,128,0);''')
        lt_top.addWidget(self.tb_up_describe)
        self.gp_top.setLayout(lt_top)
        #### 按钮组
        self.buttonBox=QDialogButtonBox()
        self.buttonBox.addButton("更新",QDialogButtonBox.YesRole)
        self.buttonBox.addButton("取消", QDialogButtonBox.NoRole)
        self.buttonBox.setCenterButtons(True)
        # 添加布局
        lt_main.addWidget(self.gp_top)
        lt_main.addWidget(self.buttonBox)
        self.setLayout(lt_main)

    def setBackgroundImage(self):
        palette=QPalette()
        palette.setBrush(self.backgroundRole(), QBrush(QPixmap(file_ico("17_big.png"))))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

    def setDatas(self,version,describe):
        self.gp_top.setTitle('版本V%s：更新内容' %version)
        self.tb_up_describe.setPlainText('；\r\n'.join(describe.split('；')))

    def on_btn_update(self):
        self.sure_update.emit()


if __name__ == '__main__':
    pass
