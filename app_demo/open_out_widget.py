'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: open_out_widget.py
@time: 2019-2-12 15:20
@version：0.1
@desc: 
'''

import os,time
import psutil
import win32con
import win32gui
import win32process
import win32api
from functools import partial,wraps
from pywinauto import findwindows
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QProcess
from PyQt5.QtGui import QWindow

# from pywinauto import application
# app = application.Application.start('notepad.exe')
# """
# 在函数执行出现异常时自动重试的简单装饰器
# """
class StopRetry(Exception):

    def __repr__(self):
        return 'retry stop'

def retry(max_retries: int =5, delay: (int, float) =0, step: (int, float) =0,
          exceptions: (BaseException, tuple, list) =BaseException,
          sleep=time.sleep, callback=None, validate=None):
    """
    函数执行出现异常时自动重试的简单装饰器。
    :param max_retries:  最多重试次数。
    :param delay:  每次重试的延迟，单位秒。
    :param step:  每次重试后延迟递增，单位秒。
    :param exceptions:  触发重试的异常类型，单个异常直接传入异常类型，多个异常以tuple或list传入。
    :param sleep:  实现延迟的方法，默认为time.sleep。
    在一些异步框架，如tornado中，使用time.sleep会导致阻塞，可以传入自定义的方法来实现延迟。
    自定义方法函数签名应与time.sleep相同，接收一个参数，为延迟执行的时间。
    :param callback: 回调函数，函数签名应接收一个参数，每次出现异常时，会将异常对象传入。
    可用于记录异常日志，中断重试等。
    如回调函数正常执行，并返回True，则表示告知重试装饰器异常已经处理，重试装饰器终止重试，并且不会抛出任何异常。
    如回调函数正常执行，没有返回值或返回除True以外的结果，则继续重试。
    如回调函数抛出异常，则终止重试，并将回调函数的异常抛出。
    :param validate: 验证函数，用于验证执行结果，并确认是否继续重试。
    函数签名应接收一个参数，每次被装饰的函数完成且未抛出任何异常时，调用验证函数，将执行的结果传入。
    如验证函数正常执行，且返回False，则继续重试，即使被装饰的函数完成且未抛出任何异常。
    如回调函数正常执行，没有返回值或返回除False以外的结果，则终止重试，并将函数执行结果返回。
    如验证函数抛出异常，且异常属于被重试装饰器捕获的类型，则继续重试。
    如验证函数抛出异常，且异常不属于被重试装饰器捕获的类型，则将验证函数的异常抛出。
    :return: 被装饰函数的执行结果。
    """
    def wrapper(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            nonlocal delay, step, max_retries
            func_ex = StopRetry
            while max_retries > 0:
                try:
                    result = func(*args, **kwargs)
                    # 验证函数返回False时，表示告知装饰器验证不通过，继续重试
                    if callable(validate) and validate(result) is False:
                        continue
                    else:
                        return result
                except exceptions as ex:
                    # 回调函数返回True时，表示告知装饰器异常已经处理，终止重试
                    if callable(callback) and callback(ex) is True:
                        return
                    func_ex = ex
                finally:
                    max_retries -= 1
                    if delay > 0 or step > 0:
                        sleep(delay)
                        delay += step
            else:
                raise func_ex
        return _wrapper
    return wrapper

def open_local_pdf(filename):
    cmd_exe = "acrord32.exe"
    # cmd_exe = r"C:\Users\Administrator\AppData\Local\Kingsoft\WPS Office\11.1.0.8214\office6\wps.exe"
    cmd_exe = "C:\Program Files\Microsoft Office\Office12\WINWORD.EXE"
    win32api.ShellExecute(0, 'open', cmd_exe, filename, '', 2)
    #hwnd = win32api.WinExec(cmd_exe,0)

    # ShellExecute(
    #   hWnd: HWND;        {指定父窗口句柄}
    #   Operation: PChar;  {指定动作, 譬如: open、print}
    #   FileName: PChar;   {指定要打开的文件或程序}
    #   Parameters: PChar; {给要打开的程序指定参数; 如果打开的是文件这里应该是 nil}
    #   Directory: PChar;  {缺省目录}
    #   ShowCmd: Integer   {打开选项}
    # ): HINST;            {执行成功会返回应用程序句柄; 如果这个值 <= 32, 表示执行错误}

    #//返回值可能的错误有:
    #                        = 0   {内存不足}
    # ERROR_FILE_NOT_FOUND   = 2;  {文件名错误}
    # ERROR_PATH_NOT_FOUND   = 3;  {路径名错误}
    # ERROR_BAD_FORMAT       = 11; {EXE 文件无效}
    # SE_ERR_SHARE           = 26; {发生共享错误}
    # SE_ERR_ASSOCINCOMPLETE = 27; {文件名不完全或无效}
    # SE_ERR_DDETIMEOUT      = 28; {超时}
    # SE_ERR_DDEFAIL         = 29; {DDE 事务失败}
    # SE_ERR_DDEBUSY         = 30; {正在处理其他 DDE 事务而不能完成该 DDE 事务}
    # SE_ERR_NOASSOC         = 31; {没有相关联的应用程序}

    # ShowCmd 参数可选值:
    # SW_HIDE            = 0;  {隐藏}
    # SW_SHOWNORMAL      = 1;  {用最近的大小和位置显示, 激活}
    # SW_NORMAL          = 1;  {同 SW_SHOWNORMAL}
    # SW_SHOWMINIMIZED   = 2;  {最小化, 激活}
    # SW_SHOWMAXIMIZED   = 3;  {最大化, 激活}
    # SW_MAXIMIZE        = 3;  {同 SW_SHOWMAXIMIZED}
    # SW_SHOWNOACTIVATE  = 4;  {用最近的大小和位置显示, 不激活}
    # SW_SHOW            = 5;  {同 SW_SHOWNORMAL}
    # SW_MINIMIZE        = 6;  {最小化, 不激活}
    # SW_SHOWMINNOACTIVE = 7;  {同 SW_MINIMIZE}
    # SW_SHOWNA          = 8;  {同 SW_SHOWNOACTIVATE}
    # SW_RESTORE         = 9;  {同 SW_SHOWNORMAL}
    # SW_SHOWDEFAULT     = 10; {同 SW_SHOWNORMAL}
    # SW_MAX             = 10; {同 SW_SHOWNORMAL}

    return os.path.basename(filename)

# 连接指定应用程序
@retry(max_retries=1000000,delay=0.1,exceptions=WindowsError)
def find_window_hwnd(window_title):
    try:
        #hwnd = findwindows.find_window(class_name="AcrobatSDIWindow",title_re=window_title)    #PDF
        return findwindows.find_window(title_re=window_title)
    except Exception as e:
        print('执行窗口连接：%s 失败！' % window_title)
        raise WindowsError

# 根据进程ID 获得进程名字
def get_pname_by_pid(pid:int):
    process_objs = psutil.process_iter()
    pnames = []
    for process_obj in process_objs:
        if process_obj.pid == pid:
            pnames.append(process_obj.name())
    return pnames

class OutWidget(QWidget):

    def __init__(self):
        super(OutWidget,self).__init__()
        lt_main = QVBoxLayout()
        self.resize(600,600)
        lt_top = QHBoxLayout()
        file1 = r"C:\Users\Administrator\Desktop\pdf测试\职业病表结构.doc"
        file2 = r"E:\DR\pdf\2018\2018-12\2018-12-06\108261638\108261638.pdf"
        self.btn_open1 = QPushButton("载入文件1")
        self.btn_open2 = QPushButton("载入文件2")
        self.btn_open1.clicked.connect(partial(self.on_btn_open_click, file1))
        self.btn_open2.clicked.connect(partial(self.on_btn_open_click, file2))
        self.btn_close = QPushButton("释放")
        self.btn_close.clicked.connect(self.on_btn_close_click)
        lt_top.addWidget(self.btn_open1)
        lt_top.addWidget(self.btn_open2)
        lt_top.addWidget(self.btn_close)
        # lt_main.addStretch()
        lt_main.addLayout(lt_top)
        self.setLayout(lt_main)
        self.cur_hwnd = None

    def on_btn_open_click(self,filename):
        self.on_btn_close_click()
        # hwnd = find_window_hwnd(open_local_pdf(filename))
        # win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        self.cur_hwnd = find_window_hwnd(open_local_pdf(filename))
        # 嵌入之前的属性
        # style = win32gui.GetWindowLong(self.cur_hwnd, win32con.GWL_STYLE)
        # exstyle = win32gui.GetWindowLong(self.cur_hwnd, win32con.GWL_EXSTYLE)
        widget = QWidget.createWindowContainer(QWindow.fromWinId(self.cur_hwnd))
        widget.hwnd = self.cur_hwnd  # 窗口句柄
        widget.phwnd = 0             # 父窗口句柄
        widget.style = win32gui.GetWindowLong(self.cur_hwnd, win32con.GWL_STYLE)  # 窗口样式
        widget.exstyle = win32gui.GetWindowLong(self.cur_hwnd, win32con.GWL_EXSTYLE)  # 窗口额外样式
        self.layout().addWidget(widget)

    def on_btn_close_click(self):
        if not self.cur_hwnd:
            return
        process_obj = QProcess()
        thread, processId = win32process.GetWindowThreadProcessId(self.cur_hwnd)
        pnames = get_pname_by_pid(processId)
        for pname in pnames:
            process_obj.execute("taskkill /im %s /f" %pname)
        process_obj.close()

    def closeEvent(self, QCloseEvent):
        self.on_btn_close_click()
        super(OutWidget,self).close()

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    w = OutWidget()
    w.show()
    sys.exit(app.exec_())

