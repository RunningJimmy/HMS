from collections import OrderedDict

#对象树,菜单栏->菜单->界面->按钮
#每个对象都有唯一ID、唯一父ID、不定子ID，标题title，提示tip，状态status,
SYS_MENU_TREE = {   # 系统
    'pid':None,
    'sid':1,
    'title':'体检系统',
    'tip':None,
    'state':True,
    'childs':OrderedDict([  # 菜单栏
        # 系统架构维护
        ('系统管理',
         {
            'pid':1,
            'sid':100,
            'title':'系统管理',
            'tip':None,
            'state':True,
            'childs':OrderedDict([  # 菜单
                ('用户管理',{'pid':100,'sid':1001,'title':'用户管理','tip':None,'state':True,'icon':'用户','is_tool':False,'shortcut':None}),
                ('角色权限',{'pid':100,'sid':1002,'title':'角色权限','tip':None,'state':True,'icon':'权限','is_tool':False,'shortcut':None}),
                ('密码修改',{'pid':100,'sid':1003,'title':'密码修改','tip':None,'state':True,'icon':'密码修改','is_tool':False,'shortcut':None}),
                ('系统日志',{'pid':100,'sid':1004,'title':'系统日志','tip':None,'state':True,'icon':'日志','is_tool':False,'shortcut':None}),
                ('系统参数',{'pid':100,'sid':1004,'title':'系统参数','tip':None,'state':True,'icon':'参数','is_tool':False,'shortcut':None}),
                ('代码字典',{'pid':100,'sid':1005,'title':'代码字典','tip':None,'state':True,'icon':'字典','is_tool':False,'shortcut':None}),
                ('版本更新',{'pid':100,'sid':1006,'title':'版本更新','tip':None,'state':True,'icon':'版本','is_tool':False,'shortcut':None}),
                ('界面设计',{'pid':100,'sid':1007,'title':'界面设计','tip':None,'state':True,'icon':'','is_tool':False,'shortcut':None}),
                ('注    销',{'pid':100,'sid':1007,'title':' 注  销 ','tip':None,'state':False,'icon':'注销','is_tool':False,'shortcut':None}),
                ('退    出',{'pid':100,'sid':1008,'title':' 退  出 ','tip':None,'state':True,'icon':'退出','is_tool':False,'shortcut':None})
            ])
         }),
        # 基础资料维护
        ('基础维护',
         {
             'pid': 1,
             'sid': 200,
             'title': '基础维护',
             'tip': None,
             'state': True,
             'childs': OrderedDict([
                  ('项目设置',{'pid': 200, 'sid': 2001, 'title': '项目设置', 'tip': None, 'state': True,'icon':'','is_tool':False,'shortcut': None}),
                  # ('体检套餐',{'pid': 200, 'id': 2002, 'title': '体检套餐', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
                  # ('体检项目类别',{'pid': 200, 'id': 2003, 'title': '体检项目类别', 'tip': None, 'state': True, 'icon':'','is_tool':False,'class':None,'childs': None}),
                  # ('导检单项目',{'pid': 200, 'id': 2004, 'title': '导检单项目', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
                  # ('导检单',{'pid': 200, 'id': 2005, 'title': '导检单', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
                  # ('员工信息',{'pid': 200, 'id': 2006, 'title': '员工信息', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
                  # ('体检科室',{'pid': 200, 'id': 2007, 'title': '体检科室', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
                  # ('发票号码',{'pid': 200, 'id': 2008, 'title': '发票号码', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None})
                  ('报告设置',{'pid': 200, 'sid': 2005, 'title': '报告设置', 'tip': None, 'state': True, 'icon':'报告中心','is_tool':False,'shortcut':None}),
                  ('接口配置', {'pid': 200, 'sid': 2008, 'title': '接口配置', 'tip': None, 'state': True, 'icon': '切换接口','is_tool': False, 'shortcut': None}),
                  ('其他配置', {'pid': 200, 'sid': 2009, 'title': '其他配置', 'tip': None, 'state': True, 'icon': '切换接口','is_tool': False, 'shortcut': None}),
            ])
         }),
        # 外围系统 WEB、app、微信、电话、短信、HIS、LIS、PACS
        # ('接口管理',
        #  {
        #      'pid': 1,
        #      'sid': 300,
        #      'title': '接口管理',
        #      'tip': None,
        #      'state': True,
        #      'childs': OrderedDict([
        #           #     ('HIS收费项目对照',
        #           #      {'pid': 400, 'id': 4001, 'title': 'HIS收费项目对照', 'tip': None, 'state': True, 'icon': '',
        #           #       'is_tool': False, 'class': None, 'childs': None}),
        #           #     ('LIS检验项目对照',
        #           #      {'pid': 400, 'id': 4002, 'title': 'LIS检验项目对照', 'tip': None, 'state': True, 'icon': '',
        #           #       'is_tool': False, 'class': None, 'childs': None}),
        #           #     ('PACS项目对照', {'pid': 400, 'id': 4003, 'title': 'PACS项目对照', 'tip': None, 'state': True, 'icon': '',
        #           #                   'is_tool': False, 'class': None, 'childs': None}),
        #           #     ('HIS接口',
        #           #      {'pid': 400, 'id': 4004, 'title': 'HIS接口', 'tip': None, 'state': True, 'icon': '', 'is_tool': False,
        #           #       'class': None, 'childs': None}),
        #           #     ('LIS接口',
        #           #      {'pid': 400, 'id': 4005, 'title': 'LIS接口', 'tip': None, 'state': True, 'icon': '', 'is_tool': False,
        #           #       'class': None, 'childs': None}),
        #           #     ('PACS接口', {'pid': 400, 'id': 4006, 'title': 'PACS接口', 'tip': None, 'state': True, 'icon': '',
        #           #                 'is_tool': False, 'class': None, 'childs': None}),
        #           #     ('设备接口',
        #           #      {'pid': 400, 'id': 4007, 'title': '设备接口', 'tip': None, 'state': True, 'icon': '', 'is_tool': False,
        #           #       'class': None, 'childs': None})
        #           ])}),
        # 体检检中管理
        ('检中管理',
         {
             'pid': 1,
             'sid': 400,
             'title': '检中管理',
             'tip': None,
             'state': True,
             'childs': OrderedDict([
             # ('体检预约',{'pid': 300, 'sid': 3001, 'title': '体检预约', 'tip': None, 'state': True, 'icon':'预约','is_tool':True,'shortcut':None}),
             ('体检登记',{'pid': 400, 'sid': 4002, 'title': '体检登记', 'tip': None, 'state': True, 'icon':'体检登记','is_tool':False,'shortcut':None}),
             # ('体检收费',{'pid': 300, 'sid': 3003, 'title': '体检收费', 'tip': None, 'state': True, 'icon':'收费','is_tool':True,'shortcut':None}),
                ('结果录入',{'pid': 400, 'sid': 4004, 'title': '结果录入', 'tip': None, 'state': True, 'icon':'结果录入','is_tool':False,'shortcut':None}),
             # ('医生总检',{'pid': 300, 'sid': 3005, 'title': '医生总检', 'tip': None, 'state': True, 'icon':'预约','is_tool':True,'shortcut':None}),
             # ('智能导检',{'pid': 300, 'sid': 3006, 'title': '智能导检', 'tip': None, 'state': False, 'icon':'导检','is_tool':True,'shortcut':None}),
             # ('短信平台',{'pid': 300, 'sid': 3007, 'title': '短信平台', 'tip': None, 'state': False, 'icon':'短信','is_tool':True,'shortcut':None})
                ('贵宾管理',{'pid': 400, 'sid': 4007, 'title': '贵宾管理', 'tip': None, 'state': True, 'icon':'贵宾管理','is_tool':True,'shortcut':None}),
                ('采血留样',{'pid': 400, 'sid': 4008, 'title': '采血台', 'tip': None, 'state': True, 'icon':'采血台','is_tool':True,'shortcut':None}),
                ('呼气试验',{'pid': 400, 'sid': 4009, 'title': '呼气室', 'tip': None, 'state': True, 'icon':'呼气室','is_tool':True,'shortcut':None}),
            ])}),
        # 体检检后管理
        ('检后管理',
         {
             'pid': 1,
             'sid': 500,
             'title': '检后管理',
             'tip': None,
             'state': True,
             'childs': OrderedDict([
                ('报告中心',{'pid': 500, 'sid': 5001, 'title': '报告中心', 'tip': None, 'state': True, 'icon':'报告中心','is_tool':True,'shortcut':None}),
                ('慢病管理',{'pid': 500, 'sid': 5002, 'title': '慢病管理', 'tip': None, 'state': True, 'icon':'慢病管理','is_tool':True,'shortcut':None}),
                ('希和检后',{'pid': 500, 'sid': 5003, 'title': '希和检后', 'tip': None, 'state': True, 'icon': '医生', 'is_tool': False,'shortcut':None}),
                ('台湾检后',{'pid': 500, 'sid': 5004, 'title': '台湾检后', 'tip': None, 'state': True, 'icon': '医生', 'is_tool': False,'shortcut':None}),
            ])}),
        # 管理人员 用到的
        ('主任平台',
         {
             'pid': 1,
             'sid': 600,
             'title': '主任平台',
             'tip': None,
             'state': True,
             'childs': OrderedDict([
                 ('医护绩效',{'pid': 600, 'sid': 6001, 'title': '医护绩效', 'tip': None, 'state': True,'icon':'','is_tool':False,'shortcut':None}),
                 ('体检时效',{'pid': 600, 'sid': 6002, 'title': '体检时效', 'tip': None, 'state': True,'icon':'','is_tool':False,'shortcut':None}),
            #    ('工作量',{'pid': 600, 'id': 6003, 'title': '工作量', 'tip': None, 'state': True,'icon':'缴费','is_tool':False,'shortcut':None}),
             # ('工作效率统计',{'pid': 500, 'id': 5003, 'title': '工作效率统计', 'tip': None, 'state': True,'icon':'','is_tool':False,'shortcut':None}),
             # ('日签到统计',{'pid': 500, 'id': 5004, 'title': '日签到统计', 'tip': None, 'state': True,'icon':'','is_tool':False,'shortcut':None}),
             # ('预约明细',{'pid': 500, 'id': 5005, 'title': '预约明细', 'tip': None, 'state': True,'icon':'','is_tool':False,'shortcut':None})
                 ('危急值上报',{'pid': 600, 'sid': 6008, 'title': '危急值上报', 'tip': None, 'state': True, 'icon': '', 'is_tool': False,'shortcut': None}),
                 ('不良事件上报',{'pid': 600, 'sid': 6009, 'title': '不良事件上报', 'tip': None, 'state': True, 'icon': '', 'is_tool': False,'shortcut': None}),
            ])}),
        # 自带财务模块
        # ('财务管理',
        #  {
        #      'pid': 1,
        #      'sid': 700,
        #      'title': '经营',
        #      'tip': None,
        #      'state': True,
        #      'childs': OrderedDict([
        #      # ('用户管理',{'pid': 600, 'id': 6001, 'title': '用户管理', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
        #      # ('权限管理',{'pid': 600, 'id': 6002, 'title': '权限管理', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
        #      # ('密码修改',{'pid': 600, 'id': 6003, 'title': '密码修改', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
        #      # ('系统参数',{'pid': 600, 'id': 6004, 'title': '系统参数', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
        #      # ('系统字典',{'pid': 600, 'id': 6005, 'title': '系统字典', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
        #      # ('系统版本',{'pid': 600, 'id': 6006, 'title': '系统版本', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
        #      # ('注销',{'pid': 600, 'id': 6007, 'title': '注销', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None}),
        #      # ('退出',{'pid': 600, 'id': 6008, 'title': '退出', 'tip': None, 'state': True,'icon':'','is_tool':False,'class':None, 'childs': None})
        #     ])}),
        # 数据统计 对所有人开放
        # ('查询统计',
        #  {
        #      'pid': 1,
        #      'sid': 800,
        #      'title': '查询统计',
        #      'tip': None,
        #      'state': True,
        #      'childs': OrderedDict([
        #          ('检查结果',{'pid': 800, 'sid': 8001, 'title': '检查结果', 'tip': None, 'state': True, 'icon': '', 'is_tool': False,'shortcut':None})
        #     ])})
        # 信息科 科室功能管理
        ('信息科',
         {
             'pid': 1,
             'sid': 900,
             'title': '信息科',
             'tip': None,
             'state': True,
             'childs': OrderedDict([
                 ('业务需求',{'pid': 900, 'sid': 9000, 'title': '业务需求', 'tip': None, 'state': True, 'icon': '填写率', 'is_tool': True,'shortcut':None}),
                 ('科室管理',{'pid': 900, 'sid': 9001, 'title': '科室管理', 'tip': None, 'state': True, 'icon': '所有科室', 'is_tool': False,'shortcut':None}),
                 ('电话平台',{'pid': 900, 'sid': 9002, 'title': '电话平台', 'tip': None, 'state': True, 'icon': '电话', 'is_tool': False,'shortcut':None}),
                 ('多媒体屏',{'pid': 900, 'sid': 9003, 'title': '多媒体屏', 'tip': None, 'state': True, 'icon': '多媒体', 'is_tool': False,'shortcut':None}),
                 ('微信后台',{'pid': 900, 'sid': 9004, 'title': '微信后台', 'tip': None, 'state': True, 'icon': 'website', 'is_tool': False,'shortcut':None}),
                 ('官网后台',{'pid': 900, 'sid': 9005, 'title': '官网后台', 'tip': None, 'state': True, 'icon': 'website', 'is_tool': False,'shortcut':None}),
                 ('官网主页',{'pid': 900, 'sid': 9006, 'title': '官网主页', 'tip': None, 'state': True, 'icon': 'website', 'is_tool': False,'shortcut':None}),
                 ('图特资产',{'pid': 900, 'sid': 9007, 'title': '图特资产', 'tip': None, 'state': True, 'icon': 'website','is_tool': False, 'shortcut': None}),
                 ('好评率',{'pid': 900, 'sid': 9008, 'title': '好评率', 'tip': None, 'state': True, 'icon': 'oa办公', 'is_tool': False,'shortcut':None}),
                 ('OA办公',{'pid': 900, 'sid': 9009, 'title': 'OA办公', 'tip': None, 'state': True, 'icon': 'oa办公', 'is_tool': False,'shortcut':None}),
            ])})
    ])
}
# 系统菜单模块对象
SYS_MENU_MODULE_CLASS = {
    1001: {'module': None, 'class': None, 'enabled': False},
    1002: {'module': None, 'class': None, 'enabled': False},
    1003: {'module': None, 'class': None, 'enabled': False},
    1004: {'module': None, 'class': None, 'enabled': False},
    1005: {'module': None, 'class': None, 'enabled': False},
    1006: {'module': None, 'class': None, 'enabled': False},
    1007: {'module': None, 'class': None, 'enabled': False},
    1008: {'module': None, 'class': None, 'enabled': False},
    2001: {'module': 'app_setup', 'class': 'SetupManagerItem', 'enabled': True},
    2002: {'module': None, 'class': None, 'enabled': False},
    2003: {'module': None, 'class': None, 'enabled': False},
    2004: {'module': None, 'class': None, 'enabled': False},
    2005: {'module': 'app_setup', 'class': 'SetupManagerReport', 'enabled': True},
    2006: {'module': None, 'class': None, 'enabled': False},
    2007: {'module': None, 'class': None, 'enabled': False},
    2008: {'module': 'app_setup', 'class': 'SetupManagerInterface', 'enabled': True},
    2009: {'module': 'app_setup', 'class': 'SetupManagerOther', 'enabled': True},
    3001: {'module': None, 'class': None, 'enabled': False},
    3002: {'module': None, 'class': None, 'enabled': False},
    3003: {'module': None, 'class': None, 'enabled': False},
    3004: {'module': None, 'class': None, 'enabled': False},
    3005: {'module': None, 'class': None, 'enabled': False},
    3006: {'module': None, 'class': None, 'enabled': False},
    3007: {'module': None, 'class': None, 'enabled': False},
    3008: {'module': None, 'class': None, 'enabled': False},
    4001: {'module': None, 'class': None, 'enabled': False},
    4002: {'module': 'register', 'class': "RegisterManager", 'enabled': True},
    4003: {'module': None, 'class': None, 'enabled': False},
    4004: {'module': 'result', 'class': 'ResultManager', 'enabled': True},
    4005: {'module': None, 'class': None, 'enabled': False},
    4006: {'module': None, 'class': None, 'enabled': False},
    4007: {'module': 'vip', 'class': 'VipManager', 'enabled': True},
    4008: {'module': 'lis', 'class': 'SampleManager', 'enabled': True},                 # 采血台
    4009: {'module': 'C13', 'class': 'BreathManager', 'enabled': True},                 # 呼气室
    5001: {'module': 'report', 'class': 'ReportManager', 'enabled': True},              # 报告中心
    5002: {'module': 'mbgl', 'class': 'NCDManager', 'enabled': True},                   # 慢病管理
    5003: {'module': 'app_interface', 'class': 'XiHe_HealthUI', 'enabled': True},       # 希和检后
    5004: {'module': 'app_interface', 'class': 'TaiWan_HealthUI', 'enabled': True},     # 台湾检后
    5005: {'module': None, 'class': None, 'enabled': False},
    5006: {'module': None, 'class': None, 'enabled': False},
    5007: {'module': None, 'class': None, 'enabled': False},
    5008: {'module': None, 'class': None, 'enabled': False},
    6001: {'module': 'statistics', 'class': 'DN_MeritPay', 'enabled': True},            # 医护绩效
    6002: {'module': 'statistics', 'class': 'TimeEfficency', 'enabled': True},          # 医护绩效
    6003: {'module': None, 'class': None, 'enabled': False},
    6004: {'module': None, 'class': None, 'enabled': False},
    6005: {'module': None, 'class': None, 'enabled': False},
    6006: {'module': None, 'class': None, 'enabled': False},
    6007: {'module': None, 'class': None, 'enabled': False},
    6008: {'module': 'app_interface', 'class': 'CriticalValueUI', 'enabled': True},
    6009: {'module': 'app_interface', 'class': 'AdverseEventUI', 'enabled': True},
    7001: {'module': None, 'class': None, 'enabled': False},
    7002: {'module': None, 'class': None, 'enabled': False},
    7003: {'module': None, 'class': None, 'enabled': False},
    7004: {'module': None, 'class': None, 'enabled': False},
    7005: {'module': None, 'class': None, 'enabled': False},
    7006: {'module': None, 'class': None, 'enabled': False},
    7007: {'module': None, 'class': None, 'enabled': False},
    7008: {'module': None, 'class': None, 'enabled': False},
    8001: {'module': None, 'class': None, 'enabled': False},
    8002: {'module': None, 'class': None, 'enabled': False},
    8003: {'module': None, 'class': None, 'enabled': False},
    8004: {'module': None, 'class': None, 'enabled': False},
    8005: {'module': None, 'class': None, 'enabled': False},
    8006: {'module': None, 'class': None, 'enabled': False},
    8007: {'module': None, 'class': None, 'enabled': False},
    8008: {'module': None, 'class': None, 'enabled': False},
    9000: {'module': 'app_interface', 'class': 'DemandManger', 'enabled': True},
    9001: {'module': 'app_interface', 'class': 'InfoManager', 'enabled': True},
    9002: {'module': 'app_interface', 'class': 'PhonePlatUI', 'enabled': True},
    9003: {'module': 'app_interface', 'class': 'MediaUI', 'enabled': True},
    9004: {'module': 'app_interface', 'class': 'WeiXinUI', 'enabled': True},
    9005: {'module': 'app_interface', 'class': 'WebsiteBackUI', 'enabled': True},
    9006: {'module': 'app_interface', 'class': 'WebsiteFrontUI', 'enabled': True},
    9007: {'module': 'app_interface', 'class': 'AssetUI', 'enabled': True},
    9008: {'module': 'app_interface', 'class': 'GoodEvaluateUI', 'enabled': True},
    9009: {'module': 'app_interface', 'class': 'OaUI', 'enabled': True},
}