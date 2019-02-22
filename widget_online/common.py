'''
@author: zhufd
@license: (C) Copyright 明州体检
@contact: 13736093855
@software: HMS
@file: common.py
@time: 2019-2-20 13:37
@version：0.1
@desc: 在线业务，窗口自带数据库连接属性
'''
from widget_custom import *
from utils import GolParasMixin,PacsGolParasMixin,PisGolParasMixin,LisGolParasMixin

# 窗口带日志、登录信息、数据库链接功能
class Widget(GolParasMixin,QWidget):

    def __init__(self,parent=None):
        super(Widget,self).__init__(parent)
        self.init()

# 分隔窗口带日志、登录信息、数据库链接功能
class SplitWidget(GolParasMixin, QSplitter):

    def __init__(self, parent=None):
        super(SplitWidget, self).__init__(parent)
        self.init()

# 中央窗口带日志、登录信息、数据库链接功能，每次只能打开一个界面
class CenterWidget(GolParasMixin, QWidget):

    status = False

    def __init__(self, parent=None):
        super(CenterWidget, self).__init__(parent)
        self.init()

    def closeEvent(self, *args, **kwargs):
        super(CenterWidget,self).closeEvent(*args, **kwargs)
        self.status=True

# 窗口带日志、登录信息、数据库链接功能
class Dialog(GolParasMixin, QDialog):
    def __init__(self, parent=None):
        super(Dialog, self).__init__(parent)
        self.init()

# 窗口带日志、登录信息、数据库链接功能
class PacsWidget(PacsGolParasMixin, QWidget):
    def __init__(self, parent=None):
        super(PacsWidget, self).__init__(parent)
        self.init()

# 检查窗口带日志、登录信息、数据库链接功能
class PacsDialog(PacsGolParasMixin, QDialog):
    def __init__(self, parent=None):
        super(PacsDialog, self).__init__(parent)
        self.init()

# 病理窗口带日志、登录信息、数据库链接功能
class PisDialog(PisGolParasMixin, QDialog):
    def __init__(self, parent=None):
        super(PisDialog, self).__init__(parent)
        self.init()

# 检验窗口带日志、登录信息、数据库链接功能
class LisDialog(LisGolParasMixin, QDialog):
    def __init__(self, parent=None):
        super(LisDialog, self).__init__(parent)
        self.init()


# 绑定一组UI控件和对应模型，实现增删改查功能
class SqlModelHandle(object):

    def __init__(self,model,session,mapper):
        '''
        :param model: 模型，sqlalchemy中模型
        :param session: sqlalchemy.orm.Session
        :param mapper: 关联字典，绑定模型与UI控件一一对应
        :return:
        '''
        self.db_model = model
        self.db_session = session
        self.ui_mapper = mapper

    # 添加数据
    def insert(self):
        # 实例化对象
        model_obj = self.db_model()
        for key,widget in self.ui_mapper.items():
            if hasattr(self.db_model, key):
                col_obj = getattr(self.db_model, key)
                col_vue = widget_get_value(widget)
                # 是否为空与UI空值比较
                if any([col_obj.nullable,col_vue]):
                    setattr(model_obj, key, col_vue)
                # 是否自增长
                elif col_obj.autoincrement == True:
                    pass
                # 是否默认值
                elif col_obj.server_default:
                    pass
                else:
                    # print(col_obj.name,col_obj.nullable,"列：%s 不能为空！" %key)
                    return False, "列：%s 不能为空！" %key

        self.db_session.add(model_obj)
        return self.commit()

    # 删除数据
    def delete(self):
        # 删除条件 根据关键字
        where_str = {}
        for key,widget in self.ui_mapper.items():
            if hasattr(self.db_model, key):
                col_obj = getattr(self.db_model, key)
                col_vue = widget_get_value(widget)
                if col_obj.primary_key:
                    where_str[col_obj.name] = col_vue
        # 传入参数
        self.db_session.query(self.db_model).filter_by(**where_str).delete()
        return self.commit()

    # 查询数据
    def select(self):
        pass

    # 更新数据
    def update(self):
        # 更新条件 根据关键字
        where_str = {}
        update_str = {}
        for key,widget in self.ui_mapper.items():
            if hasattr(self.db_model, key):
                col_obj = getattr(self.db_model, key)
                col_vue = widget_get_value(widget)
                if col_obj.primary_key:
                    where_str[col_obj.name] = col_vue
                else:
                    update_str[col_obj.name] = col_vue
        model_obj = self.db_session.query(self.db_model).filter_by(**where_str).first()
        update = {setattr(model_obj, k, v) for k,v in update_str.items()}
        return self.commit()

    # 提交数据库
    def commit(self):
        try:
            self.db_session.commit()
            return True, ''
        except Exception as e:
            self.db_session.rollback()
            return False, "%s" %e

    # 处理入口
    def handle(self,action):
        '''
        :param action:insert/update/delete
        :return:
        '''
        if hasattr(self, action):
            return getattr(self, action)()
        else:
            return False,"类SqlModelHandle未定义方法：%s" %action