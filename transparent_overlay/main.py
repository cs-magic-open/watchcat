import sys
import json
import signal
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QPoint, QTimer
from PyQt6.QtGui import QPainter, QColor

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
        config_path = Path.home() / '.autogui.json'
        if config_path.exists():
            with open(config_path) as f:
                self.config = json.load(f)
        else:
            # Default configuration
            self.config = {
                "position": {
                    "x": 100,
                    "y": 100
                },
                "size": {
                    "width": 50,
                    "height": 50
                },
                "color": "#FF0000",
                "opacity": 0.5
            }
            # Save default config
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)

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
            self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
            self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Set geometry from config
        self.setGeometry(
            self.config["position"]["x"],
            self.config["position"]["y"],
            self.config["size"]["width"],
            self.config["size"]["height"]
        )
        
        # Set window opacity
        self.setWindowOpacity(self.config["opacity"])
        
        # 显示窗口
        self.show()
        
        # 等待窗口创建完成后设置原生窗口属性
        QTimer.singleShot(0, self.setup_native_window)

    def setup_native_window(self):
        """Setup native window properties after window is created"""
        if sys.platform == 'darwin':
            try:
                from Foundation import NSWindow
                import AppKit
                
                # 获取原生窗口句柄
                window = self.windowHandle()
                if window and hasattr(window, 'winId'):
                    native_window = window.winId()
                    if hasattr(native_window, 'setCollectionBehavior_'):
                        # 设置窗口行为
                        native_window.setCollectionBehavior_(
                            AppKit.NSWindowCollectionBehaviorCanJoinAllSpaces |
                            AppKit.NSWindowCollectionBehaviorTransient |
                            AppKit.NSWindowCollectionBehaviorIgnoresCycle
                        )
                        
                        # 设置窗口层级为状态项层级
                        native_window.setLevel_(AppKit.NSStatusWindowLevel)
                        
                        # 禁用窗口阴影
                        native_window.setHasShadow_(False)
                        
                        # 设置窗口为非激活状态
                        native_window.setCanBecomeKeyWindow_(False)
                        native_window.setCanBecomeMainWindow_(False)
                        
                        # 允许窗口显示但不接受任何输入
                        native_window.setIgnoresMouseEvents_(True)
                        native_window.setAcceptsMouseMovedEvents_(False)
                        
                        # 确保窗口始终可见
                        native_window.setOpaque_(False)
                        native_window.setBackgroundColor_(AppKit.NSColor.clearColor())
            except Exception as e:
                print(f"Warning: Could not set all native window properties: {e}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Set the color from config
        color = QColor(self.config["color"])
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        
        # Draw a filled rectangle
        painter.drawRect(self.rect())

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