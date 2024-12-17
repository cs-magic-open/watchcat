import sys
import json
import signal
import time
import cv2
import numpy as np
from mss import mss
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QFileDialog
from PyQt6.QtCore import Qt, QPoint, QTimer, QRect, QThread, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPen, QAction, QIcon
from cs_magic_log import setup_logger, LogConfig

log = setup_logger(
    LogConfig(
        log_file=Path.home() / ".autogui.log",
        console_level="DEBUG",
    )
)


class ImageMatchThread(QThread):
    match_found = pyqtSignal(tuple)  # 发送匹配结果的信号 (x, y, w, h)

    def __init__(self, sct):
        super().__init__()
        self.sct = sct
        self.target_image = None
        self.running = False

    def set_target(self, image):
        """设置目标图片"""
        h, w = image.shape[:2]
        log.info(f"设置目标图片: {w}x{h}")
        self.target_image = image

    def run(self):
        """线程主循环"""
        self.running = True
        log.info("开始图像匹配线程")
        while self.running and self.target_image is not None:
            s_time = time.time()
            # 获取屏幕截图
            screen = self.sct.grab(self.sct.monitors[0])
            screen_np = np.array(screen)
            screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_BGRA2BGR)

            # 模板匹配
            result = cv2.matchTemplate(
                screen_bgr, self.target_image, cv2.TM_CCOEFF_NORMED
            )
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            t = time.time() - s_time
            if max_val > 0.8:  # 匹配度阈值
                h, w = self.target_image.shape[:2]
                x, y = max_loc
                log.debug(
                    f"[{t:.2f}s, {max_val*100:.2f}%] 找到匹配: 位置({x}, {y}), 大小({w}x{h})"
                )
                self.match_found.emit((x, y, w, h))
            else:
                log.debug(f"[{t:.2f}s, {max_val*100:.2f}%] 未找到匹配")

            self.msleep(200)

    def stop(self):
        """停止线程"""
        log.info("停止图像匹配线程")
        self.running = False
        self.wait()


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

        # 尝试加载上次的图片
        if self.config.get("last_image"):
            last_image_path = self.config["last_image"]
            if Path(last_image_path).exists():
                log.info(f"正在加载上次使用的图片: {last_image_path}")
                self.load_image_file(last_image_path)
            else:
                log.warning(f"上次使用的图片不存在: {last_image_path}")
                self.config["last_image"] = None
                self.save_config()

    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        if sys.platform == "darwin":
            self.setAttribute(Qt.WidgetAttribute.WA_MacAlwaysShowToolWindow)

        self.center_window()
        self.show()

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
        if self.toggle_action.isChecked():
            self.show()
            self.raise_()
            self.update()

    def load_image_file(self, file_path: str):
        """加载图片并开始匹配"""
        self.target_image = cv2.imread(file_path)
        if self.target_image is not None:
            # 停止之前的匹配线程
            self.match_thread.stop()

            # 重置匹配状态信息
            self.last_match_info = None

            # 更新配置
            self.config["last_image"] = file_path
            self.save_config()

            # 更新状态显示
            self.update_status_text()

            # 开始新的匹配
            self.match_thread.set_target(self.target_image)
            self.match_thread.start()

            # 确保窗口可见
            if self.toggle_action.isChecked():
                self.show()
                self.raise_()

    def paintEvent(self, event):
        """绘制边框"""
        painter = QPainter(self)
        pen = QPen(QColor(self.config["color"]))
        pen.setWidth(self.border_width)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        painter.drawRect(
            self.border_width // 2,
            self.border_width // 2,
            self.width() - self.border_width,
            self.height() - self.border_width,
        )

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

    def load_config(self):
        """加载配置，如果没有配置文件则使用默认配置"""
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
                "color": "#FF0000",  # 纯红色
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

    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()

        # 使用逻辑像素计算窗口大小和位置
        new_width = 320
        new_height = 240

        # 计算居中位置（screen.width() 和 height() 已经是逻辑像素）
        new_x = (screen.width() - new_width) // 2
        new_y = (screen.height() - new_height) // 2

        self.setGeometry(new_x, new_y, new_width, new_height)
        log.info(f"窗口居中: 位置({new_x}, {new_y}), 大小({new_width}x{new_height})")

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
        select_image_action.triggered.connect(self.load_target_image)
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

    def load_target_image(self):
        """加载目标图片"""
        # 暂存当前可见性状态
        was_visible = self.isVisible()

        if sys.platform == "darwin":
            import AppKit

            app = AppKit.NSApplication.sharedApplication()
            original_policy = app.activationPolicy()
            app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyRegular)
            app.activateIgnoringOtherApps_(True)

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
            # 恢复之前的可见性状态
            if was_visible:
                self.show()
                self.raise_()

    def toggle_visibility(self, checked):
        """切换可见性"""
        if checked:
            self.show()
            self.raise_()
            if self.target_image is not None:
                self.match_thread.start()
            self.toggle_action.setText("Hide Draw")
        else:
            self.hide()
            if self.target_image is not None:
                self.match_thread.stop()
            self.toggle_action.setText("Show Draw")

    def closeEvent(self, event):
        """关闭事件处理"""
        self.match_thread.stop()
        super().closeEvent(event)


def main():
    # 在创建 QApplication 之前设置 dock 隐藏
    if sys.platform == "darwin":
        try:
            import AppKit

            # 初始化 NSApplication 并设置为后台应用
            app = AppKit.NSApplication.sharedApplication()

            # 要保留这个，否则一闪而过了
            app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)
            # 禁用所有默认的应用程序行为 （不抢占焦点）
            app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyProhibited)

            from Foundation import NSBundle

            # 不显示在 dock 内
            NSBundle.mainBundle().infoDictionary()["LSUIElement"] = "1"

        except ImportError:
            print(
                "Warning: pyobjc not installed. Please install with: pip install pyobjc-framework-Cocoa"
            )

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Create and show the overlay
    overlay = TransparentOverlay(app)

    # Enable processing of keyboard interrupts
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
