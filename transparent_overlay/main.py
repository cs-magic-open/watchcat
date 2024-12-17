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
            
            # 尝试使用 Cocoa API 来设置窗口属性
            try:
                from Foundation import NSWindow
                import AppKit
                
                # 获取原生窗口句柄
                window = self.windowHandle().winId()
                if hasattr(window, 'setCollectionBehavior_'):
                    # 设置窗口行为
                    window.setCollectionBehavior_(
                        AppKit.NSWindowCollectionBehaviorCanJoinAllSpaces |
                        AppKit.NSWindowCollectionBehaviorTransient |
                        AppKit.NSWindowCollectionBehaviorIgnoresCycle
                    )
                    
                    # 设置窗口层级为状态项层级
                    window.setLevel_(AppKit.NSStatusWindowLevel)
                    
                    # 禁用窗口阴影
                    window.setHasShadow_(False)
                    
                    # 设置窗口为非激活状态
                    window.setCanBecomeKeyWindow_(False)
                    window.setCanBecomeMainWindow_(False)
                    
                    # 允许窗口显示但不接受任何输入
                    window.setIgnoresMouseEvents_(True)
                    window.setAcceptsMouseMovedEvents_(False)
                    
                    # 确保窗口始终可见
                    window.setOpaque_(False)
                    window.setBackgroundColor_(AppKit.NSColor.clearColor())
                
            except (ImportError, AttributeError) as e:
                print(f"Warning: Could not set all native window properties: {e}")
        
        # Set geometry from config
        self.setGeometry(
            self.config["position"]["x"],
            self.config["position"]["y"],
            self.config["size"]["width"],
            self.config["size"]["height"]
        )
        
        # Set window opacity
        self.setWindowOpacity(self.config["opacity"])
        
        self.show()

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
            from Foundation import NSBundle
            import AppKit
            
            # 初始化 NSApplication 并设置为后台应用
            app = AppKit.NSApplication.sharedApplication()
            app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)
            
            # 设置为后台应用
            info = NSBundle.mainBundle().infoDictionary()
            info['LSUIElement'] = '1'
            
            # 禁用所有默认的应用程序行为
            app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyProhibited)
            NSApp = AppKit.NSApplication.sharedApplication()
            # NSApp.setPresentsAutomaticallyFullScreen_(False)
            
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