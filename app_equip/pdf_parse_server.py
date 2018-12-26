from watchdog.events import FileSystemEventHandler
from watchdog.observers.read_directory_changes import WindowsApiObserver as Observer
from app_equip.handle_parse import *
from utils.envir_equip import set_equip_env
from utils.api import *

# 重大更新说明：
# 2017-09-01 0.1  新增设备接口，增加设备：骨密度、心电图、电测听、大便仪、超声骨密度、C13/14
# 2018-05-01 0.2  重构设备接口，外出联网，增加设备：DR放射、肺功能（COM）
# 2018-07-26 0.3  重构设备接口
    # 1、增加 PDF转Pic功能；
    # 2、增加绩效、归档、日志补充 TJ_CZJLB,TJ_FILE_ACTIVE；
    # 3、HTTP上传取代SMB上传方式；
# 2018-09-20 0.31  增加设备接口：人体成分（特殊版）图像识别功能，调用百度API进行识别解析体检编号，(Tesseract-OCR 识别率低，放弃本地识别模式)
# 2018-12-20 0.40  重构并解耦模块：PDF处理模块(业务无关)，文本处理模块(关联具体PDF格式)，数据库处理模块，根据业务形态组合封装API，方便其他模块调用

# 监听文件生成，解析，上传
class MonitorHandler(FileSystemEventHandler):

    def __init__(self,queue=None):
        super(MonitorHandler, self).__init__()
        self.process_queue = queue
        self.initParas()

    def initParas(self):
        # 数据库链接
        self.session = gol.get_value('tjxt_session_local')
        # 日志
        self.log = gol.get_value('parse_log')
        # 设备类型
        self.equip_type=str(gol.get_value('equip_type','00')).zfill(2)
        # 监控文件类型
        self.monitor_file_types = gol.get_value('monitor_file_types', ['.pdf', '.bmp', '.'])
        # 解析目录
        self.monitor_file_parse = gol.get_value('monitor_file_parse', 'D:/PDF/parse/')
        mkdir(self.monitor_file_parse,self.log)
        # 解析目录
        self.monitor_file_error = gol.get_value('monitor_file_error', 'D:/PDF/error/')
        mkdir(self.monitor_file_error, self.log)
        # 是否删除原文件
        self.monitor_file_handle = gol.get_value('monitor_file_handle', True)
        # 监听后 等待多少秒后再处理
        self.monitor_file_sleep = gol.get_value('monitor_file_sleep', 2)
        # 上传文件请求地址
        self.url = gol.get_value('api_equip_upload','')
        # 登录用户信息
        self.login_id = gol.get_value('login_user_id', '')
        self.login_name = gol.get_value('login_user_name', '')
        self.login_area = gol.get_value('login_area', '')
        self.item_no = EquipNo.get(self.equip_type,'')
        self.host_name = gol.get_value('host_name', '')
        self.host_ip = gol.get_value('host_ip', '')
        # 设备记录表
        self.equip_info={
                    'tjbh': '',
                    'equip_type':self.equip_type,
                    'equip_name':EquipName.get(self.equip_type,''),
                    'xmbh': self.item_no,
                    'hostname':self.host_name,
                    'hostip':self.host_ip,
                    'operator':self.login_id,
                    'operator2': self.login_name,
                    'operate_area': self.login_area
                }
        # 操作记录表
        self.czlj_info = {
            'jllx': EquipAction.get(self.equip_type,''),
            'jlmc': EquipActionName.get(self.equip_type,''),
            'tjbh': '',
            'mxbh': self.item_no,
            'czgh': self.login_id,
            'czxm': self.login_name,
            'czsj':'',
            'czqy': self.login_area
        }

    # 文件创建事件
    def on_created(self, event):
        filename = event.src_path
        self.log.info("文件：%s 监听到，等待%s秒后进行处理！" %(filename,self.monitor_file_sleep))
        print("文件：%s 监听到，等待%s秒后进行处理！" %(filename,self.monitor_file_sleep))
        time.sleep(self.monitor_file_sleep)
        # 被监听文件：监听->解析->移动删除->上传
        equip_file_parse(filename,self.session,self.log,self.process_queue,
                         self.login_id,self.login_name,self.login_area, self.host_name, self.host_ip,
                         self.equip_type,self.url,self.item_no,self.czlj_info,self.equip_info,
                         self.monitor_file_types,self.monitor_file_parse,self.monitor_file_error,self.monitor_file_handle)

# 运行监控服务
def pdf_parse_run(queue=None):
    import cgitb
    cgitb.enable(logdir="./error/",format="text")
    set_equip_env(False)
    log = gol.get_value('parse_log')
    monitor_file_paths = gol.get_value('monitor_file_paths', 'C:/')
    monitor_polling_timer = gol.get_value('monitor_polling_timer', 2)
    observer = Observer()
    event_handler = MonitorHandler(queue)
    if isinstance(monitor_file_paths,list):
        for file_path in monitor_file_paths:
            if mkdir(file_path,log):
                observer.schedule(event_handler, file_path, True)
    else:
        if mkdir(monitor_file_paths,log):
            observer.schedule(event_handler, monitor_file_paths, True)

    observer.start()
    try:
        while True:
            time.sleep(monitor_polling_timer)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == '__main__':
    pdf_parse_run()