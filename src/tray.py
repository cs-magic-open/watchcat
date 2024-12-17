from pathlib import Path
from typing import TYPE_CHECKING
import sys
from PyQt6.QtGui import QAction, QIcon, QPainter, QPixmap, QColor, QPen
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QMenu, QSystemTrayIcon, QFileDialog, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QDoubleSpinBox, QPushButton, QWidget

from src.config import Config
from src.sounds import SoundType, SoundPlayer

if TYPE_CHECKING:
    from src.TransparentOverlay import TransparentOverlay


class TrayManager:
    def __init__(self, parent: "TransparentOverlay", config: Config):
        self.parent = parent
        self.config = config
        self.setup_tray()
        # Initialize status based on config
        if self.config.data.last_image:
            self.update_status(Path(self.config.data.last_image).name)

    def setup_tray(self):
        """Setup system tray icon and menu"""
        # 先准备图标
        icon_path = str(Path(__file__).parent.parent / "resources" / "icon.svg")
        icon = None
        if Path(icon_path).exists():
            icon = QIcon(icon_path)
            if icon.isNull():
                print(f"Warning: Failed to load icon from {icon_path}")
                icon = QIcon.fromTheme("visibility")
        else:
            print(f"Warning: Icon file not found at {icon_path}")
            icon = QIcon.fromTheme("visibility")

        # 创建托盘图标时直接设置图标
        self.tray = QSystemTrayIcon(icon, parent=self.parent)

        # 创建菜单
        menu = QMenu()

        # Status display
        self.status_action = QAction("当前图片: 无", menu)
        self.status_action.setEnabled(False)
        menu.addAction(self.status_action)

        menu.addSeparator()

        # 图片操作菜单
        image_menu = QMenu("图片操作", menu)
        
        # Select image action
        select_image_action = QAction("选择目标图片", image_menu)
        select_image_action.triggered.connect(self.parent.show_image_picker)
        image_menu.addAction(select_image_action)

        # Reload last image if available
        if self.config.data.last_image:
            reload_action = QAction("重新加载上次图片", image_menu)
            reload_action.triggered.connect(self.parent.reload_last_image)
            image_menu.addAction(reload_action)
            
        menu.addMenu(image_menu)

        menu.addSeparator()

        # 提醒方式菜单
        notification_menu = QMenu("提醒方式", menu)
        

        # Add notification toggle
        notification_action = QAction("系统通知", notification_menu)
        notification_action.setCheckable(True)
        notification_action.setChecked(self.config.data.enable_notification)
        notification_action.triggered.connect(self.toggle_notification)
        notification_menu.addAction(notification_action)

        # Add sound toggle
        sound_action = QAction("声音提醒", notification_menu)
        sound_action.setCheckable(True)
        sound_action.setChecked(self.config.data.enable_sound)
        sound_action.triggered.connect(self.toggle_sound)
        notification_menu.addAction(sound_action)
        
        # 添加声音设置子菜单
        sound_menu = QMenu("声音设置", notification_menu)
        
        # 创建声音选择动作组
        for sound_type in SoundType:
            action = QAction(sound_type.value, sound_menu)
            action.setCheckable(True)
            action.setChecked(self.config.data.sound_type == sound_type.name)
            action.triggered.connect(lambda checked, st=sound_type: self.change_sound_type(st))
            sound_menu.addAction(action)

        # 添加自定义音乐设置选项
        sound_menu.addSeparator()
        custom_settings_action = QAction("自定义音乐设置...", sound_menu)
        custom_settings_action.triggered.connect(self.show_custom_sound_settings)
        sound_menu.addAction(custom_settings_action)
        
        notification_menu.addMenu(sound_menu)
        
        menu.addMenu(notification_menu)

        menu.addSeparator()

        # 高级功能菜单
        advanced_menu = QMenu("高级功能", menu)
        
        # 显示匹配框
        self.toggle_action = QAction("显示匹配框（不会影响正常点击）", advanced_menu)
        self.toggle_action.setCheckable(True)
        self.toggle_action.setChecked(True)
        self.toggle_action.triggered.connect(self.parent.toggle_visibility)
        advanced_menu.addAction(self.toggle_action)
        
        # 添加分隔符
        advanced_menu.addSeparator()
        
        menu.addMenu(advanced_menu)

        menu.addSeparator()

        # 添加关于选项
        about_action = QAction("关于", menu)
        about_action.triggered.connect(self.show_about_dialog)
        menu.addAction(about_action)

        # Quit action
        quit_action = QAction("退出", menu)
        quit_action.triggered.connect(self.parent.app.quit)
        menu.addAction(quit_action)

        # 设置菜单
        self.tray.setContextMenu(menu)
        
        # 使用定时器延迟显示托盘图标
        QTimer.singleShot(100, self.tray.show)

    def update_status(self, image_name: str = None):
        """Update the tray status with current image name"""
        if image_name:
            self.status_action.setText(f"当前图片: {image_name}")
        else:
            self.status_action.setText("当前图片: 无")

    def update_status_text(self, target_image, last_match_info):
        """Update status text"""
        status_parts = []

        if target_image is not None and self.config.data.last_image:
            filename = Path(self.config.data.last_image).name
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
        self.config.data.sound_type = sound_type.name
        self.config.save()  # 保存配置到磁盘
        
        # 更新菜单项选中状态
        sound_menu = None
        for action in self.tray.contextMenu().actions():
            if action.text() == "声音设置":
                sound_menu = action.menu()
                break
        
        if sound_menu:
            for action in sound_menu.actions():
                action.setChecked(action.text() == sound_type.value)

    def toggle_notification(self, checked):
        """Toggle notification setting"""
        self.config.data.enable_notification = checked
        self.config.save()

    def toggle_sound(self, checked):
        """Toggle sound setting"""
        self.config.data.enable_sound = checked
        self.config.save()

    def show_custom_sound_settings(self):
        """显示自定义音乐设置对话框"""
        dialog = CustomSoundDialog(self.config)
        
        # 将对话框移动到屏幕中央
        screen = self.parent.app.primaryScreen().geometry()
        dialog_size = dialog.sizeHint()
        x = screen.center().x() - dialog_size.width() // 2
        y = screen.center().y() - dialog_size.height() // 2
        dialog.move(x, y)
        
        # 显示对话框并处理结果
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # 保存设置
            self.config.data.custom_sound = dialog.get_settings()
            # 如果当前选择的是自定义音乐，更新一下设置
            if self.config.data.sound_type == SoundType.CUSTOM.name:
                self.change_sound_type(SoundType.CUSTOM)

    def show_about_dialog(self):
        """显示关于对话框"""
        dialog = AboutDialog(self.parent)
        
        # 将对话框移动到屏幕中央
        screen = self.parent.app.primaryScreen().geometry()
        dialog_size = dialog.sizeHint()
        x = screen.center().x() - dialog_size.width() // 2
        y = screen.center().y() - dialog_size.height() // 2
        dialog.move(x, y)
        
        dialog.exec()


class CustomSoundDialog(QDialog):
    """自定义音乐设置对话框"""
    def __init__(self, config: Config, parent=None):
        super().__init__(parent)
        self.config = config
        
        # 设置窗口标志
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowStaysOnTopHint
        )
        
        # macOS 特殊处理
        if sys.platform == "darwin":
            import AppKit
            self._app = AppKit.NSApplication.sharedApplication()
            self._original_activation_policy = self._app.activationPolicy()
            self._app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyRegular)
        
        self.setup_ui()

    def closeEvent(self, event):
        """关闭事件处理"""
        # 恢复 macOS 的激活策略
        if sys.platform == "darwin":
            self._app.setActivationPolicy_(self._original_activation_policy)
        super().closeEvent(event)

    def setup_ui(self):
        """设置UI"""
        self.setWindowTitle("自定义音乐设置")
        layout = QVBoxLayout()

        # 当前音乐文件
        current_file = QHBoxLayout()
        self.file_label = QLabel(self.config.data.custom_sound.path or "未选择音乐文件")
        self.file_label.setWordWrap(True)
        select_btn = QPushButton("选择文件")
        select_btn.clicked.connect(self.select_file)
        current_file.addWidget(self.file_label)
        current_file.addWidget(select_btn)
        layout.addLayout(current_file)

        # 开始时间和持续时间设置
        time_settings = QHBoxLayout()
        
        # 开始时间
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("开始时间(秒):"))
        self.start_spin = QDoubleSpinBox()
        self.start_spin.setRange(0, 3600)  # 最长1小时
        self.start_spin.setValue(self.config.data.custom_sound.start)
        self.start_spin.setDecimals(1)
        start_layout.addWidget(self.start_spin)
        time_settings.addLayout(start_layout)
        
        # 持续时间
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("持续时间(秒):"))
        self.duration_spin = QDoubleSpinBox()
        self.duration_spin.setRange(0.1, 10)  # 最短0.1秒，最长10秒
        self.duration_spin.setValue(self.config.data.custom_sound.duration)
        self.duration_spin.setDecimals(1)
        duration_layout.addWidget(self.duration_spin)
        time_settings.addLayout(duration_layout)
        
        layout.addLayout(time_settings)

        # 测试按钮
        test_btn = QPushButton("测试")
        test_btn.clicked.connect(self.test_sound)
        layout.addWidget(test_btn)

        # 确定和取消按钮
        buttons = QHBoxLayout()
        ok_btn = QPushButton("确定")
        ok_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(ok_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)

        self.setLayout(layout)

    def select_file(self):
        """选择音乐文件"""
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "选择音乐文件",
            "",
            "Audio Files (*.mp3 *.wav *.m4a *.ogg);;All Files (*.*)"
        )
        if file_name:
            self.file_label.setText(file_name)

    def test_sound(self):
        """测试当前设置的音效"""
        # 创建临时配置
        temp_config = {
            "custom_sound": {
                "path": self.file_label.text(),
                "start": self.start_spin.value(),
                "duration": self.duration_spin.value()
            }
        }
        # 播放测试音效
        SoundPlayer.play_sound(SoundType.CUSTOM, temp_config)

    def get_settings(self):
        """获取设置值"""
        return {
            "path": self.file_label.text() if self.file_label.text() != "未选择音乐文件" else None,
            "start": self.start_spin.value(),
            "duration": self.duration_spin.value()
        }


class AboutDialog(QDialog):
    """关于对话框"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("关于 WatchCat")
        
        # 设置窗口标志
        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.WindowStaysOnTopHint
        )
        
        # macOS 特殊处理
        if sys.platform == "darwin":
            import AppKit
            self._app = AppKit.NSApplication.sharedApplication()
            self._original_activation_policy = self._app.activationPolicy()
            self._app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyRegular)
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置UI"""
        layout = QVBoxLayout()
        
        # 图标
        icon_label = QLabel()
        icon_path = str(Path(__file__).parent.parent / "resources" / "icon.svg")
        if Path(icon_path).exists():
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                icon_label.setPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(icon_label)
        
        # 应用名称和版本
        title_label = QLabel("WatchCat")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title_label.font()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        layout.addWidget(title_label)
        
        version_label = QLabel("版本 0.1.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        # 描述
        desc_label = QLabel("一款桌面自动化通知工具，基于透明覆盖窗口技术")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)
        
        # 链接
        link_label = QLabel('<a href="https://github.com/cs-magic-open/watchcat">GitHub 仓库</a>')
        link_label.setOpenExternalLinks(True)
        link_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(link_label)
        
        # 版权信息
        copyright_label = QLabel(" 2024 CS Magic")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright_label)
        
        # 确定按钮
        button_box = QHBoxLayout()
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self.accept)
        button_box.addStretch()
        button_box.addWidget(ok_button)
        button_box.addStretch()
        layout.addLayout(button_box)
        
        self.setLayout(layout)
    
    def closeEvent(self, event):
        """关闭事件处理"""
        # 恢复 macOS 的激活策略
        if sys.platform == "darwin":
            self._app.setActivationPolicy_(self._original_activation_policy)
        super().closeEvent(event)
