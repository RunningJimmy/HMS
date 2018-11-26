from .report_equip_ui import *
from .model import *
from collections import OrderedDict
from utils import cur_datetime,cur_date

# 设备报告
class ReportEquip(ReportEquipUI):

    def __init__(self):
        super(ReportEquip, self).__init__()
        # 初始化必要数据
        self.initParas()
        self.table_report_equip.setContextMenuPolicy(Qt.CustomContextMenu)  ######允许右键产生子菜单
        self.table_report_equip.customContextMenuRequested.connect(self.onTableMenu)   ####右键菜单
        # 绑定信号槽
        self.btn_query.clicked.connect(self.on_btn_query_click)
        self.table_report_equip.itemClicked.connect(self.on_table_report_equip_click)
        # 按钮栏
        self.gp_quick_search.returnPressed.connect(self.on_quick_search)    # 快速检索
        self.gp_review_user.btnClick.connect(self.on_btn_audit_click)
        # 特殊变量，用于快速获取  含义：当前选择的体检编号、组合编号
        self.cur_tjbh = None
        self.cur_zhbh = None

    def initParas(self):
        self.dwmc_bh = OrderedDict()
        self.dwmc_py = OrderedDict()
        results = self.session.query(MT_TJ_DW).all()
        for result in results:
            self.dwmc_bh[result.dwbh] = str2(result.mc)
            self.dwmc_py[result.pyjm.lower()] = str2(result.mc)

        self.gp_where_search.s_dwbh.setValues(self.dwmc_bh,self.dwmc_py)
        self.equips = {
            '电测听':'0310',
            '人体成分':'5402',
            '骨密度':'501576',
            '超声骨密度':'1000074',
            '心电图':'0806'
        }

    # 右键功能
    def onTableMenu(self,pos):
        row_num = -1
        indexs=self.table_report_equip.selectionModel().selection().indexes()
        if indexs:
            for i in indexs:
                row_num = i.row()
        else:
            return
        menu = QMenu()
        item1 = menu.addAction(Icon("报告中心"), "修改检查医生")
        action = menu.exec_(self.table_report_equip.mapToGlobal(pos))
        if action == item1:
            text, ok = QInputDialog.getText(self, '明州体检', '请输入检查医生工号：', QLineEdit.Normal, '')
            if ok and text:
                tjbh = self.table_report_equip.getItemValueOfKey(row_num,'tjbh')
                cname = self.table_report_equip.getItemValueOfKey(row_num,'cname')
                result = self.session.query(MT_TJ_YGDM).filter(MT_TJ_YGDM.yggh == str(text)).scalar()
                if result:
                    # 更新数据库
                    try:
                        self.session.query(MT_TJ_EQUIP).filter(MT_TJ_EQUIP.tjbh==tjbh,MT_TJ_EQUIP.xmbh==self.equips.get(cname,'0000')).update(
                            {MT_TJ_EQUIP.operator:str(text),MT_TJ_EQUIP.operator2:str2(result.ygxm)}
                        )
                        self.session.commit()
                        mes_about(self,'修改成功！')
                    except Exception as e:
                        self.session.rollback()
                        mes_about(self, '插入 TJ_EQUIP 记录失败！错误代码：%s' % e)
                    # 刷新控件
                    self.table_report_equip.setItemValueOfKey(row_num,'jcys',str2(result.ygxm))
                else:
                    mes_about(self,'工号不存在，请确认后重新输入！')

    def on_btn_query_click(self):
        self.cur_tjbh = None
        self.cur_zhbh = None
        if self.gp_where_search.where_dwbh=='00000':
            mes_about(self,'不存在该单位，请重新选择！')
            return
        # 1、日期范围
        t_start,t_end = self.gp_where_search.date_range
        sql = get_equip_sql(t_start,t_end)
        # 2、单位编号
        dwbh = self.gp_where_search.where_dwbh
        if dwbh:
            sql = sql + " AND TJ_TJDJB.DWBH = '%s' " %dwbh
        # 关联项目表
        sql = sql + ''' INNER JOIN TJ_TJJLMXB ON TJ_TJDJB.TJBH=TJ_TJJLMXB.TJBH AND TJ_TJJLMXB.SFZH='0' '''
        # 3、设备编号
        equip_xmbh = self.cb_equip_type.get_equip_type2()
        if equip_xmbh:
            sql = sql + ''' AND ZHBH ='%s' ''' %equip_xmbh
        else:
            sql = sql + ''' AND ZHBH IN ('0806','5402','501576','1000074','0310') '''
        # 4、报告状态
        xmzt = self.cb_report_state.xmzt
        if xmzt:
            sql = sql + ''' AND TJ_TJJLMXB.jsbz='1' '''
        sql = sql + ''' LEFT JOIN TJ_EQUIP ON TJ_TJJLMXB.TJBH = TJ_EQUIP.TJBH AND TJ_TJJLMXB.ZHBH=TJ_EQUIP.XMBH ) '''
        sql = sql + ''' SELECT * FROM T1  '''
        # 5、检查医生
        if self.cb_user.where_user:
            sql = sql + ''' WHERE T1.JCYS='%s' ''' %self.cb_user.where_user

        sql = sql + ''' ORDER BY xmzt,cname,jcys,TJQY,jcrq '''
        results = self.session.execute(sql).fetchall()

        # 载入数据
        self.table_report_equip.load(results)
        self.gp_table.setTitle('检查列表（%s）' %self.table_report_equip.rowCount())
        mes_about(self,'共检索出 %s 条数据！' %self.table_report_equip.rowCount())

    # 预览报告
    # http://localhost:4001/web/viewer.html?file=\equip\2018\2018-08\2018-08-15\172960088_08.pdf
    def on_table_report_equip_click(self,QTableWidgetItem):
        row = QTableWidgetItem.row()
        # 获取变量
        fpath = self.table_report_equip.getLastItemValue(row)
        tjbh = self.table_report_equip.getItemValueOfKey(row, 'tjbh')
        cname = self.table_report_equip.getItemValueOfKey(row, 'cname')
        xm = self.table_report_equip.getItemValueOfKey(row, 'xm')
        xb = self.table_report_equip.getItemValueOfKey(row, 'xb')
        nl = self.table_report_equip.getItemValueOfKey(row, 'nl')
        xmzt = self.table_report_equip.getItemValueOfKey(row, 'xmzt')
        jcys = self.table_report_equip.getItemValueOfKey(row, 'jcys')
        jcrq = self.table_report_equip.getItemValueOfKey(row, 'jcrq')
        bgys = self.table_report_equip.getItemValueOfKey(row, 'bgys')
        bgrq = self.table_report_equip.getItemValueOfKey(row, 'bgrq')
        xmzd = self.table_report_equip.getItemValueOfKey(row, 'xmzd')
        dwmc = self.table_report_equip.getItemValueOfKey(row, 'dwmc')
        # 更新变量
        self.cur_tjbh = tjbh
        self.cur_zhbh = self.equips.get(cname,'0000')
        # 刷新控件
        self.gp_review_user.dataChanged.emit(xmzt,jcys,jcrq,bgys,bgrq,xmzd)
        self.gp_quick_search.setText(tjbh,xm)
        title = '体检编号：%s    姓名：%s   性别：%s   年龄：%s 岁     单位：%s' %(tjbh,xm,xb,nl,dwmc)
        self.gp_right.setTitle(title)
        # self.gp_review_user.setTitle(title)
        # self.gp_review_user.setStyleSheet('''font: 75 8pt '微软雅黑';''')
        # 刷新网页
        url = gol.get_value('api_equip_show','')
        if url:
            self.wv_report_equip.load(url %fpath)
            # self.wv_report_equip.show()
        else:
            mes_about(self,'未配置：api_equip_show 参数！')

    # 快速检索
    def on_quick_search(self, p1_str, p2_str):
        # 更新变量
        self.cur_tjbh = None
        self.cur_zhbh = None
        sql = get_equip_quick_sql()
        if p1_str == 'tjbh':
            sql = sql + ''' AND TJ_TJDJB.TJBH='%s' ''' %p2_str
        elif p1_str == 'xm':
            sql = sql + ''' AND TJ_TJDAB.XM='%s' ''' % p2_str
        else:
            return
        sql = sql + ''' INNER JOIN TJ_TJJLMXB ON TJ_TJDJB.TJBH=TJ_TJJLMXB.TJBH AND TJ_TJJLMXB.SFZH='0' AND ZHBH IN ('0806','5402','501576','1000074','0310') '''
        sql = sql + ''' LEFT JOIN TJ_EQUIP ON TJ_TJJLMXB.TJBH = TJ_EQUIP.TJBH AND TJ_TJJLMXB.ZHBH=TJ_EQUIP.XMBH ) '''
        sql = sql + ''' SELECT * FROM T1 ORDER BY xmzt,cname,jcys,TJQY,jcrq '''
        # print(sql)
        results = self.session.execute(sql).fetchall()
        self.table_report_equip.load(results)
        self.gp_table.setTitle('检查列表（%s）' % self.table_report_equip.rowCount())

    # 审核/取消审核
    def on_btn_audit_click(self,shzt:bool,xmzd:str):
        '''
        :param shzt: 审核/取消审核
        :param xmzd: 审核：项目诊断；取消审核：取消原因
        :return:
        '''
        if not self.cur_tjbh:
            mes_about(self,'请选择体检顾客！')
            return
        # 审核
        if shzt:
            # 更新TJ_TJJLMXB、TJ_EQUIP、TJ_CZJLB
            try:
                if self.cur_zhbh=='0806':
                    self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == self.cur_tjbh,
                                                             MT_TJ_TJJLMXB.zhbh==self.cur_zhbh
                                                             ).update(
                        {MT_TJ_TJJLMXB.jg: xmzd,
                         MT_TJ_TJJLMXB.zxpb: '1',
                         MT_TJ_TJJLMXB.jsbz: '1',
                         MT_TJ_TJJLMXB.qzjs: None,
                         MT_TJ_TJJLMXB.ycbz: '1',
                         MT_TJ_TJJLMXB.jcrq: cur_datetime(),
                         MT_TJ_TJJLMXB.jcys: self.login_id,
                         }
                    )
                else:
                    self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == self.cur_tjbh,
                                                             MT_TJ_TJJLMXB.zhbh==self.cur_zhbh
                                                             ).update(
                        {
                             MT_TJ_TJJLMXB.zd: xmzd,
                             MT_TJ_TJJLMXB.zxpb: '1',
                             MT_TJ_TJJLMXB.jsbz: '1',
                             MT_TJ_TJJLMXB.qzjs: None,
                             MT_TJ_TJJLMXB.ycbz: '1',
                             MT_TJ_TJJLMXB.jcrq: cur_datetime(),
                             MT_TJ_TJJLMXB.jcys: self.login_id,
                         }
                    )
                data_obj = {
                    'jllx': '0124', 'jlmc': '%s结果录入' % get_key(self.equips, self.cur_zhbh), 'tjbh': self.cur_tjbh,
                    'mxbh': self.cur_zhbh,'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
                    'jlnr': xmzd, 'bz': None}
                self.session.bulk_insert_mappings(MT_TJ_CZJLB, [data_obj])
                self.gp_review_user.statechange(self.login_name,cur_date())
                self.session.commit()
                mes_about(self,"审核完成！")
            except Exception as e:
                self.session.rollback()
                mes_about(self,"审核失败，错误信息：%s" %e)
                return

        # 取消审核
        else:
            bgys = self.table_report_equip.getCurItemValueOfKey('bgys')
            if self.login_name!=bgys:
                mes_about(self,'该报告不是您审核的，您没有权限修改！')
                return
            try:
                self.session.query(MT_TJ_TJJLMXB).filter(MT_TJ_TJJLMXB.tjbh == self.cur_tjbh,
                                                         MT_TJ_TJJLMXB.zhbh == self.cur_zhbh
                                                         ).update(
                    {
                         MT_TJ_TJJLMXB.zxpb: '0',
                         MT_TJ_TJJLMXB.jsbz: '0',
                         MT_TJ_TJJLMXB.qzjs: None,
                         MT_TJ_TJJLMXB.ycbz: '1',
                         MT_TJ_TJJLMXB.jcrq: None,
                         MT_TJ_TJJLMXB.jcys: None,
                     }
                )
                data_obj = {
                    'jllx': '0128', 'jlmc': '%s结果录入取消' %get_key(self.equips,self.cur_zhbh), 'tjbh': self.cur_tjbh, 'mxbh': self.cur_zhbh,
                    'czgh': self.login_id, 'czxm': self.login_name, 'czqy': self.login_area,
                    'jlnr': '%s报告取消审核' %get_key(self.equips,self.cur_zhbh), 'bz': xmzd}
                self.session.bulk_insert_mappings(MT_TJ_CZJLB,[data_obj])
                self.session.commit()
                self.gp_review_user.statechange()
                mes_about(self, "取消审核完成！")
            except Exception as e:
                self.session.rollback()
                mes_about(self,"取消审核失败，错误信息：%s" %e)
                return


def get_key(d, value):
    return [k for k,v in d.items() if v == value][0]

