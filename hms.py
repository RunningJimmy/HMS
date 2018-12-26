# Qt内嵌谷歌引擎BUG太多，实在是不好用->改用开源谷歌引擎  目前部分替换
from PyQt5.QtCore import PYQT_VERSION_STR,QCoreApplication,Qt,QProcess
# 判断版本号
if int(PYQT_VERSION_STR.replace('.',''))>=560:
    # 处理闪屏、黑屏问题 必须放在 Application 实例化前
    QCoreApplication.setAttribute(Qt.AA_UseSoftwareOpenGL)
else:
    from PyQt5.QtWebKit import *
    from PyQt5.QtWebKitWidgets import *
from multiprocessing import Process, Queue
import multiprocessing,requests,ctypes
from importlib import import_module
from utils.envir import *
from app_equip import equip_ui_run


# 主界面
def main_ui(ui,app):
    if gol.get_value('ui_show', 0) == 0:
        ui.showMaximized()
    elif gol.get_value('ui_show', 0) == 1:
        ui.showFullScreen()
    else:
        ui.show()
    app.exec_()

#
def equip_ui(ui,app):
    ui.show()
    app.exec_()

def start_run():
    from main import Login_UI
    from widgets import CefApplication
    try:
        from cefpython3 import cefpython as cef
    except Exception as e:
        ctypes.windll.user32.MessageBoxA(0, '动态库：cefpython3 载入失败！'.encode('gb2312'), '明州体检'.encode('gb2312'), 0)
        cef = None
    from PyQt5.QtWidgets import QSplashScreen
    from PyQt5.QtGui import QPixmap
    import sys
    ##########################################
    #app = QApplication(sys.argv)
    if cef:
        # sys.excepthook = cef.ExceptHook
        cef.Initialize()
    app = CefApplication(sys.argv)
    splash = QSplashScreen(QPixmap("login.png"))
    # 是否通过用户密码验证登陆
    if gol.get_value('system_is_login',1) == 1:
        login_ui = Login_UI()
        if login_ui.exec_():
            # 是否进入设备接口
            if gol.get_value('system_is_equip', 0) == 0:
                from main import TJ_Main_UI
                main_ui(TJ_Main_UI(), app)
            # 进入设备接口
            else:
                # 全局进程队列
                gol_process_queue = Queue()
                equip_ui_run(app,gol_process_queue,gol.get_value('equip_type', 0))

    # 不需要通过用户密码验证，直接进入主界面
    elif gol.get_value('system_is_login',1) == 0:
        from main import TJ_Main_UI
        main_ui(TJ_Main_UI(), app)
    # 进入自助机模式
    else:
        from app_selfhelp import SelfHelpMachine
        ui = SelfHelpMachine()
        main_ui(ui,app)
    if cef:
        cef.Shutdown()

def run_exe(module,function):
    module_class = getattr(import_module(module), function)
    module_class()

# 是否需要更新程序
def is_update(url,log):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 启动更新子进程
            process = QProcess()
            dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
            update_process_name = os.path.join(dirname,'autoupdate.exe')
            try:
                process.startDetached(update_process_name)
                print("准备更新程序，启动更新进程！")
                log.info("准备更新程序，启动更新进程！")
                sys.exit(0)
                # os._exit()
            except Exception as e:
                print("准备更新程序，启动更新进程失败，错误信息：%s" %e)
                log.info("准备更新程序，启动更新进程失败，错误信息：%s" %e)
                return
        else:
            return False
    except Exception as e:
        error = '%s' % e
        ctypes.windll.user32.MessageBoxA(0, error.encode('gb2312'), '明州体检'.encode('gb2312'), 0)
        return False


if __name__=="__main__":
    import cgitb
    # 非pycharm编辑器可用输出错误
    # sys.excepthook = cgitb.Hook(1, None, 5, sys.stderr, 'text')
    cgitb.enable(logdir="./error/",format="text")
    multiprocessing.freeze_support()
    # 启动主进程
    set_env()
    auto_update = gol.get_value('update_auto', True)
    if auto_update:
        # 是否自动更新
        sys_version = gol.get_value('system_version', 1.0)
        update_url = gol.get_value('system_update', "http://10.7.200.101:4009/api/version/%s/%s")
        log = gol.get_value('log')
        url = update_url %(get_system(),sys_version)
        is_update(url,log)
    # 增加全局异常处理
    start_run()



