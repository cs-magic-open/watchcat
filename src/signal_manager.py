import signal

from PyQt6.QtCore import QTimer

from .log import logger


class SignalManager:
    def __init__(self, app):
        self.app = app
        self.setup_handlers()

    def setup_handlers(self):
        """Setup signal handlers for graceful shutdown"""

        def signal_handler(*args):
            logger.info("\nReceived termination signal. Closing application...")
            # Use QTimer to safely quit from the main thread
            QTimer.singleShot(0, self.app.quit)

        # Create socket notifier for SIGINT (Ctrl+C)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Handle SIGTSTP (Ctrl+Z) on Unix-like systems
        if hasattr(signal, "SIGTSTP"):
            signal.signal(signal.SIGTSTP, signal_handler)
