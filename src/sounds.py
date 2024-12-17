"""声音管理模块"""
import enum
import numpy as np
import sounddevice as sd
from pydub import AudioSegment
import os
import time


class SoundType(enum.Enum):
    """提示音类型"""
    NONE = "无提示音"
    BEEP = "简单提示音"
    SUCCESS = "成功提示音"
    ERROR = "错误提示音"
    MARIO = "马里奥音效"
    CUSTOM = "自定义音乐"


class SoundPlayer:
    """声音播放器类"""
    _custom_sound_cache = None  # 缓存加载的自定义音频

    @staticmethod
    def generate_sine_wave(frequency: float, duration: float, sample_rate: int = 44100) -> np.ndarray:
        """生成正弦波

        Args:
            frequency: 频率 (Hz)
            duration: 持续时间 (秒)
            sample_rate: 采样率 (Hz)

        Returns:
            numpy.ndarray: 音频数据
        """
        t = np.linspace(0, duration, int(duration * sample_rate), False)
        note = np.sin(2 * np.pi * frequency * t)
        return note.astype(np.float32)

    @classmethod
    def _play_buffer(cls, audio_data, sample_rate=44100):
        """安全地播放音频缓冲区"""
        try:
            sd.play(audio_data, sample_rate, blocking=False)
        except Exception as e:
            from src.log import logger
            logger.warning(f"播放音频失败: {e}")

    @classmethod
    def play_sound(cls, sound_type: SoundType, config=None) -> None:
        """根据类型播放提示音

        Args:
            sound_type: 提示音类型
            config: 配置对象，用于自定义音乐设置
        """
        if sound_type == SoundType.NONE:
            return
        elif sound_type == SoundType.BEEP:
            cls.play_beep()
        elif sound_type == SoundType.SUCCESS:
            cls.play_success()
        elif sound_type == SoundType.ERROR:
            cls.play_error()
        elif sound_type == SoundType.MARIO:
            cls.play_mario()
        elif sound_type == SoundType.CUSTOM and config:
            cls.play_custom(config)

    @classmethod
    def play_beep(cls, frequency: float = 440, duration: float = 0.25) -> None:
        """播放蜂鸣声

        Args:
            frequency: 频率 (Hz)，默认 440Hz (标准 A 音)
            duration: 持续时间 (秒)，默认 0.25 秒
        """
        audio = cls.generate_sine_wave(frequency, duration)
        cls._play_buffer(audio)

    @classmethod
    def play_success(cls) -> None:
        """播放成功提示音 (上升音)"""
        audio1 = cls.generate_sine_wave(440, 0.1)  # A4
        audio2 = cls.generate_sine_wave(523.25, 0.1)  # C5
        audio = np.concatenate([audio1, audio2])
        cls._play_buffer(audio)

    @classmethod
    def play_error(cls) -> None:
        """播放错误提示音 (下降音)"""
        audio1 = cls.generate_sine_wave(440, 0.1)  # A4
        audio2 = cls.generate_sine_wave(349.23, 0.1)  # F4
        audio = np.concatenate([audio1, audio2])
        cls._play_buffer(audio)

    @classmethod
    def play_mario(cls) -> None:
        """播放马里奥风格的提示音"""
        frequencies = [660, 660, 0, 660, 0, 520, 660, 0, 784]
        durations = [0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.15]
        audio_parts = []
        
        for freq, dur in zip(frequencies, durations):
            if freq == 0:  # 静音
                audio_parts.append(np.zeros(int(dur * 44100), dtype=np.float32))
            else:
                audio_parts.append(cls.generate_sine_wave(freq, dur))
        
        audio = np.concatenate(audio_parts)
        cls._play_buffer(audio)

    @classmethod
    def play_custom(cls, config) -> None:
        """播放自定义音乐

        Args:
            config: 配置对象，包含自定义音乐设置
        """
        custom_config = config["custom_sound"]
        if not custom_config["path"] or not os.path.exists(custom_config["path"]):
            return

        try:
            # 检查是否需要重新加载音频
            if (cls._custom_sound_cache is None or 
                cls._custom_sound_cache.get("path") != custom_config["path"]):
                # 加载音频文件
                audio = AudioSegment.from_file(custom_config["path"])
                cls._custom_sound_cache = {
                    "path": custom_config["path"],
                    "audio": audio
                }
            else:
                audio = cls._custom_sound_cache["audio"]

            # 提取指定区间
            start_ms = int(custom_config["start"] * 1000)  # 转换为毫秒
            duration_ms = int(custom_config["duration"] * 1000)
            segment = audio[start_ms:start_ms + duration_ms]

            # 导出为临时文件并播放
            segment = segment.set_channels(1)  # 转换为单声道
            samples = np.array(segment.get_array_of_samples(), dtype=np.float32)
            
            # 确保音量适中
            max_sample = np.max(np.abs(samples))
            if max_sample > 0:
                samples = samples / max_sample
            
            # 播放音频
            cls._play_buffer(samples, segment.frame_rate)

        except Exception as e:
            from src.log import logger
            logger.warning(f"播放自定义音乐失败: {e}")
