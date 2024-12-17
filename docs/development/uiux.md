# UIUX 参考

## PyQt 绘制边框

使用 PyQt 的 `QPainter` 绘制边框时，需要注意以下几个重要事项：

### 基础边框绘制示例

以下是如何在目标区域周围绘制边框的示例：

```python
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class BorderWidget(QWidget):
    def __init__(self):
        super().__init__()
        # 窗口尺寸 = 内容区域 + 两侧边框宽度
        self.setFixedSize(158, 88)  # (118+20+20) x (48+20+20)

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen(Qt.black, 20)  # 创建20px宽的画笔
        painter.setPen(pen)
        # 从(10,10)开始绘制，考虑画笔宽度
        painter.drawRect(10, 10, 138, 68)  # 宽度118+20，高度48+20
```

### 尺寸计算说明

对于一个 118x48 的目标区域，配合 20px 的边框：

- 总窗口尺寸：158x88（内容区域 + 两侧边框）
- 绘制起点：(10,10),因为画笔是从中心线开始绘制
- 矩形尺寸：138x68（内容区域 + 单侧边框）

### 重要注意事项

1. 边框宽度考虑：
    - QPainter 在指定线条的中心位置绘制边框
    - 需要将起始位置偏移半个边框宽度
    - 最终尺寸必须考虑边框厚度

2. 窗口尺寸考虑：
    - 总宽度 = 内容宽度 + (边框宽度 × 2)
    - 总高度 = 内容高度 + (边框宽度 × 2)
    - 绘制位置需要考虑边框宽度的一半

!!! warning "边缘情况警告"
    当在屏幕边缘附近绘制较粗的边框，或者边框宽度相对于内容区域较大时，边框可能会被压缩或变形。这是因为 PyQt 会尝试在可用空间内适配边框，可能导致边框宽度不均匀或出现视觉偏差。
