import signal
import sys

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication

from transparent_overlay.TransparentOverlay import TransparentOverlay


def main():
    # 在创建 QApplication 之前检查权限
    if sys.platform == "darwin":
        import AppKit

        try:
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

    # 创建应用
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # 创建窗口
    overlay = TransparentOverlay(app)

    # Enable processing of keyboard interrupts
    timer = QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    def signal_handler(signum, frame):
        """处理退出信号"""
        from transparent_overlay.log import logger

        logger.info(f"收到信号: {signum}")
        # 确保清理资源
        overlay.cleanup()
        app.quit()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # ctrl + z
    signal.signal(signal.SIGTSTP, signal_handler)

    # 使用 try-finally 确保清理
    try:
        sys.exit(app.exec())
    finally:
        overlay.cleanup()


if __name__ == "__main__":
    main()
