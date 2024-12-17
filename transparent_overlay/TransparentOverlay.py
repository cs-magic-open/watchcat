import sys
from pathlib import Path

from mss import mss
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QWidget

from .config import Config
from .geometry_manager import GeometryManager
from .image_manager import ImageManager
from .ImageMatchThread import ImageMatchThread
from .log import logger
from .platform_window import setup_platform_window
from .signal_manager import SignalManager
from .tray import TrayManager
from .window_painter import WindowPainter


class TransparentOverlay(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.scale_factor = app.primaryScreen().devicePixelRatio()
        self.last_match_info = None

        # Initialize components
        self.config = Config()
        self.sct = mss()
        self.match_thread = ImageMatchThread(self.sct)
        self.match_thread.match_found.connect(self.on_match_found)

        self.image_manager = ImageManager(self.config, self.match_thread)
        self.window_painter = WindowPainter(self, self.config)
        self.geometry_manager = GeometryManager(self, self.config)
        self.signal_manager = SignalManager(app)

        # Initialize UI
        self.init_ui()
        self.tray_manager = TrayManager(self, self.config)

        # Setup cleanup
        app.aboutToQuit.connect(self.cleanup)

        # Try loading last image
        self.image_manager.load_last_image()

    def init_ui(self):
        # 设置基本窗口标志
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.WindowDoesNotAcceptFocus
        )

        # 设置窗口属性
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 设置平台特定的窗口属性
        setup_platform_window(self)

        # 设置位置和大小
        if self.image_manager.target_image is None:
            self.geometry_manager.center_window()
        else:
            self.geometry_manager.update_geometry(
                self.config["position"]["x"],
                self.config["position"]["y"],
                self.config["size"]["width"],
                self.config["size"]["height"],
            )

        self.show()

    def on_match_found(self, match_result):
        """处理匹配结果"""
        # 转换逻辑像素
        x, y, w, h = [int(v / self.scale_factor) for v in match_result]

        # 更新匹配状态信息
        self.last_match_info = (x, y, w, h)
        self.tray_manager.update_status_text(
            self.image_manager.target_image, self.last_match_info
        )

        # 更新窗口位置和大小
        self.geometry_manager.update_geometry(x, y, w, h)

        # 确保窗口可见
        if self.tray_manager.is_visible():
            self.show()
            self.raise_()
            self.update()

    def show_image_picker(self):
        """加载目标图片"""
        # 暂存当前可见性状态和窗口属性
        was_visible = self.isVisible()
        current_flags = self.windowFlags()

        if sys.platform == "darwin":
            import AppKit

            app = AppKit.NSApplication.sharedApplication()
            original_policy = app.activationPolicy()
            app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyRegular)

        start_dir = ""
        if self.config["last_image"]:
            start_dir = str(Path(self.config["last_image"]).parent)

        file_name, _ = QFileDialog.getOpenFileName(
            None,
            "选择目标图片",
            start_dir,
            "Images (*.png *.jpg *.jpeg)",
            options=QFileDialog.Option.ReadOnly,
        )

        if sys.platform == "darwin":
            app.setActivationPolicy_(original_policy)

        if file_name:
            self.image_manager.load_file(file_name)

        # 恢复窗口属性和可见性
        self.setWindowFlags(current_flags)
        if was_visible and self.tray_manager.is_visible():
            self.show()
            self.raise_()
            self.update()

    def toggle_visibility(self, checked):
        """切换可见性"""
        logger.info(f"切换可见性: {checked}")
        if checked:
            if self.image_manager.target_image is not None:
                # 先确保线程停止
                if self.match_thread.isRunning():
                    self.match_thread.stop()
                    self.match_thread.wait()
                # 重新启动线程
                self.match_thread.start()
            self.show()
            self.raise_()
            self.tray_manager.toggle_action.setText("Hide Draw")
        else:
            if self.image_manager.target_image is not None:
                self.match_thread.stop()
                self.match_thread.wait()
            self.hide()
            self.tray_manager.toggle_action.setText("Show Draw")

    def closeEvent(self, event):
        """关闭事件处理"""
        logger.info("关闭窗口")
        self.cleanup()
        super().closeEvent(event)

    def cleanup(self):
        """清理资源"""
        logger.info("正在清理资源...")
        self.image_manager.cleanup()

        if hasattr(self, "sct"):
            logger.info("关闭屏幕捕获")
            self.sct.close()

    def paintEvent(self, event):
        """绘制边框"""
        self.window_painter.paint(event)

        # 如果在 macOS 上，强制更新 NSPanel
        if sys.platform == "darwin" and hasattr(self, "_panel"):
            self._panel.display()

    def reload_last_image(self):
        """Reload the last used image from config"""
        if self.config["last_image"]:
            self.load_image(self.config["last_image"])
