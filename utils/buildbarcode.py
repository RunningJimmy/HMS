from barcode.writer import ImageWriter
from barcode.codex import Code39,Code128
from pystrich.code128 import Code128Encoder
import os

class BarCodeBuild(object):

    lis_alter_option = {
       "module_width":0.08,      # 条形码模块宽度：浮点数。默认值为0.2 单位为毫米
       "module_height":6,       # 条形码模块高度：为浮点。默认值为15  单位为毫米
       "quiet_zone":0.8,          # 左、右边的距离，从边界到第一个（最后）条形码模块，以M为浮点。默认值为6.5。 单位为毫米
       "font_size":10,          # 在PT下的文本大小为整数。默认值为10 文本字体大小，单位为磅
       "text_distance": 1,    # 条形码与它下面的文本之间的距离为浮点。默认值为5。 单位为毫米
       "center_text":True,      # 条形码下面文本是否居中
       "text":"测试",
       "background":'goldenrod', # 创建的条形码的背景颜色为字符串。默认为白色 white
       "foreground":'white'     # 创建的条形码的前景颜色为字符串。默认为黑色 black
    }

    # 采血台，创建条码
    lis_create_option = {
       "module_width":0.08,      # 条形码模块宽度：浮点数。默认值为0.2
       "module_height":6,       # 条形码模块高度：为浮点。默认值为15
       "quiet_zone":0.8,       # 左、右边的距离，从边界到第一个（最后）条形码模块，以M为浮点。默认值为6.5。
       "font_size":10,          # 在PT下的文本大小为整数。默认值为10
       "text_distance": 1,    # 条形码与它下面的文本之间的距离为浮点。默认值为5。
       "center_text":True,      # 条形码下面文本是否居中
       "write_text":True,
       "text":"测试",
       "background":'white',    # 创建的条形码的背景颜色为字符串。默认为白色 white
       "foreground":'black'     # 创建的条形码的前景颜色为字符串。默认为黑色 black
    }

    option3 = {
               "module_width":0.15,      # 条形码模块宽度：浮点数。默认值为0.2
               "module_height":6,       # 条形码模块高度：为浮点。默认值为15
               "quiet_zone":0.8,          # 左、右边的距离，从边界到第一个（最后）条形码模块，以M为浮点。默认值为6.5。
               "font_size":12,          # 在PT下的文本大小为整数。默认值为10
               "text_distance": 0.5,    # 条形码与它下面的文本之间的距离为浮点。默认值为5。
               "center_text":True,      # 条形码下面文本是否居中
               "background":'white',    # 创建的条形码的背景颜色为字符串。默认为白色 white
               "foreground":'black'     # 创建的条形码的前景颜色为字符串。默认为黑色 black
    }

    # 报告中的条码
    option4 = {
               "module_width":0.2,      # 条形码模块宽度：浮点数。默认值为0.2
               "module_height":6,       # 条形码模块高度：为浮点。默认值为15
               "quiet_zone":0.8,          # 左、右边的距离，从边界到第一个（最后）条形码模块，以M为浮点。默认值为6.5。
               "font_size":12,          # 在PT下的文本大小为整数。默认值为10
               "text_distance": 0.5,    # 条形码与它下面的文本之间的距离为浮点。默认值为5。
               "center_text":True,      # 条形码下面文本是否居中
               "background":'white',    # 创建的条形码的背景颜色为字符串。默认为白色 white
               "foreground":'#C6A079'     # 创建的条形码的前景颜色为字符串 金色
    }

    # 采血台，条码交接
    lis_handle_option = {
       "module_width":0.08,      # 条形码模块宽度：浮点数。默认值为0.2
       "module_height":2,       # 条形码模块高度：为浮点。默认值为15
       "quiet_zone":0.8,       # 左、右边的距离，从边界到第一个（最后）条形码模块，以M为浮点。默认值为6.5。
       "font_size":10,          # 在PT下的文本大小为整数。默认值为10
       "text_distance": 1,    # 条形码与它下面的文本之间的距离为浮点。默认值为5。
       "center_text":True,      # 条形码下面文本是否居中
       "text":"测试",
       "background":'white',    # 创建的条形码的背景颜色为字符串。默认为白色 white
       "foreground":'black'     # 创建的条形码的前景颜色为字符串。默认为黑色 black
    }

    def __init__(self,code='39',path=''):
        self.path = path
        self.tmp = ImageWriter()
        self.tmp.dpi = 254

    # 采集创建条码：新的条码
    def create(self,serialno):
        ean = Code39(serialno, writer=self.tmp, add_checksum=False)
        return ean.save(os.path.join(self.path,serialno), options=self.lis_create_option)

    # 采集创建条码：采集过的条码
    def alter(self,serialno):
        ean = Code39(serialno, writer=self.tmp, add_checksum=False)
        return ean.save(os.path.join(self.path,serialno), options=self.lis_alter_option)

    # 体检报告用到的 条码大小
    def create2(self,serialno):
        ean = Code39(serialno, writer=self.tmp, add_checksum=False)
        return ean.save(os.path.join(self.path,serialno), options=self.option4)

    # 条码交接：
    def create_code39(self,serialno):
        # self.tmp.format = 'png'
        # self.tmp.dpi = 800
        ean = Code128(serialno, writer=self.tmp)
        return ean.save(os.path.join(self.path,serialno), options=self.lis_handle_option)

if __name__=="__main__":
    bc_obj= BarCodeBuild(path=r'C:/Users/Administrator/Desktop/')
    print(bc_obj.create_code39('1902211821'))
    # from pystrich.code128 import Code128Encoder
    # encoder = Code128Encoder("1901291140")
    # encoder.save("C:/Users/Administrator/Desktop/pyStrich.png")


    #
    #
    # 定义二维码生成函数，将网址放入二维码是常用场景
    # def gen_qrcode(link):
    #     qr = qrcode.QRCode(
    #         version=2,
    #         error_correction=qrcode.constants.ERROR_CORRECT_L,
    #         box_size=10,
    #         border=10, )
    #     qr.add_data(link)
    #     qr.make(fit=True)
    #     img = qr.make_image()
    #     img.show()
    #
    #     photopath = os.path.join(settings.MEDIA_ROOT, "test")
    #     if not os.path.exists(photopath):
    #         os.makedirs(photopath)
    #     path = os.path.join(photopath, 'create.jpg')
    #     img.save(path)
    #     return path




