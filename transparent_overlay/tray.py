from pathlib import Path
from typing import TYPE_CHECKING

from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon

from transparent_overlay.config import Config
from transparent_overlay.sounds import SoundType

if TYPE_CHECKING:
    from transparent_overlay.TransparentOverlay import TransparentOverlay


class TrayManager:
    def __init__(self, parent: "TransparentOverlay", config: Config):
        self.parent = parent
        self.config = config
        self.setup_tray()

    def setup_tray(self):
        """Setup system tray icon and menu"""
        self.tray = QSystemTrayIcon(self.parent)
        self.tray.setIcon(QIcon.fromTheme("edit-cut"))

        menu = QMenu()

        # Status display
        self.status_action = QAction("当前图片: 无", menu)
        self.status_action.setEnabled(False)
        menu.addAction(self.status_action)

        menu.addSeparator()

        # Select image action
        select_image_action = QAction("选择目标图片", menu)
        select_image_action.triggered.connect(self.parent.show_image_picker)
        menu.addAction(select_image_action)

        # Reload last image if available
        if self.config["last_image"]:
            reload_action = QAction("重新加载上次图片", menu)
            reload_action.triggered.connect(self.parent.reload_last_image)
            menu.addAction(reload_action)

        menu.addSeparator()

        # 添加声音设置子菜单
        sound_menu = QMenu("提示音设置", menu)
        sound_group = QMenu(sound_menu)
        
        # 创建声音选择动作组
        for sound_type in SoundType:
            action = QAction(sound_type.value, sound_menu)
            action.setCheckable(True)
            action.setChecked(self.config["sound_type"] == sound_type.name)
            action.triggered.connect(lambda checked, st=sound_type: self.change_sound_type(st))
            sound_menu.addAction(action)
        
        menu.addMenu(sound_menu)

        menu.addSeparator()

        # Toggle visibility action
        self.toggle_action = QAction("Hide Draw", menu)
        self.toggle_action.setCheckable(True)
        self.toggle_action.setChecked(True)
        self.toggle_action.triggered.connect(self.parent.toggle_visibility)
        menu.addAction(self.toggle_action)

        # Quit action
        quit_action = QAction("Quit", menu)
        quit_action.triggered.connect(self.parent.app.quit)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
        self.tray.show()

    def update_status_text(self, target_image, last_match_info):
        """Update status text"""
        status_parts = []

        if target_image is not None and self.config["last_image"]:
            filename = Path(self.config["last_image"]).name
            status_parts.append(f"图片: {filename}")

            h, w = target_image.shape[:2]
            status_parts.append(f"大小: {w}x{h}")

            if last_match_info:
                x, y, w, h = last_match_info
                status_parts.append(f"位置: ({x}, {y})")

            self.status_action.setText(" | ".join(status_parts))
        else:
            self.status_action.setText("当前图片: 无")

    def is_visible(self):
        """Return if the overlay should be visible"""
        return self.toggle_action.isChecked()

    def set_visible(self, visible):
        """Set the visibility state"""
        self.toggle_action.setChecked(visible)

    def change_sound_type(self, sound_type: SoundType):
        """更改提示音类型"""
        self.config["sound_type"] = sound_type.name
        
        # 更新菜单项选中状态
        sound_menu = None
        for action in self.tray.contextMenu().actions():
            if action.text() == "提示音设置":
                sound_menu = action.menu()
                break
        
        if sound_menu:
            for action in sound_menu.actions():
                action.setChecked(action.text() == sound_type.value)
