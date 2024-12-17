# Qt 界面 API

## Window 类

主要的窗口类，用于创建和管理透明覆盖窗口。

### 基本用法

```python
from watchcat import Window

window = Window()
window.show()
```

### 属性

| 属性 | 类型 | 描述 |
|------|------|------|
| `opacity` | float | 窗口透明度 (0.0-1.0) |
| `click_through` | bool | 是否允许点击穿透 |
| `always_on_top` | bool | 是否总是置顶 |
| `geometry` | QRect | 窗口几何属性 |

### 方法

#### `__init__(self, parent=None)`
创建一个新的窗口实例。

参数:
- `parent`: 父窗口对象（可选）

#### `show(self)`
显示窗口。

#### `hide(self)`
隐藏窗口。

#### `set_opacity(self, value: float)`
设置窗口透明度。

参数:
- `value`: 透明度值 (0.0-1.0)

#### `set_click_through(self, enabled: bool)`
设置是否允许点击穿透。

参数:
- `enabled`: 是否启用点击穿透

#### `set_always_on_top(self, enabled: bool)`
设置窗口是否总是置顶。

参数:
- `enabled`: 是否启用置顶

#### `add_widget(self, widget, x: int = 0, y: int = 0)`
向窗口添加控件。

参数:
- `widget`: Qt控件对象
- `x`: 横坐标位置
- `y`: 纵坐标位置

### 信号

| 信号 | 参数 | 描述 |
|------|------|------|
| `opacity_changed` | float | 透明度改变时触发 |
| `click_through_changed` | bool | 点击穿透状态改变时触发 |
| `geometry_changed` | QRect | 窗口几何属性改变时触发 |

### 示例

```python
from watchcat import Window
from PyQt6.QtWidgets import QPushButton, QLabel
from PyQt6.QtCore import Qt

class MyWindow(Window):
    def __init__(self):
        super().__init__()
        
        # 设置窗口属性
        self.set_opacity(0.8)
        self.set_click_through(False)
        self.set_always_on_top(True)
        
        # 添加按钮
        button = QPushButton("点击", self)
        self.add_widget(button, 10, 10)
        
        # 添加标签
        label = QLabel("Hello", self)
        label.setStyleSheet("color: white;")
        self.add_widget(label, 10, 50)
        
        # 连接信号
        self.opacity_changed.connect(self.on_opacity_changed)
    
    def on_opacity_changed(self, value):
        print(f"透明度改变为: {value}")

# 使用示例
window = MyWindow()
window.show()
```

## 样式定制

### 设置窗口样式

```python
window.setStyleSheet("""
    QWidget {
        background-color: rgba(0, 0, 0, 180);
        border: 1px solid #00ff00;
        border-radius: 5px;
    }
    
    QPushButton {
        background-color: #00ff00;
        color: black;
        border: none;
        padding: 5px;
        border-radius: 3px;
    }
    
    QPushButton:hover {
        background-color: #33ff33;
    }
    
    QLabel {
        color: #00ff00;
        font-family: 'Consolas';
    }
""")
```

### 自定义边框

```python
class BorderlessWindow(Window):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
```
