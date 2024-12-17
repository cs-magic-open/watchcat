from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QColor, QPainter, QPen


class WindowPainter:
    def __init__(self, widget, config):
        self.widget = widget
        self.config = config

    def paint(self, event):
        """绘制边框"""
        painter = QPainter(self.widget)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 设置画笔
        pen = QPen(QColor(self.config["color"]))
        pen.setWidth(self.border_width)
        pen.setStyle(Qt.PenStyle.SolidLine)
        pen.setCapStyle(Qt.PenCapStyle.SquareCap)
        painter.setPen(pen)

        # 移除背景
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # 绘制边框
        rect = QRect(
            self.border_width // 2,
            self.border_width // 2,
            self.widget.width() - self.border_width,
            self.widget.height() - self.border_width,
        )
        painter.drawRect(rect)

    @property
    def border_width(self):
        return self.config["border"]["width"]
