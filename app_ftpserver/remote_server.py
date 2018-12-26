# 导入该模块
from socketserver import StreamRequestHandler,ThreadingTCPServer
import time
import win32gui, win32ui, win32con, win32api

def window_capture(filename):
    hwnd = 0  # 窗口的编号，0号表示当前活跃窗口
    # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根据窗口的DC获取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC创建可兼容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 创建bigmap准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    # 获取监控器信息
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    # print w,h　　　#图片大小
    # 为bitmap开辟空间
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，将截图保存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 截取从左上角（0，0）长宽为（w，h）的图片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)


class RemoteDesktopServer(StreamRequestHandler):

    def handle(self):
        # 打印客户端地址和端口
        print('新连接:', self.client_address)
        # 循环
        while True:
            # 接收客户发送的数据
            data = self.request.recv(1024)
            if not data: break  # 如果接收数据为空就跳出，否则打印
            print('Client data:', data.decode())

            beg = time.time()
            for i in range(10):
                filename = "%s.jpg" % str(i)
                window_capture(filename)
                with open(filename, "rb") as f:
                    self.request.send(f.read())  # 将收到的信息再发送给客户端
            end = time.time()
            print(end - beg)


if __name__ == "__main__":
    host, port = "10.7.103.205", 9000  # 定义服务器地址和端口
    server = ThreadingTCPServer((host, port), RemoteDesktopServer)  # 实现了多线程的socket通话
    server.serve_forever()  # 不会出现在一个客户端结束后，当前服务器端就会关闭或者报错，而是继续运行，与其他的客户端继续进行通话。