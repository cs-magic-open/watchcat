import sys

from PyQt6.QtCore import Qt


def setup_platform_window(widget):
    """Setup platform-specific window attributes"""
    if sys.platform == "darwin":
        import AppKit
        import Quartz

        widget.setAttribute(Qt.WidgetAttribute.WA_MacAlwaysShowToolWindow)

        # Create NSPanel
        panel = AppKit.NSPanel.alloc().init()

        panel.setStyleMask_(
            AppKit.NSWindowStyleMaskBorderless
            | AppKit.NSWindowStyleMaskNonactivatingPanel
            | AppKit.NSWindowStyleMaskUtilityWindow
        )

        panel.setBackgroundColor_(AppKit.NSColor.clearColor())
        panel.setFloatingPanel_(True)
        panel.setLevel_(
            Quartz.CGWindowLevelForKey(Quartz.kCGMaximumWindowLevelKey) + 1000
        )
        panel.setAlphaValue_(1.0)
        panel.setOpaque_(False)
        panel.setHasShadow_(False)
        panel.setIgnoresMouseEvents_(True)

        panel.setCollectionBehavior_(
            AppKit.NSWindowCollectionBehaviorCanJoinAllSpaces
            | AppKit.NSWindowCollectionBehaviorStationary
            | AppKit.NSWindowCollectionBehaviorIgnoresCycle
        )

        if widget.windowHandle():
            window = widget.windowHandle()
            window_id = window.winId()
            ns_window = AppKit.NSApp.windowWithWindowNumber_(window_id)
            if ns_window:
                widget._panel = panel
                content_view = AppKit.NSView.alloc().init()
                panel.setContentView_(content_view)
                panel.setFrame_display_(ns_window.frame(), True)
                ns_window.orderOut_(None)
                panel.makeKeyAndOrderFront_(None)

    return widget
