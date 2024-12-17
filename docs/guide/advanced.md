# 高级功能

## 自动化脚本

### 编写自定义脚本

```python
from watchcat import Automation, Window
from watchcat.utils import sleep

class MyAutomation(Automation):
    def __init__(self):
        super().__init__()
        self.window = Window()
    
    def run(self):
        # 创建透明窗口
        self.window.show()
        
        # 等待3秒
        sleep(3)
        
        # 模拟点击
        self.click(100, 200)
        
        # 模拟按键
        self.key_press('enter')
        
        # 截图
        self.screenshot('output.png')

# 运行自动化脚本
auto = MyAutomation()
auto.run()
```

### 事件监听

```python
from watchcat import EventListener

class MyListener(EventListener):
    def on_mouse_move(self, x, y):
        print(f"鼠标移动到: {x}, {y}")
    
    def on_key_press(self, key):
        print(f"按下按键: {key}")
    
    def on_window_change(self, window_info):
        print(f"活动窗口变化: {window_info}")

# 启动监听
listener = MyListener()
listener.start()
```

## 插件系统

### 创建插件

```python
from watchcat.plugin import Plugin

class MyPlugin(Plugin):
    def __init__(self):
        super().__init__("我的插件", "1.0.0")
    
    def initialize(self):
        # 插件初始化代码
        self.register_command("hello", self.hello_command)
    
    def hello_command(self, args):
        return "Hello from plugin!"

# 注册插件
plugin = MyPlugin()
plugin.register()
```

### 插件配置

```yaml
# ~/.config/watchcat/plugins/myplugin.yaml
enabled: true
settings:
  option1: value1
  option2: value2
```

## API集成

### HTTP API

```python
from watchcat.api import WatchCatAPI

# 创建API客户端
api = WatchCatAPI("http://localhost:8080")

# 创建窗口
window_id = api.create_window()

# 设置窗口属性
api.set_window_opacity(window_id, 0.7)

# 执行自动化操作
api.click(100, 200)
```

### WebSocket API

```python
from watchcat.api import WatchCatWebSocket

async def main():
    # 连接WebSocket
    ws = await WatchCatWebSocket.connect()
    
    # 订阅事件
    await ws.subscribe("mouse_move")
    
    # 处理事件
    async for event in ws.events():
        if event.type == "mouse_move":
            print(f"鼠标位置: {event.x}, {event.y}")

```

## 性能优化

### 内存管理

```python
from watchcat import MemoryManager

# 配置内存限制
mm = MemoryManager()
mm.set_limit(512)  # MB

# 监控内存使用
@mm.monitor
def my_function():
    # 你的代码
    pass
```

### 多线程处理

```python
from watchcat.threading import ThreadPool

# 创建线程池
pool = ThreadPool(max_workers=4)

# 提交任务
future = pool.submit(my_function, args)

# 获取结果
result = future.result()
```

## 调试工具

### 日志记录

```python
from watchcat.logger import Logger

# 创建日志记录器
logger = Logger("debug.log")

# 记录日志
logger.debug("调试信息")
logger.info("普通信息")
logger.warning("警告信息")
logger.error("错误信息")
```

### 性能分析

```python
from watchcat.profiler import Profiler

# 创建性能分析器
profiler = Profiler()

# 分析代码性能
with profiler.profile("my_operation"):
    # 你的代码
    pass

# 输出性能报告
profiler.report()
```
