from random import randint
import sys
from widgets.bwidget import *
from widgets.bchart import *
from PyQt5.QtChart import *

class ChartView(QChartView):

    def __init__(self, *args, **kwargs):
        super(ChartView, self).__init__(*args, **kwargs)
        self.resize(800, 600)
        self.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.initChart()

        # 提示widget
        self.toolTipWidget = GraphicsProxyWidget(self._chart)

        # line 宽度需要调整
        self.lineItem = QGraphicsLineItem(self._chart)
        pen = QPen(Qt.gray)
        self.lineItem.setPen(pen)
        self.lineItem.setZValue(998)
        self.lineItem.hide()

        # 一些固定计算，减少mouseMoveEvent中的计算量
        # 获取x和y轴的最小最大值
        axisX, axisY = self._chart.axisX(), self._chart.axisY()
        self.category_len = len(axisX.categories())
        self.min_x, self.max_x = -0.5, self.category_len - 0.5
        self.min_y, self.max_y = axisY.min(), axisY.max()
        # 坐标系中左上角顶点
        self.point_top = self._chart.mapToPosition(QPointF(self.min_x, self.max_y))

    def mouseMoveEvent(self, event):
        super(ChartView, self).mouseMoveEvent(event)
        pos = event.pos()
        # 把鼠标位置所在点转换为对应的xy值
        x = self._chart.mapToValue(pos).x()
        y = self._chart.mapToValue(pos).y()
        index = round(x)
        # 得到在坐标系中的所有bar的类型和点
        serie = self._chart.series()[0]
        bars = [(bar, bar.at(index))
                for bar in serie.barSets() if self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y]
#         print(bars)
        if bars:
            right_top = self._chart.mapToPosition(
                QPointF(self.max_x, self.max_y))
            # 等分距离比例
            step_x = round(
                (right_top.x() - self.point_top.x()) / self.category_len)
            posx = self._chart.mapToPosition(QPointF(x, self.min_y))
            self.lineItem.setLine(posx.x(), self.point_top.y(),
                                  posx.x(), posx.y())
            self.lineItem.show()
            try:
                title = self.categories[index]
            except:
                title = ""
            t_width = self.toolTipWidget.width()
            t_height = self.toolTipWidget.height()
            # 如果鼠标位置离右侧的距离小于tip宽度
            x = pos.x() - t_width if self.width() - \
                pos.x() - 20 < t_width else pos.x()
            # 如果鼠标位置离底部的高度小于tip高度
            y = pos.y() - t_height if self.height() - \
                pos.y() - 20 < t_height else pos.y()
            self.toolTipWidget.show(
                title, bars, QPoint(x, y))
        else:
            self.toolTipWidget.hide()
            self.lineItem.hide()

    def handleMarkerClicked(self):
        marker = self.sender()  # 信号发送者
        if not marker:
            return
        bar = marker.barset()
        if not bar:
            return
        # bar透明度
        brush = bar.brush()
        color = brush.color()
        alpha = 0.0 if color.alphaF() == 1.0 else 1.0
        color.setAlphaF(alpha)
        brush.setColor(color)
        bar.setBrush(brush)
        # marker
        brush = marker.labelBrush()
        color = brush.color()
        alpha = 0.4 if color.alphaF() == 1.0 else 1.0
        # 设置label的透明度
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setLabelBrush(brush)
        # 设置marker的透明度
        brush = marker.brush()
        color = brush.color()
        color.setAlphaF(alpha)
        brush.setColor(color)
        marker.setBrush(brush)

    def handleMarkerHovered(self, status):
        # 设置bar的画笔宽度
        marker = self.sender()  # 信号发送者
        if not marker:
            return
        bar = marker.barset()
        if not bar:
            return
        pen = bar.pen()
        if not pen:
            return
        pen.setWidth(pen.width() + (1 if status else -1))
        bar.setPen(pen)

    def handleBarHoverd(self, status, index):
        # 设置bar的画笔宽度
        bar = self.sender()  # 信号发送者
        pen = bar.pen()
        if not pen:
            return
        pen.setWidth(pen.width() + (1 if status else -1))
        bar.setPen(pen)

    def initChart(self):
        self._chart = QChart(title="工作量")
        self._chart.setAcceptHoverEvents(True)
        # Series动画
        self._chart.setAnimationOptions(QChart.SeriesAnimations)
        self.categories = ["周一"]
        #names = ["邮件营销", "联盟广告", "视频广告", "直接访问", "搜索引擎"]
        names = ['龚玮玮','卢央央','鲁雪燕','吕瑞兰','麻淑剑','薛颖','杨奕','张施施']
        series = QBarSeries(self._chart)
        for name in names:
            bar = QBarSet(name)
            # 随机数据
            for _ in range(7):
                bar.append(randint(0, 10))
            series.append(bar)
            bar.hovered.connect(self.handleBarHoverd)  # 鼠标悬停
        self._chart.addSeries(series)
        self._chart.createDefaultAxes()  # 创建默认的轴
        # x轴
        axis_x = QBarCategoryAxis(self._chart)
        axis_x.append(self.categories)
        self._chart.setAxisX(axis_x, series)
        # chart的图例
        legend = self._chart.legend()
        legend.setVisible(True)
        # 遍历图例上的标记并绑定信号
        for marker in legend.markers():
            # 点击事件
            marker.clicked.connect(self.handleMarkerClicked)
            # 鼠标悬停事件
            marker.hovered.connect(self.handleMarkerHovered)
        self.setChart(self._chart)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = ChartView()
    view.show()
    sys.exit(app.exec_())