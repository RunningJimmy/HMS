from .equip_ui import *
from .model import *
from .handle_parse import equip_file_parse,EquipNo,EquipName,EquipAction,EquipActionName

# 设备检查：
# 线程1：自动录入：开启与关闭与否
# 线程2：更新界面状态：已上传 默认检查中
class EquipInspect(EquipInspectUI):

    def __init__(self,queue,parent=None):
        '''
        :param queue: 跨进程队列
        :param parent: 父窗口
        '''
        super(EquipInspect,self).__init__(parent)
        # 自动录入功能
        self.le_tjbh.returnPressed.connect(self.on_le_tjbh_pressed)
        # 自动录入线程
        self.background_thread = None
        # 后台进程回传状态读取线程
        self.real_update_thread = EquipDataThread(queue)
        self.real_update_thread.signalPost.connect(self.update_state, type=Qt.QueuedConnection)
        self.real_update_thread.start()
        # 检查列表容器，用于快速定位某条码
        self.container_tjbhs = []
        # 绑定右键信号槽
        self.table_inspect.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.table_inspect.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单
        # 后台线程
        self.file_handle_thread = FileHandleThread(queue)
        self.equip_no = EquipNo.get(self.equip_type, '')

    # 右键功能
    def onTableMenu(self,pos):
        row_num = -1
        indexs=self.table_inspect.selectionModel().selection().indexes()
        if indexs:
            for i in indexs:
                row_num = i.row()

        menu = QMenu()
        # item1 = menu.addAction(Icon("报告中心"), "查看报告")
        item2 = menu.addAction(Icon("upload"), "本地上传")
        action = menu.exec_(self.table_inspect.mapToGlobal(pos))

        if action == item2:
            monitor_paths = gol.get_value('monitor_file_paths','')
            if monitor_paths:
                if not self.file_handle_thread.isRunning():
                    self.file_handle_thread.setTask(monitor_paths)
                    self.file_handle_thread.start()
                else:
                    mes_about(self,"正在处理，请勿重复操作！")
            else:
                mes_about(self,'未配置监控目录：monitor_file_paths')

    def update_state(self,p_tjbh):
        # 是否在容器中，较下面速度快
        # items = self.table_inspect.findItems(p_tjbh, Qt.MatchContains)
        if p_tjbh in self.container_tjbhs:
            self.table_inspect.item(self.container_tjbhs.index(p_tjbh), 0).setText('已上传')
            self.table_inspect.item(self.container_tjbhs.index(p_tjbh), 0).setBackground(QColor("#f0e68c"))
        else:
            # 如果不存在，则刷新界面
            try:
                result = self.session.query(MV_EQUIP_JCMX).filter(MV_EQUIP_JCMX.tjbh == p_tjbh,MV_EQUIP_JCMX.xmbh == self.equip_no).scalar()
                if result:
                    # 不存在则添加容器
                    self.container_tjbhs.append(p_tjbh)
                    # 刷新列表
                    self.table_inspect.insert3(result.to_dict)
                    self.table_inspect.selectRow(self.container_tjbhs.index(result.tjbh))
                    self.gp_middle.setTitle('检查列表（%s）' % str(self.table_inspect.rowCount()))
                else:
                    mes_about(self,'无法查询到体检编号：%s 的信息，请确认！' %p_tjbh)
            except Exception as e:
                mes_about(self,'网络异常，连接数据库失败,错误信息：%s' %e)

        # 删除整行变色
        # for col_index in range(self.table_inspect.columnCount()):
        #         self.table_inspect.item(self.container_tjbhs.index(p_tjbh), col_index).setBackground(QColor("#f0e68c"))

        # mes_about(self,'获得设备端数据：%s' %p_str)

    def on_le_tjbh_pressed(self):
        tjbh = self.le_tjbh.text()
        if  len(tjbh)==9:
            # 先判断项目是否完成
            result = self.session.query(MV_EQUIP_JCMX).filter(MV_EQUIP_JCMX.tjbh == tjbh, MV_EQUIP_JCMX.xmbh == self.equip_no).scalar()
            if result:
                # 更新界面
                self.on_table_insert(result)
                # 启动后台线程
                if self.cb_auto.isChecked():
                    if self.equip_no=='0806':
                        self.on_thread_start(tjbh)
            else:
                mes_about(self,'体检顾客：%s,无检查项目：%s ' %(tjbh,self.equip_no))

        else:
            mes_about(self, "请输入正确的体检编号！")

        self.tjbh.setText('')
        self.tjbh.setFocus(Qt.OtherFocusReason)

    # 刷新列表
    def on_table_insert(self,result):
        if result.tjbh in self.container_tjbhs:
            self.table_inspect.selectRow(self.container_tjbhs.index(result.tjbh))
        else:
            # 不存在则添加容器
            self.container_tjbhs.append(result.tjbh)
            # 刷新列表
            self.table_inspect.insert2(result.to_dict)
            self.table_inspect.selectRow(self.container_tjbhs.index(result.tjbh))
            self.gp_middle.setTitle('检查列表（%s）' % str(self.table_inspect.rowCount()))

    # 自动录入线程
    def on_thread_start(self,tjbh):
        if self.background_thread:
            self.background_thread.setStart(tjbh)
            self.background_thread.start()
        else:
            self.background_thread = BackGroundThread()
            self.background_thread.setStart(tjbh)
            self.background_thread.start()

    def closeEvent(self, *args, **kwargs):
        # 退出系统写入日志
        try:
            self.session.query(MT_TJ_LOGIN).filter(MT_TJ_LOGIN.login_id == self.login_id,
                                                   MT_TJ_LOGIN.lid == gol.get_value('login_lid',0)
                                                   ).update({
                MT_TJ_LOGIN.login_out:cur_datetime()
            })
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            mes_about(self, '退出系统记录日志，发生错误：%s' % e)
        # 关闭后台线程
        try:
            if self.background_thread:
                self.background_thread.stop()
                self.background_thread = None
            if self.real_update_thread:
                self.real_update_thread.stop()
                self.real_update_thread = None
        except Exception as e:
            self.log.info("关闭时发生错误：%s " %e)

        super(EquipInspect, self).closeEvent(*args, **kwargs)

# 后台线程 处理是否自动录入
class FileHandleThread(QThread):

    # 定义信号,定义参数为str类型
    signalPost = pyqtSignal(str)  # 更新界面
    signalExit = pyqtSignal()
    tjbh = None

    def __init__(self,queue):
        super(FileHandleThread, self).__init__()
        self.initParas()
        self.runing = False
        self.process_queue = queue

    def setTask(self,path):
        self.runing= True
        self.path =path

    def initParas(self):
        # 数据库链接
        self.session = gol.get_value('tjxt_session_local')
        # 日志
        self.log = gol.get_value('log')
        # 设备类型
        self.equip_type=str(gol.get_value('equip_type','00')).zfill(2)
        # 监控文件类型
        self.monitor_file_types = gol.get_value('monitor_file_types', ['.pdf', '.bmp', '.'])
        # 解析目录
        self.monitor_file_parse = gol.get_value('monitor_file_parse', 'D:/PDF/parse/')
        # 解析目录
        self.monitor_file_error = gol.get_value('monitor_file_error', 'D:/PDF/error/')
        # 是否删除原文件
        self.monitor_file_handle = gol.get_value('monitor_file_handle', True)
        # 监听后 等待多少秒后再处理
        self.monitor_file_sleep = gol.get_value('monitor_file_sleep', 2)
        # 上传文件请求地址
        self.url = gol.get_value('api_equip_upload','')
        # 登录用户信息
        self.login_id = gol.get_value('login_user_id', '')
        self.login_name = gol.get_value('login_user_name', '')
        self.login_area = gol.get_value('login_user_area', '')
        self.item_no = EquipNo.get(self.equip_type,'')
        self.host_name = gol.get_value('host_name', '')
        self.host_ip = gol.get_value('host_ip', '')
        # 设备记录表
        self.equip_info={
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

    def run(self):
        while self.runing:
            for filename,_ in fileiter(self.path):
                # 被监听文件：监听->解析->移动删除->上传
                equip_file_parse(filename,self.session,self.log,self.process_queue,
                                 self.login_id,self.login_name,self.login_area, self.host_name, self.host_ip,
                                 self.equip_type,self.url,self.item_no,self.czlj_info,self.equip_info,
                                 self.monitor_file_types,self.monitor_file_parse,self.monitor_file_error,self.monitor_file_handle)
            self.runing=False

# 后台线程 处理是否自动录入
class BackGroundThread(QThread):

    # 定义信号,定义参数为str类型
    signalPost = pyqtSignal(str)     # 更新界面
    signalExit = pyqtSignal()
    tjbh = None

    def __init__(self):
        super(BackGroundThread, self).__init__()
        self.session = gol.get_value('tjxt_session_thread')
        self.log = gol.get_value('log')
        self.running = False
        # 初始化 坐标
        self.pos = {}
        self.pos['position_tj'] = gol.get_value('position_tj')
        self.pos['position_tjbh'] = gol.get_value('position_tjbh')
        self.pos['position_xm'] = gol.get_value('position_xm')
        self.pos['position_xb1'] = gol.get_value('position_xb1')
        self.pos['position_xb2'] = gol.get_value('position_xb2')
        self.pos['position_nl'] = gol.get_value('position_nl')
        self.pos['position_sure'] = gol.get_value('position_sure')
        self.pos['position_gx'] = gol.get_value('position_gx')
        self.pos['position_cj'] = gol.get_value('position_cj')

    def stop(self):
        self.running = False

    # 传递体检编号
    def setStart(self,tjbh):
        self.tjbh = tjbh
        self.running = True

    def run(self):
        while self.running:
            try:
                if self.tjbh:
                    result = self.session.execute(get_tjxx_sql(self.tjbh)).first()
                    if result:
                        tmp = {}
                        tmp['tjbh'] = result[0]
                        tmp['xm'] = str2(result[1])
                        tmp['xb'] = str2(result[2])
                        tmp['nl'] = str(result[3])
                        autoInputXDT(tmp,self.pos)
                        self.log.info('体检编号：%s,自动录入成功！' %self.tjbh)
            except Exception as e:
                self.log.info('体检编号：%s,自动录入失败,错误信息：%s' % (self.tjbh, e))
            self.running = False
            self.tjbh = None
