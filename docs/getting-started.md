# 快速开始

## 环境要求

- Python 3.9+
- Poetry
- 操作系统：
    - Windows 10/11
    - macOS 10.15+
    - Linux (X11)

## ⚡️ 安装

### 1. 克隆仓库

```bash
git clone https://github.com/cs-magic-open/watchcat.git
cd watchcat
```

### 2. 安装依赖

使用Poetry安装所有依赖：

```bash
poetry install
```

### 3. 启动应用

```bash
poetry run python -m watchcat
```

## 🎮 基本操作

1. **启动应用**
   - 应用启动后会在系统托盘显示图标
   - 点击托盘图标可以打开主界面

2. **创建覆盖窗口**
   ```python
   from watchcat import create_overlay
   
   overlay = create_overlay()
   overlay.show()
   ```

3. **设置透明度**
   ```python
   overlay.set_opacity(0.5)  # 50%透明度
   ```

4. **添加交互元素**
   ```python
   from PyQt6.QtWidgets import QPushButton
   
   button = QPushButton("Click Me")
   overlay.add_widget(button)
   ```

## 🔧 配置

### 基本配置

```yaml
# config.yaml
window:
  opacity: 0.7
  always_on_top: true
  click_through: false

automation:
  enabled: true
  interval: 1000  # ms
```

### 快捷键设置

- `Ctrl+Shift+H`: 显示/隐藏窗口
- `Ctrl+Shift+Q`: 退出应用
- `Ctrl+Shift+R`: 重载配置

## 📝 下一步

- 查看[基本使用](guide/basic-usage.md)了解更多功能
- 浏览[API参考](api/qt-interface.md)获取详细接口信息
- 加入[开发者社区](development/contributing.md)参与贡献
