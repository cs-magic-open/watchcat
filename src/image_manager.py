from pathlib import Path

import cv2

from .log import logger


class ImageManager:
    def __init__(self, config, match_thread):
        self.config = config
        self.match_thread = match_thread
        self.target_image = None
        self.tray_manager = None

    def set_tray_manager(self, tray_manager):
        """Set the tray manager reference"""
        self.tray_manager = tray_manager

    def load_file(self, file_path: str):
        """加载图片并开始匹配"""
        logger.info(f"开始加载图片: {file_path}")

        # 先停止当前的匹配线程
        if self.target_image is not None:
            logger.info("停止当前匹配线程")
            self.match_thread.stop()

        # 加载新图片
        self.target_image = cv2.imread(file_path)
        if self.target_image is not None:
            h, w = self.target_image.shape[:2]
            logger.info(f"成功加载图片: {w}x{h}")

            # 更新配置
            self.config["last_image"] = file_path
            self.config.save()

            # 更新托盘状态
            if self.tray_manager:
                self.tray_manager.update_status(Path(file_path).name)

            # 启动新的匹配线程
            logger.info("启动新的匹配线程")
            self.match_thread.set_target(self.target_image)
            self.match_thread.start()

            return True
        else:
            logger.error(f"无法加载图片: {file_path}")
            # 更新托盘状态为无图片
            if self.tray_manager:
                self.tray_manager.update_status(None)
            return False

    def load_last_image(self):
        """尝试加载上次的图片"""
        last_image_path = self.config["last_image"]
        if last_image_path and Path(last_image_path).exists():
            logger.info(f"正在加载上次使用的图片: {last_image_path}")
            return self.load_file(last_image_path)
        else:
            logger.warning(f"上次使用的图片不存在: {last_image_path}")
            self.config["last_image"] = None
            self.config.save()
            return False

    def cleanup(self):
        """清理资源"""
        if self.match_thread and self.match_thread.isRunning():
            logger.info("停止匹配线程")
            self.match_thread.stop()
            self.match_thread.wait()
