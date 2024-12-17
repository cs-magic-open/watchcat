from transparent_overlay.TransparentOverlay import TransparentOverlay


import AppKit
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication


import sys


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
