import sys
import json
import signal
import cv2
import numpy as np
from mss import mss
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QFileDialog
from PyQt6.QtCore import Qt, QPoint, QTimer, QRect
from PyQt6.QtGui import QPainter, QColor, QPen, QAction, QIcon

class TransparentOverlay(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.load_config()
        self.init_ui()
        self.setup_tray()
        self.setup_signal_handling()
        
        # 初始化屏幕捕获
        self.sct = mss()
        self.target_image = None
        self.match_timer = QTimer()
        self.match_timer.timeout.connect(self.update_match_position)
        
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
        if hasattr(signal, 'SIGTSTP'):
            signal.signal(signal.SIGTSTP, signal_handler)

    @property
    def border_width(self):
        return self.config['border']['width']

    def load_config(self):
        """
        todo: better config management
        """
        config_path = Path.home() / '.autogui.json'
        with open(config_path) as f:
            self.config = json.load(f)
        print("config: ", self.config)

    def init_ui(self):
        # Set window flags
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )
        
        # 在 macOS 上特别设置
        if sys.platform == 'darwin':
            self.setAttribute(Qt.WidgetAttribute.WA_MacAlwaysShowToolWindow)
            # self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        # Set geometry from config - window size includes border
        self.setGeometry(
            self.config["position"]["x"] - self.border_width,
            self.config["position"]["y"] - self.border_width,
            self.config["size"]["width"] + (self.border_width * 2),
            self.config["size"]["height"] + (self.border_width * 2)
        )
        
        # Set window opacity
        self.setWindowOpacity(self.config["opacity"])
        
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Set the border color from config
        color = QColor(self.config["color"])
        
        # Remove the brush (background fill)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        # Set the pen for border
        pen = QPen(color)
        pen.setWidth(self.border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)
        
        # Draw the border exactly at the content box
        content_rect = QRect(
            self.border_width // 2,                    # 从边框宽度处开始
            self.border_width // 2,
            self.config["size"]["width"] + self.border_width,    # 保持原始内容大小
            self.config["size"]["height"] + self.border_width
        )
        painter.drawRect(content_rect)

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

    def load_target_image(self):
        """加载目标图片"""
        # 临时保存当前窗口状态
        current_flags = self.windowFlags()
        current_visible = self.isVisible()
        
        # 临时隐藏并移除置顶标志
        self.hide()
        self.setWindowFlags(current_flags & ~Qt.WindowType.WindowStaysOnTopHint)
        
        # 创建文件对话框
        dialog = QFileDialog(None)  # 使用 None 作为父窗口
        dialog.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowStaysOnTopHint
        )
        dialog.setWindowTitle("选择目标图片")
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        dialog.setNameFilter("Images (*.png *.jpg *.jpeg)")
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        
        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_name = dialog.selectedFiles()[0]
            self.target_image = cv2.imread(file_name)
            if self.target_image is not None:
                self.match_timer.start(1000)
                self.update_match_position()
            else:
                print("无法加载图片")
        
        # 恢复窗口状态
        self.setWindowFlags(current_flags)
        if current_visible:
            self.show()
            self.raise_()

    def update_match_position(self):
        """更新匹配位置"""
        if self.target_image is None:
            return
            
        # 获取屏幕截图
        screen = self.sct.grab(self.sct.monitors[0])
        screen_np = np.array(screen)
        screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_BGRA2BGR)
        
        # 模板匹配
        result = cv2.matchTemplate(screen_bgr, self.target_image, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)
        
        if max_val > 0.8:  # 匹配度阈值
            # 更新窗口位置和大小
            h, w = self.target_image.shape[:2]
            x, y = max_loc
            
            self.config["position"]["x"] = x
            self.config["position"]["y"] = y
            self.config["size"]["width"] = w
            self.config["size"]["height"] = h
            
            # 更新窗口几何属性
            self.setGeometry(
                x - self.border_width,
                y - self.border_width,
                w + (self.border_width * 2),
                h + (self.border_width * 2)
            )
            self.update()

    def toggle_visibility(self, checked):
        """修改切换可见性的逻辑"""
        if checked:
            self.show()
            if self.target_image is not None:
                self.match_timer.start(1000)
            self.toggle_action.setText("Hide Draw")
            # 确保窗口保持在最顶层
            self.raise_()
        else:
            self.hide()
            self.match_timer.stop()
            self.toggle_action.setText("Show Draw")

def main():
    # 在创建 QApplication 之前设置 dock 隐藏
    if sys.platform == 'darwin':
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
            NSBundle.mainBundle().infoDictionary()['LSUIElement'] = '1'
            
        except ImportError:
            print("Warning: pyobjc not installed. Please install with: pip install pyobjc-framework-Cocoa")
    
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # Create and show the overlay
    overlay = TransparentOverlay(app)
    
    # Enable processing of keyboard interrupts
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 