# WatchCat

一个高性能的屏幕监控与自动通知工具，致敬 watchdog！

## 项目简介

WatchCat 是一个基于 PyQt 开发的桌面自动化工具，专注于实时屏幕监控和智能通知功能。本项目旨在解决需要实时监控屏幕特定特征并进行及时通报的应用场景。

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
  - 支持自由选择本地目标图形
  - 实时屏幕标注功能（受系统限制，不支持在 dock 上方标注）

- **多样化通知方式**
  - 系统通知
  - 音频通知
    - 支持预设音频
    - 支持本地音乐片段选择
  - 计划支持：邮件通知、微信通知等

### 技术栈

- Poetry（依赖管理）
- PyQt（GUI 框架）
- Python 3.x

## 项目愿景

WatchCat 的目标是打造一个通用的"条件监控-通知触发"工具。未来规划：

- 支持多图片同时监控
- 扩展更多输入比对形式
- 支持更灵活的比对条件定义
- 增加更多通知渠道

## 系统要求

- Python 3.x
- Poetry（依赖管理）
- macOS（目前仅支持）

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

## 参与贡献

我们欢迎所有形式的贡献，无论是新功能、bug 修复还是文档改进：

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的改动 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 问题反馈

如果您在使用过程中遇到任何问题，或有任何功能建议，欢迎：

- 提交 [Issue](https://github.com/cs-magic-open/watchcat/issues)
- 提交 [Pull Request](https://github.com/cs-magic-open/watchcat/pulls)

我们会认真查看每一个反馈！

## 开源协议

本项目采用 [MIT](LICENSE) 协议开源。
