<div align="center">

# <img src="transparent_overlay/resources/icon.svg" width="32" height="32" alt="WatchCat Icon" style="vertical-align: middle" /> WatchCat <img src="transparent_overlay/resources/icon.svg" width="32" height="32" alt="WatchCat Icon" style="vertical-align: middle" />

```
                                    ╭─────────────────────────╮
                                    │   W A T C H C A T      │
                                    │      ╭──────╮          │
                                    │    ╭─┤ ^.^ ├─╮        │
                                    │    │ ╰──────╯ │        │
                                    │    │  Poetry  │        │
                                    │    │   PyQt   │        │
                                    │    ╰──────────╯        │
                                    ╰─────────────────────────╯
```

> 完全由 AI 编写的高性能屏幕对比与自动通知工具，支持 MacOS、Windows、Linux。

</div>

## 主要功能

1. 🔍 **选择目标图片**：您可以选择任何想要监控的图片
2. 👀 **实时监控**：自动比对屏幕内容与目标图片
3. 🔔 **及时通知**：当发现匹配时，通过系统通知或音频提醒您

### 主要特性

- **高性能图像比对**

  - 实时屏幕监控
  - 支持自定义目标图片
  - 智能匹配算法

- **多样化通知**

  - 系统通知
  - 音频提醒（预设音效/自定义音乐）
  - 更多通知方式开发中

- **简单易用**
  - 直观的图形界面
  - 托盘图标运行
  - 低资源占用

### 使用场景

1. **网页监控**

   - 监控网站更新
   - 等待特定内容出现
   - 抢购提醒

2. **游戏通知**

   - 监控游戏状态
   - 提醒重要事件
   - 自动通知

3. **下载完成提醒**
   - 监控下载状态
   - 及时获知完成情况

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/cs-magic-open/watchcat.git
cd watchcat

# 安装依赖
poetry install
```

### 运行

```bash
poetry run python -m watchcat
```

### 基本使用

1. 运行程序，在系统托盘找到猫咪图标
2. 点击图标打开主界面
3. 选择要监控的目标图片
4. 设置通知方式（系统通知/音频）
5. 点击开始，程序会在后台运行
6. 当屏幕出现匹配内容时，您会立即收到通知

## 系统要求

- Python 3.9+
- Poetry（依赖管理）
- macOS 10.15+（目前仅完整支持 macOS，其他平台支持开发中）

## 参与贡献

我们欢迎所有形式的贡献，无论是新功能、bug 修复还是文档改进：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系我们

- 问题反馈：[GitHub Issues](https://github.com/cs-magic-open/watchcat/issues)
- 邮件联系：mark@cs-magic.com

## 更详细的用户文档（不保证更新及时）

[WatchCat 用户文档](https://cs-magic-open.github.io/watchcat/)
