from transparent_overlay.TransparentOverlay import TransparentOverlay


import AppKit
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication


import sys
import signal
import ApplicationServices


def main():
    # 在创建 QApplication 之前检查权限
    if sys.platform == "darwin":
        import AppKit
        import ApplicationServices

        trusted = ApplicationServices.AXIsProcessTrusted()
        if not trusted:
            # 创建提示对话框
            alert = AppKit.NSAlert.alloc().init()
            alert.setMessageText_("需要辅助功能权限")
            alert.setInformativeText_(
                "为了让窗口显示在 Dock 之上，需要开启辅助功能权限。\n"
                "请在系统偏好设置 > 安全性与隐私 > 隐私 > 辅助功能中授权此应用。\n"
                "授权后请重启应用。"
            )
            alert.addButtonWithTitle_("打开系统偏好设置")
            alert.addButtonWithTitle_("继续使用（窗口可能被 Dock 遮挡）")
            alert.addButtonWithTitle_("退出")

            response = alert.runModal()

            if response == AppKit.NSAlertFirstButtonReturn:
                # 打开系统偏好设置
                AppKit.NSWorkspace.sharedWorkspace().openURL_(
                    AppKit.NSURL.URLWithString_(
                        "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
                    )
                )
                sys.exit(0)
            elif response == AppKit.NSAlertThirdButtonReturn:
                sys.exit(0)

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
