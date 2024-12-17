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

完全由 AI 编写的高性能屏幕对比与自动通知工具，支持 MacOS、Windows、Linux。

## 项目简介

WatchCat 是一个简单易用的屏幕监控工具，专注于帮助用户实时监控屏幕内容并及时获得通知。

主要功能：
1. 🔍 **选择目标图片**：您可以选择任何想要监控的图片
2. 👀 **实时监控**：自动比对屏幕内容与目标图片
3. 🔔 **及时通知**：当发现匹配时，通过系统通知或音频提醒您

> 我开发这个程序的背景，主要是为了解决一些需要实时监控屏幕特定特征然后通报的场景
>
> 在监控部分，我实现了实时的高性能图像比对，允许用户自由选择本地的目标图形，并且还支持实时屏幕标注（由于系统限制不支持标注在 dock 上方
>
> 在通报部分，我实现了基于系统通知、基于音频通知（支持一些预设音频和本地音乐片段选择），未来还将继续支持邮件、微信等通知形式
>
> 在功能部分，目前还比较机械地只支持单个图片的比对，未来应该支持多个图片，甚至不同的其他输入比对形式，万物皆可比对，只要能定义好比对条件，我们要做的就是一个设定条件然后达标后友好通知的小工具，所以叫 watchcat（致敬 watchdog）
>
> 另外，本项目是全程由 windsurf + claude-3.5 花了两天时间做完，我本人虽然做了多年软件研发，但也确实不够熟悉 pyqt 生态，所以基本上也不懂里面的代码，甚至连实现 ctrl + c/z 退出需要在 thread 中都不知道，花了很多时间，但最多的时间还是在解决文件选择框打开之后绘制罢工的问题
>
> 希望对大家有帮助！也希望对这个项目感兴趣的可以多提 issue 和 pr，我会仔细看的！

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

## 文档

- [在线文档](https://cs-magic-open.github.io/watchcat/)
- [快速入门](https://cs-magic-open.github.io/watchcat/getting-started/)
- [使用指南](https://cs-magic-open.github.io/watchcat/guide/basic-usage/)
- [常见问题](https://cs-magic-open.github.io/watchcat/faq/)

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
