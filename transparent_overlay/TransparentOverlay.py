import sys
import json
import signal
import cv2
from mss import mss
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QFileDialog
from PyQt6.QtCore import Qt, QPoint, QTimer, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QAction, QIcon

from transparent_overlay.ImageMatchThread import ImageMatchThread
from transparent_overlay.log import logger


class TransparentOverlay(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.scale_factor = app.primaryScreen().devicePixelRatio()

        # 添加匹配状态信息
        self.last_match_info = None

        # 加载配置
        self.load_config()

        # 初始化匹配相关
        self.target_image = None
        self.sct = mss()
        self.match_thread = ImageMatchThread(self.sct)
        self.match_thread.match_found.connect(self.on_match_found)

        # 初始化UI
        self.init_ui()
        self.setup_tray()

        # 保程序退出时清理资源
        app.aboutToQuit.connect(self.cleanup)

        # 尝试加载上次的图片
        if self.config.get("last_image"):
            last_image_path = self.config["last_image"]
            if Path(last_image_path).exists():
                logger.info(f"正在加载上次使用的图片: {last_image_path}")
                self.load_image_file(last_image_path)
            else:
                logger.warning(f"上次使用的图片不存在: {last_image_path}")
                self.config["last_image"] = None
                self.save_config()

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

        if sys.platform == "darwin":
            self.setAttribute(Qt.WidgetAttribute.WA_MacAlwaysShowToolWindow)

            # 设置窗口层级高于 Dock
            import AppKit
            import Quartz

            # 创建一个新的 NSPanel
            panel = AppKit.NSPanel.alloc().init()

            # 设置面板样式
            panel.setStyleMask_(
                AppKit.NSWindowStyleMaskBorderless
                | AppKit.NSWindowStyleMaskNonactivatingPanel
                | AppKit.NSWindowStyleMaskUtilityWindow
            )

            # 设置面板属性
            panel.setBackgroundColor_(AppKit.NSColor.clearColor())
            panel.setFloatingPanel_(True)
            panel.setLevel_(
                Quartz.CGWindowLevelForKey(Quartz.kCGMaximumWindowLevelKey) + 1000
            )
            panel.setAlphaValue_(1.0)
            panel.setOpaque_(False)
            panel.setHasShadow_(False)

            # 允许鼠标事件穿透，但保留绘制能力
            panel.setIgnoresMouseEvents_(True)

            # 设置窗口行为
            panel.setCollectionBehavior_(
                AppKit.NSWindowCollectionBehaviorCanJoinAllSpaces
                | AppKit.NSWindowCollectionBehaviorStationary
                | AppKit.NSWindowCollectionBehaviorIgnoresCycle
            )

            # 获取原始窗口并替换
            if self.windowHandle():
                window = self.windowHandle()
                window_id = window.winId()
                ns_window = AppKit.NSApp.windowWithWindowNumber_(window_id)
                if ns_window:
                    # 保存 panel 引用
                    self._panel = panel

                    # 创建新的内容���图
                    content_view = AppKit.NSView.alloc().init()
                    panel.setContentView_(content_view)

                    # 设置面板位置和大小
                    panel.setFrame_display_(ns_window.frame(), True)

                    # 替换原始窗口
                    ns_window.orderOut_(None)
                    panel.makeKeyAndOrderFront_(None)

        # 设置位置和大小
        if self.target_image is None:
            self.center_window()
        else:
            self._update_geometry(
                self.config["position"]["x"],
                self.config["position"]["y"],
                self.config["size"]["width"],
                self.config["size"]["height"],
            )

        self.show()

    def load_config(self):
        """加载配置，如果没有置文件则使用默认配置"""
        config_path = Path.home() / ".autogui.json"
        try:
            with open(config_path) as f:
                self.config = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # 默认配置
            self.config = {
                "position": {"x": 100, "y": 100},
                "size": {"width": 320, "height": 240},
                "opacity": 1.0,
                "color": "#FF0000",  # ���红色
                "border": {"width": 4},  # 加粗边框
                "last_image": None,
            }

        # 保存配置
        self.save_config()

    def save_config(self):
        """保存配置到文件"""
        config_path = Path.home() / ".autogui.json"
        with open(config_path, "w") as f:
            json.dump(self.config, f, indent=2)

    def on_match_found(self, match_result):
        """处理匹配结果"""
        # 转换为逻辑像素
        x, y, w, h = [int(v / self.scale_factor) for v in match_result]

        # 更新匹配状态信息
        self.last_match_info = (x, y, w, h)
        self.update_status_text()

        # 更新窗口位置和大小
        self.setGeometry(
            x - self.border_width,
            y - self.border_width,
            w + (self.border_width * 2),
            h + (self.border_width * 2),
        )

        # 确保窗口可见
        checked = self.toggle_action.isChecked()
        if checked:
            self.show()
            self.raise_()
            self.update()

    def load_image_file(self, file_path: str):
        """加载图片并开始匹配"""
        logger.info(f"开始加载图片: {file_path}")

        # 先停止当前的匹配线程
        if self.target_image is not None:
            logger.info("停止当前匹配线程")
            self.match_thread.stop()

        # 加载新图片
        self.target_image = cv2.imread(file_path)
        if self.target_image is not None:
            h, w = self.target_image.shape[:2]
            logger.info(f"成功加载图片: {w}x{h}")

            # 重置匹配状态信息
            self.last_match_info = None

            # 更新配置
            self.config["last_image"] = file_path
            self.save_config()

            # 更新状态显示
            self.update_status_text()

            # 启动新的匹配线程
            logger.info("启动新的匹配线程")
            self.match_thread.set_target(self.target_image)
            self.match_thread.start()
        else:
            logger.error(f"无法加载图片: {file_path}")

    def paintEvent(self, event):
        """绘制边框"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)  # 启用抗锯齿

        # 设置画笔
        pen = QPen(QColor(self.config["color"]))
        pen.setWidth(self.border_width)
        pen.setStyle(Qt.PenStyle.SolidLine)  # 确保是实线
        pen.setCapStyle(Qt.PenCapStyle.SquareCap)  # 设置线段端点样式
        painter.setPen(pen)

        # 移除背景
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # 绘制边框
        rect = QRect(
            self.border_width // 2,
            self.border_width // 2,
            self.width() - self.border_width,
            self.height() - self.border_width,
        )
        painter.drawRect(rect)

        # 如果在 macOS 上，强制更新 NSPanel
        if sys.platform == "darwin" and hasattr(self, "_panel"):
            self._panel.display()

    def setup_signal_handling(self):
        """Setup signal handlers for graceful shutdown"""

        def signal_handler(*args):
            print("\nReceived termination signal. Closing application...")
            # Use QTimer to safely quit from the main thread
            QTimer.singleShot(0, self.app.quit)

        # Create socket notifier for SIGINT (Ctrl+C)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Handle SIGTSTP (Ctrl+Z) on Unix-like systems
        if hasattr(signal, "SIGTSTP"):
            signal.signal(signal.SIGTSTP, signal_handler)

    @property
    def border_width(self):
        return self.config["border"]["width"]

    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()

        # 使用逻辑���素计算窗口大小和位置
        new_width = 320
        new_height = 240

        # 计算居中位置（screen.width() 和 height() 已经是逻辑像素）
        new_x = (screen.width() - new_width) // 2
        new_y = (screen.height() - new_height) // 2

        self.setGeometry(new_x, new_y, new_width, new_height)
        logger.info(f"窗口居中: 位置({new_x}, {new_y}), 大小({new_width}x{new_height})")

    def setup_tray(self):
        """Setup system tray icon and menu"""
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon.fromTheme("edit-cut"))

        menu = QMenu()

        # 添加状态显示
        self.status_action = QAction("当前图片: 无", menu)
        self.status_action.setEnabled(False)
        menu.addAction(self.status_action)

        menu.addSeparator()

        # 添加选择图片的动作
        select_image_action = QAction("选择目标图片", menu)
        select_image_action.triggered.connect(self.show_image_picker)
        menu.addAction(select_image_action)

        # 如果有上次选择的图片，添加重新加载选项
        if self.config.get("last_image"):
            reload_action = QAction("重新加载上次图片", menu)
            reload_action.triggered.connect(self.reload_last_image)
            menu.addAction(reload_action)

        menu.addSeparator()

        # Toggle visibility action
        self.toggle_action = QAction("Hide Draw", menu)
        self.toggle_action.setCheckable(True)
        self.toggle_action.setChecked(True)
        self.toggle_action.triggered.connect(self.toggle_visibility)
        menu.addAction(self.toggle_action)

        # Quit action
        quit_action = QAction("Quit", menu)
        quit_action.triggered.connect(self.app.quit)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
        self.tray.show()

        # 更新状态显示
        self.update_status_text()

    def update_status_text(self):
        """更新状态文本"""
        status_parts = []

        # 添加当前图片信息
        if self.target_image is not None and self.config.get("last_image"):
            filename = Path(self.config["last_image"]).name
            status_parts.append(f"图片: {filename}")

            # 添加图片尺寸信息
            h, w = self.target_image.shape[:2]
            status_parts.append(f"大小: {w}x{h}")

            # 添加匹配位置信息
            if self.last_match_info:
                x, y, w, h = self.last_match_info
                status_parts.append(f"位置: ({x}, {y})")

            self.status_action.setText(" | ".join(status_parts))
        else:
            self.status_action.setText("当前图片: 无")

    def reload_last_image(self):
        """重新加载上次使用的图片"""
        if self.config.get("last_image"):
            self.load_image_file(self.config["last_image"])

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
        if self.config.get("last_image"):
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
            self.load_image_file(file_name)

        # 恢复窗口属性和可见性
        self.setWindowFlags(current_flags)
        if was_visible and self.toggle_action.isChecked():
            self.show()
            self.raise_()
            self.update()  # 强制重绘

    def toggle_visibility(self, checked):
        """切换可见性"""
        logger.info(f"切换见性: {checked}")
        if checked:
            if self.target_image is not None:
                # 先确保线程停止
                if self.match_thread.isRunning():
                    self.match_thread.stop()
                    self.match_thread.wait()
                # 重新启动线程
                self.match_thread.start()
            self.show()
            self.raise_()
            self.toggle_action.setText("Hide Draw")
        else:
            if self.target_image is not None:
                self.match_thread.stop()
                self.match_thread.wait()
            self.hide()
            self.toggle_action.setText("Show Draw")

    def closeEvent(self, event):
        """关闭事件处理"""
        logger.info("关闭窗口")
        self.cleanup()
        super().closeEvent(event)

    def cleanup(self):
        """清理资源"""
        logger.info("正在清理资源...")
        if self.match_thread and self.match_thread.isRunning():
            logger.info("停止匹配线程")
            self.match_thread.stop()
            self.match_thread.wait()  # 等待线程完全停止

        if hasattr(self, "sct"):
            logger.info("关闭屏幕捕获")
            self.sct.close()