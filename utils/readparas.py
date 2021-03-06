from utils import gol


class GolParasMixin(object):

    def init(self):
        try:
            self.tmp_file = gol.get_value('path_tmp')
            self.log = gol.get_value('log','')
            self.session = gol.get_value('tjxt_session_local','')
            self.login_id = gol.get_value('login_user_id','')
            self.login_name = gol.get_value('login_user_name','')
            self.login_time = gol.get_value('login_time','')
            self.login_area = gol.get_value('login_area', '')
            self.api_host = gol.get_value('api_host','')
            self.api_port = gol.get_value('api_port', '')
        except Exception as e:
            self.log = ''
            self.session = ''
            self.login_id = ''
            self.login_name = ''
            self.login_time = ''
            self.login_area = ''

    # 获取全局参数名称
    def get_gol_para(self,para_name):
        return gol.get_value(para_name,'')


class PacsGolParasMixin(object):

    def init(self):
        try:
            self.tmp_file = gol.get_value('path_tmp')
            self.log = gol.get_value('log','')
            self.session = gol.get_value('tjxt_session_local', '')
            self.session_pacs = gol.get_value('pacs_session','')
            self.login_id = gol.get_value('login_user_id','')
            self.login_name = gol.get_value('login_user_name','')
            self.login_time = gol.get_value('login_time','')
            self.login_area = gol.get_value('login_area', '')
            self.api_host = gol.get_value('api_host','')
            self.api_port = gol.get_value('api_port', '')
        except Exception as e:
            self.log = ''
            self.session = ''
            self.login_id = ''
            self.login_name = ''
            self.login_time = ''
            self.login_area = ''

class PisGolParasMixin(object):

    def init(self):
        try:
            self.tmp_file = gol.get_value('path_tmp')
            self.log = gol.get_value('log','')
            self.session = gol.get_value('tjxt_session_local', '')
            self.session_pis = gol.get_value('pis_session','')
            self.login_id = gol.get_value('login_user_id','')
            self.login_name = gol.get_value('login_user_name','')
            self.login_time = gol.get_value('login_time','')
            self.login_area = gol.get_value('login_area', '')
            self.api_host = gol.get_value('api_host','')
            self.api_port = gol.get_value('api_port', '')
        except Exception as e:
            self.log = ''
            self.session = ''
            self.login_id = ''
            self.login_name = ''
            self.login_time = ''
            self.login_area = ''

class LisGolParasMixin(object):

    def init(self):
        try:
            self.tmp_file = gol.get_value('path_tmp')
            self.log = gol.get_value('log','')
            self.session = gol.get_value('tjxt_session_local', '')
            self.session_lis = gol.get_value('lis_session','')
            self.login_id = gol.get_value('login_user_id','')
            self.login_name = gol.get_value('login_user_name','')
            self.login_time = gol.get_value('login_time','')
            self.login_area = gol.get_value('login_area', '')
            self.api_host = gol.get_value('api_host','')
            self.api_port = gol.get_value('api_port', '')
        except Exception as e:
            self.log = ''
            self.session = ''
            self.login_id = ''
            self.login_name = ''
            self.login_time = ''
            self.login_area = ''