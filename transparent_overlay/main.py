import sys
import json
import signal
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QPoint, QTimer, QRect
from PyQt6.QtGui import QPainter, QColor, QPen

class TransparentOverlay(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app  # Store reference to QApplication
        self.load_config()
        self.init_ui()
        
        # Setup signal handling
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
        if hasattr(signal, 'SIGTSTP'):
            signal.signal(signal.SIGTSTP, signal_handler)

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
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.WindowDoesNotAcceptFocus |
            Qt.WindowType.NoDropShadowWindowHint |
            Qt.WindowType.BypassWindowManagerHint
        )
        
        # 在 macOS 上特别设置
        if sys.platform == 'darwin':
            self.setAttribute(Qt.WidgetAttribute.WA_MacAlwaysShowToolWindow)
        
        # Calculate border adjustment - window needs to be larger to accommodate border
        border_width = self.config['border']['width']
        
        # Set geometry from config - window size includes border
        self.setGeometry(
            self.config["position"]["x"] - border_width,  # 向左扩展边框宽度
            self.config["position"]["y"] - border_width,  # 向上扩展边框宽度
            self.config["size"]["width"] + (border_width * 2),   # 左右各扩展边框宽度
            self.config["size"]["height"] + (border_width * 2)   # 上下各扩展边框宽度
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
        border_width = self.config['border']['width']
        pen.setWidth(border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)
        
        # Draw the border exactly at the content box
        content_rect = QRect(
            border_width // 2,                    # 从边框宽度处开始
            border_width // 2,
            self.config["size"]["width"] + border_width,    # 保持原始内容大小
            self.config["size"]["height"] + border_width
        )
        painter.drawRect(content_rect)

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