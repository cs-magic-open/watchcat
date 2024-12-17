import json
from pathlib import Path


class Config:
    def __init__(self):
        self.config_path = Path.home() / ".autogui.json"
        self.data = self.load()

    def load(self):
        """Load config, use defaults if file doesn't exist"""
        try:
            with open(self.config_path) as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "position": {"x": 100, "y": 100},
                "size": {"width": 320, "height": 240},
                "opacity": 1.0,
                "color": "#FF0000",
                "border": {"width": 4},
                "last_image": None,
                "sound_type": "SUCCESS",  # 默认使用成功提示音
                "custom_sound": {
                    "path": None,  # 本地音乐文件路径
                    "start": 0,    # 开始时间（秒）
                    "duration": 3  # 持续时间（秒）
                }
            }

    def save(self):
        """Save config to file"""
        with open(self.config_path, "w") as f:
            json.dump(self.data, f, indent=2)

    def __getitem__(self, key):
        return self.data.get(key) or "SUCCESS"

    def __setitem__(self, key, value):
        self.data[key] = value
        self.save()
