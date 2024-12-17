from PyQt6.QtWidgets import QApplication


class GeometryManager:
    def __init__(self, widget, config):
        self.widget = widget
        self.config = config
        self.border_width = config["border"]["width"]

    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()
        new_width = 320
        new_height = 240
        new_x = (screen.width() - new_width) // 2
        new_y = (screen.height() - new_height) // 2
        self.widget.setGeometry(new_x, new_y, new_width, new_height)

    def update_geometry(self, x, y, width, height):
        """Update window geometry with border consideration"""
        self.widget.setGeometry(
            x - self.border_width,
            y - self.border_width,
            width + (self.border_width * 2),
            height + (self.border_width * 2),
        )
