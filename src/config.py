import json
import os
from pathlib import Path
import sys
from typing import Optional

from pydantic import BaseModel, Field

def get_default_config_path():
    """获取默认配置文件路径，考虑打包情况"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的应用
        base_path = sys._MEIPASS
    else:
        # 如果是开发环境
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    return os.path.join(base_path, 'default_config.json')

class Position(BaseModel):
    x: int = Field(default=100, description="窗口X坐标")
    y: int = Field(default=100, description="窗口Y坐标")

class Size(BaseModel):
    width: int = Field(default=320, description="窗口宽度")
    height: int = Field(default=240, description="窗口高度")

class Border(BaseModel):
    width: int = Field(default=4, description="边框宽度")

class CustomSound(BaseModel):
    path: Optional[str] = Field(default=None, description="本地音乐文件路径")
    start: float = Field(default=0, description="开始时间（秒）")
    duration: float = Field(default=3, description="持续时间（秒）")

class AppConfig(BaseModel):
    position: Position = Field(default_factory=Position, description="窗口位置")
    size: Size = Field(default_factory=Size, description="窗口大小")
    opacity: float = Field(default=1.0, description="窗口透明度")
    color: str = Field(default="#FF0000", description="边框颜色")
    border: Border = Field(default_factory=Border, description="边框设置")
    last_image: Optional[str] = Field(default=None, description="上次使用的图片路径")
    sound_type: str = Field(default="SUCCESS", description="提示音类型")
    enable_notification: bool = Field(default=True, description="是否启用通知")
    enable_sound: bool = Field(default=True, description="是否启用声音")
    custom_sound: CustomSound = Field(default_factory=CustomSound, description="自定义音乐设置")

class Config:
    def __init__(self):
        self.config_path = Path.home() / ".autogui.json"
        self.data = self.load()

    def load(self) -> AppConfig:
        """Load config, use defaults if file doesn't exist"""
        try:
            # 尝试加载用户配置
            with open(self.config_path) as f:
                return AppConfig.model_validate(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            try:
                # 尝试加载默认配置
                with open(get_default_config_path()) as f:
                    return AppConfig.model_validate(json.load(f))
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error loading default config: {e}")
                # 使用默认值创建新配置
                return AppConfig()

    def save(self):
        """Save config to file"""
        with open(self.config_path, "w") as f:
            json.dump(self.data.model_dump(), f, indent=2)

    def __getitem__(self, key):
        """支持字典式访问，同时进行类型检查"""
        return getattr(self.data, key)

    def __setitem__(self, key, value):
        """支持字典式赋值，同时进行类型检查"""
        # 让 pydantic 进行类型验证
        updated_data = self.data.model_dump()
        updated_data[key] = value
        self.data = AppConfig.model_validate(updated_data)
        self.save()
