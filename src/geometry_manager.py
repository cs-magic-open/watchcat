from PyQt6.QtWidgets import QApplication

from src.config import Config


class GeometryManager:
    def __init__(self, widget, config: Config):
        self.widget = widget
        self.config = config
        self.border_width = config.data.border.width

    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()
        size = self.widget.geometry()
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        self.widget.move(x, y)

    def restore_geometry(self):
        """从配置中恢复窗口位置和大小"""
        pos = self.config.data.position
        size = self.config.data.size
        self.widget.setGeometry(pos.x, pos.y, size.width, size.height)

    def save_geometry(self):
        """保存窗口位置和大小到配置"""
        geometry = self.widget.geometry()
        self.config["position"] = {"x": geometry.x(), "y": geometry.y()}
        self.config["size"] = {"width": geometry.width(), "height": geometry.height()}
