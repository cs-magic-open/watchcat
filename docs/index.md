# WatchCat

> 🚀 一个强大的桌面自动化工具，基于透明覆盖窗口技术

[![GitHub stars](https://img.shields.io/github/stars/cs-magic-open/watchcat?style=social)](https://github.com/cs-magic-open/watchcat)
[![Poetry](https://img.shields.io/badge/poetry-managed-blue)](https://python-poetry.org/)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green)](https://www.riverbankcomputing.com/software/pyqt/)

<!-- <iframe src="//player.bilibili.com/player.html?bvid=BV11CB5YWEyM&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" style="width: 100%; height: 500px;"> </iframe> -->

## 🎯 特性

- 💫 透明覆盖窗口
- 🤖 桌面自动化
- 🎨 现代化 GUI 界面
- 🔧 可扩展的插件系统
- 📦 跨平台支持

## 🚀 快速开始

```bash
# 使用Poetry安装
poetry install

# 启动应用
poetry run python -m watchcat
```

## 💡 使用场景

- 桌面自动化测试
- 界面交互录制
- 自动化工作流
- 屏幕监控与分析

## 🛠️ 技术栈

- **PyQt6**: 现代化的 GUI 框架
- **Poetry**: Python 依赖管理
- **OpenCV**: 图像处理
- **NumPy**: 数据处理
- **MSS**: 屏幕捕获

## 📚 文档导航

- [快速开始](getting-started.md) - 5 分钟上手指南
- [基本使用](guide/basic-usage.md) - 核心功能介绍
- [高级功能](guide/advanced.md) - 进阶使用技巧
- [API 参考](api/qt-interface.md) - 详细 API 文档

## 🤝 贡献

欢迎贡献代码！请查看我们的[贡献指南](development/contributing.md)。

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](https://github.com/cs-magic-open/watchcat/blob/main/LICENSE) 文件

## 花絮

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
