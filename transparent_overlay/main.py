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
                    f"[{t:.2f}s, {max_val:.2f}%] 找到匹配: 位置({x}, {y}), 大小({w}x{h})"
                )
                self.match_found.emit((x, y, w, h))
            else:
                log.debug(f"[{t:.2f}s, {max_val:.2f}%] 未找到匹配")

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

        # Initialize target_image before init_ui
        self.target_image = None
        self.load_config()

        # Initialize screen capture and matching thread
        self.sct = mss()
        self.match_thread = ImageMatchThread(self.sct)
        self.match_thread.match_found.connect(self.update_window_geometry)

        self.init_ui()
        self.setup_tray()
        self.setup_signal_handling()

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

        with open(config_path) as f:
            self.config = json.load(f)

    def _update_geometry(self, x: int, y: int, width: int, height: int):
        """统一处理窗口几何属性的更新
        Args:
            x: 窗口 x 坐标
            y: 窗口 y 坐标
            width: 内容区域宽度
            height: 内容区域高度
        """
        # 更新配置
        self.config["position"]["x"] = x
        self.config["position"]["y"] = y
        self.config["size"]["width"] = width
        self.config["size"]["height"] = height

        # 设置窗口几何属性（考虑边框宽度）
        self.setGeometry(
            x - self.border_width,
            y - self.border_width,
            width + (self.border_width * 2),
            height + (self.border_width * 2),
        )
        self.update()  # 触发重绘

    def center_window(self):
        """将窗口居中显示"""
        screen = QApplication.primaryScreen().geometry()

        # 计算新的窗口大小 (屏幕的1/4)
        new_width = 320
        new_height = 240

        # 计算居中位置
        new_x = (screen.width() - new_width) // 2
        new_y = (screen.height() - new_height) // 2

        self._update_geometry(new_x, new_y, new_width, new_height)
        log.info(f"窗口居中: 位置({new_x}, {new_y}), 大小({new_width}x{new_height})")

    def init_ui(self):
        # Set window flags
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowStaysOnTopHint
        )

        # 在 macOS 上特别设置
        if sys.platform == "darwin":
            self.setAttribute(Qt.WidgetAttribute.WA_MacAlwaysShowToolWindow)

        # 根据是否有目标图片决定窗口位置和大小
        if self.target_image is None:
            self.center_window()
        else:
            self._update_geometry(
                self.config["position"]["x"],
                self.config["position"]["y"],
                self.config["size"]["width"],
                self.config["size"]["height"],
            )

        self.setWindowOpacity(self.config["opacity"])
        self.show()

    def _draw_border(self, painter: QPainter, rect: QRect):
        """绘制边框
        Args:
            painter: QPainter 实例
            rect: 要绘制的矩形区域
        """
        # Set the border color from config
        color = QColor(self.config["color"])

        # Remove the brush (background fill)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        # Set the pen for border
        pen = QPen(color)
        pen.setWidth(self.border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        # Draw the border
        painter.drawRect(rect)

    def _get_content_rect(self) -> QRect:
        """获取内容区域的矩形"""
        return QRect(
            self.border_width // 2,
            self.border_width // 2,
            self.config["size"]["width"] + self.border_width,
            self.config["size"]["height"] + self.border_width,
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        self._draw_border(painter, self._get_content_rect())

    def setup_tray(self):
        """Setup system tray icon and menu"""
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(QIcon.fromTheme("edit-cut"))

        menu = QMenu()

        # 添加择图片的动作
        select_image_action = QAction("选择目标图片", menu)
        select_image_action.triggered.connect(self.load_target_image)
        menu.addAction(select_image_action)

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

    def update_window_geometry(self, match_result):
        """更新窗口位置和大小"""
        x, y, w, h = match_result
        self._update_geometry(x, y, w, h)

        # 确保窗口显示并在最顶层
        if not self.isVisible() and self.toggle_action.isChecked():
            self.show()
        self.raise_()

    def load_target_image(self):
        """加载目标图片"""
        if sys.platform == "darwin":
            import AppKit

            app = AppKit.NSApplication.sharedApplication()
            original_policy = app.activationPolicy()
            app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyRegular)
            app.activateIgnoringOtherApps_(True)

        file_name, _ = QFileDialog.getOpenFileName(
            None,
            "选择目标图片",
            "",
            "Images (*.png *.jpg *.jpeg)",
            options=QFileDialog.Option.ReadOnly,
        )

        if sys.platform == "darwin":
            app.setActivationPolicy_(original_policy)

        if file_name:
            log.info(f"选择图片: {file_name}")
            self.target_image = cv2.imread(file_name)
            if self.target_image is not None:
                h, w = self.target_image.shape[:2]
                log.info(f"成功加载图片: {w}x{h}")
                # 设置目标图片并启动匹配线程
                self.match_thread.set_target(self.target_image)
                self.match_thread.start()
            else:
                log.error(f"无法加载图片: {file_name}")

    def toggle_visibility(self, checked):
        """修改切换可见性的逻辑"""
        if checked:
            self.show()
            if self.target_image is not None:
                self.match_thread.start()
            self.toggle_action.setText("Hide Draw")
            self.raise_()
        else:
            self.hide()
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
