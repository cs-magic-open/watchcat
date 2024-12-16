import sys
import json
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPainter, QColor

class TransparentOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.load_config()
        self.init_ui()
        
    def load_config(self):
        config_path = Path.home() / '.autogui.json'
        if config_path.exists():
            with open(config_path) as f:
                self.config = json.load(f)
        else:
            # Default configuration
            self.config = {
                "position": {
                    "x": 100,
                    "y": 100
                },
                "size": {
                    "width": 50,
                    "height": 50
                },
                "color": "#FF0000",
                "opacity": 0.5
            }
            # Save default config
            with open(config_path, 'w') as f:
                json.dump(self.config, f, indent=2)

    def init_ui(self):
        # Set window flags
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Set geometry from config
        self.setGeometry(
            self.config["position"]["x"],
            self.config["position"]["y"],
            self.config["size"]["width"],
            self.config["size"]["height"]
        )
        
        # Set window opacity
        self.setWindowOpacity(self.config["opacity"])
        
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Set the color from config
        color = QColor(self.config["color"])
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        
        # Draw a filled rectangle
        painter.drawRect(self.rect())

def main():
    app = QApplication(sys.argv)
    
    # Create and show the overlay
    overlay = TransparentOverlay()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 