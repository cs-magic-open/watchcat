import time

import cv2
import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal

from transparent_overlay.log import logger


class ImageMatchThread(QThread):
    match_found = pyqtSignal(tuple)  # 发送匹配结果的信号 (x, y, w, h)

    def __init__(self, sct):
        super().__init__()
        self.sct = sct
        self.target_image = None
        self.running = False
        self.last_match = None  # 存储上次匹配位置

    def set_target(self, image):
        """设置目标图片"""
        h, w = image.shape[:2]
        logger.info(f"设置目标图片: {w}x{h}")
        self.target_image = image
        self.last_match = None

    def run(self):
        """线程主循环"""
        self.running = True
        logger.info("开始图像匹配线程")
        while self.running and self.target_image is not None:
            s_time = time.time()
            # 获取屏幕截图
            screen = self.sct.grab(self.sct.monitors[0])
            screen_np = np.array(screen)
            screen_bgr = cv2.cvtColor(screen_np, cv2.COLOR_BGRA2BGR)

            # 模板匹配
            result = cv2.matchTemplate(
                screen_bgr, self.target_image, cv2.TM_CCOEFF_NORMED
            )
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            t = time.time() - s_time
            if max_val > 0.8:  # 匹配度阈值
                h, w = self.target_image.shape[:2]
                x, y = max_loc

                # 如果是首次匹配，保存位置
                if self.last_match is None:
                    self.last_match = (x, y)

                # 添加随机抖动 (±20像素)
                # x = self.last_match[0] + random.randint(100, 200)
                # y = self.last_match[1] - random.randint(0, 100)

                logger.info(
                    f"[{t:.2f}s, {max_val*100:.2f}%] 找到匹配: "
                    f"位置({x}, {y}), 大小({w}x{h})"
                )

                # 发送抖动后的位置
                self.match_found.emit((x, y, w, h))
            else:
                logger.warning(f"[{t:.2f}s, {max_val*100:.2f}%] 未找到匹配")

            self.msleep(200)

    def stop(self):
        """停止线程"""
        logger.info("停止图像匹配线程")
        self.running = False
        self.wait()
