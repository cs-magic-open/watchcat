# 自动化 API

## Automation 类

自动化操作的核心类，提供鼠标、键盘模拟和屏幕捕获功能。

### 基本用法

```python
from watchcat import Automation

auto = Automation()
auto.click(100, 200)
auto.type_text("Hello World")
```

### 方法

#### 鼠标操作

##### `click(self, x: int, y: int, button: str = "left")`
在指定位置执行鼠标点击。

参数:
- `x`: 横坐标
- `y`: 纵坐标
- `button`: 鼠标按键 ("left", "right", "middle")

##### `double_click(self, x: int, y: int)`
在指定位置执行双击。

参数:
- `x`: 横坐标
- `y`: 纵坐标

##### `move_to(self, x: int, y: int, duration: float = 0)`
移动鼠标到指定位置。

参数:
- `x`: 横坐标
- `y`: 纵坐标
- `duration`: 移动持续时间（秒）

##### `drag_to(self, start_x: int, start_y: int, end_x: int, end_y: int, duration: float = 0.5)`
执行拖拽操作。

参数:
- `start_x`: 起始横坐标
- `start_y`: 起始纵坐标
- `end_x`: 结束横坐标
- `end_y`: 结束纵坐标
- `duration`: 拖拽持续时间（秒）

#### 键盘操作

##### `type_text(self, text: str, interval: float = 0)`
模拟键盘输入文本。

参数:
- `text`: 要输入的文本
- `interval`: 按键间隔（秒）

##### `key_press(self, key: str)`
按下指定按键。

参数:
- `key`: 按键名称

##### `key_release(self, key: str)`
释放指定按键。

参数:
- `key`: 按键名称

##### `hotkey(self, *keys: str)`
执行组合键。

参数:
- `keys`: 按键序列

#### 屏幕操作

##### `screenshot(self, region: tuple = None) -> Image`
截取屏幕区域。

参数:
- `region`: 截图区域 (x, y, width, height)

返回:
- PIL Image对象

##### `locate_on_screen(self, image_path: str, confidence: float = 0.9) -> tuple`
在屏幕上查找图像。

参数:
- `image_path`: 图像文件路径
- `confidence`: 匹配置信度

返回:
- 匹配位置 (x, y)

### 示例

#### 基础自动化

```python
from watchcat import Automation
from watchcat.utils import sleep

auto = Automation()

# 移动鼠标
auto.move_to(100, 100, duration=1)

# 点击
auto.click(100, 100)

# 等待
sleep(1)

# 输入文本
auto.type_text("Hello World")

# 按组合键
auto.hotkey("ctrl", "a")
auto.hotkey("ctrl", "c")
```

#### 图像识别自动化

```python
from watchcat import Automation

auto = Automation()

# 查找图像位置
pos = auto.locate_on_screen("button.png")
if pos:
    x, y = pos
    auto.click(x, y)

# 截图并保存
screenshot = auto.screenshot()
screenshot.save("screen.png")
```

#### 复杂操作序列

```python
from watchcat import Automation
from watchcat.utils import sleep

class LoginAutomation(Automation):
    def __init__(self, username: str, password: str):
        super().__init__()
        self.username = username
        self.password = password
    
    def run(self):
        # 找到登录按钮
        login_btn = self.locate_on_screen("login_button.png")
        if not login_btn:
            raise Exception("找不到登录按钮")
        
        # 点击登录按钮
        self.click(*login_btn)
        sleep(1)
        
        # 输入用户名
        self.type_text(self.username)
        self.key_press("tab")
        
        # 输入密码
        self.type_text(self.password)
        
        # 提交
        self.key_press("enter")
        
        # 等待登录完成
        sleep(2)
        
        # 验证登录结果
        if self.locate_on_screen("login_success.png"):
            print("登录成功")
        else:
            print("登录失败")

# 使用示例
auto = LoginAutomation("user", "pass")
auto.run()
```

## 注意事项

1. 坐标系统
   - 坐标原点(0,0)在屏幕左上角
   - x轴向右为正
   - y轴向下为正

2. 性能优化
   - 使用`duration`参数可以使动作更自然
   - 适当的`sleep`可以提高可靠性
   - 图像识别操作较慢，建议缓存结果

3. 错误处理
   - 所有操作都可能抛出异常
   - 建议使用try-except处理可能的错误
   - 图像识别可能返回None
