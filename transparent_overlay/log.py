from cs_magic_log import LogConfig, setup_logger


from pathlib import Path


# logger = setup_logger(
#     LogConfig(
#         log_file=Path.home() / ".autogui.log",
#         console_level="DEBUG",
#     )
# )

from loguru import logger as _logger


logger = _logger
