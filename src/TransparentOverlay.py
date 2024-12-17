import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QFileDialog, QWidget

from .config import Config
from .geometry_manager import GeometryManager
from .signal_manager import SignalManager
from .tray import TrayManager
from .window_painter import WindowPainter
from .log import logger

# Lazy imports
_mss = None
_ImageMatchThread = None
_ImageManager = None

def get_mss():
    global _mss
    if _mss is None:
        from mss import mss
        _mss = mss()
    return _mss

def get_image_match_thread(sct, config):
    global _ImageMatchThread
    if _ImageMatchThread is None:
        from .ImageMatchThread import ImageMatchThread
        _ImageMatchThread = ImageMatchThread(sct, config)
    return _ImageMatchThread

def get_image_manager(config, match_thread):
    global _ImageManager
    if _ImageManager is None:
        from .image_manager import ImageManager
        _ImageManager = ImageManager(config, match_thread)
    return _ImageManager

class TransparentOverlay(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.scale_factor = app.primaryScreen().devicePixelRatio()
        self.last_match_info = None
        self._sct = None
        self._match_thread = None
        self._image_manager = None

        # Initialize essential components first
        self.config = Config()
        self.window_painter = WindowPainter(self, self.config)
        self.geometry_manager = GeometryManager(self, self.config)
        self.signal_manager = SignalManager(app)
        self.tray_manager = TrayManager(self, self.config)

        # Initialize UI
        self.init_ui()

        # Setup cleanup
        app.aboutToQuit.connect(self.cleanup)

        # Defer loading last image
        QTimer.singleShot(100, self.delayed_init)

    def delayed_init(self):
        """延迟初始化较重的组件"""
        if self.config.data.last_image:
            self.ensure_components_initialized()
            self.image_manager.load_last_image()

    def ensure_components_initialized(self):
        """确保组件已初始化"""
        if self._sct is None:
            self._sct = get_mss()
        if self._match_thread is None:
            self._match_thread = get_image_match_thread(self._sct, self.config)
            self._match_thread.match_found.connect(self.on_match_found)
            # 设置托盘管理器
            self._match_thread.set_tray_manager(self.tray_manager)
        if self._image_manager is None:
            self._image_manager = get_image_manager(self.config, self._match_thread)

    @property
    def sct(self):
        self.ensure_components_initialized()
        return self._sct

    @property
    def match_thread(self):
        self.ensure_components_initialized()
        return self._match_thread

    @property
    def image_manager(self):
        self.ensure_components_initialized()
        return self._image_manager

    def init_ui(self):
        """初始化UI"""
        # 设置基本窗口标志
        flags = (
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.NoDropShadowWindowHint  # 禁用阴影
        )
        self.setWindowFlags(flags)

        # 设置窗口属性
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 透明背景

        # 设置平台特定的窗口属性
        from .platform_window import setup_platform_window
        setup_platform_window(self)

        # 设置位置和大小
        self.ensure_components_initialized()  # Ensure components are initialized first
        if self.image_manager.target_image is None:
            self.geometry_manager.center_window()

        self.show()

    def on_match_found(self, match_result):
        """处理匹配结果"""
        # 转换逻辑像素
        x, y, w, h = [int(v / self.scale_factor) for v in match_result]
        logger.debug(f"[on_match_found] 匹配结果: ({x}, {y}, {w}, {h})")

        # 增加边框
        x -= self.config.data.border.width
        y -= self.config.data.border.width
        w += self.config.data.border.width * 2
        h += self.config.data.border.width * 2

        # 更新匹配状态信息
        self.last_match_info = (x, y, w, h)

        # 更新窗口位置和大小
        self.setGeometry(x, y, w, h)

        # 确保窗口可见并在最前面
        if self.tray_manager.is_visible():
            self.hide()
            self.show()

    def paintEvent(self, event):
        """绘制边框"""
        logger.debug(
            f"paintEvent 被调用: event={event}, visible={self.isVisible()}, geometry={self.geometry()}"
        )
        self.window_painter.paint(event)

    def show_image_picker(self):
        """加载目标图片"""
        # 暂存当前可见性状态和窗口属性
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

    def toggle_visibility(self):
        """切换可见性"""
        logger.info(f"切换可见性: {self.isVisible()}")
        if self.isVisible():
            if self.image_manager.target_image is not None:
                self.match_thread.stop()
                self.match_thread.wait()
            self.hide()
            self.tray_manager.toggle_action.setText("显示匹配框")
        else:
            if self.image_manager.target_image is not None:
                # 先确保线程停止
                if self.match_thread.isRunning():
                    self.match_thread.stop()
                    self.match_thread.wait()
                # 重新启动线程
                self.match_thread.start()
            self.show()
            self.raise_()
            self.tray_manager.toggle_action.setText("隐藏匹配框")

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

    def reload_last_image(self):
        """Reload the last used image from config"""
        if self.config["last_image"]:
            self.load_image(self.config["last_image"])
