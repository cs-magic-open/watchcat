# WatchCat

> 🚀 完全基于 AI 开发的一款桌面自动化工具，基于透明覆盖窗口技术

[![GitHub stars](https://img.shields.io/github/stars/cs-magic-open/watchcat?style=social)](https://github.com/cs-magic-open/watchcat)
[![Release](https://img.shields.io/github/v/release/cs-magic-open/watchcat)](https://github.com/cs-magic-open/watchcat/releases)

<!-- <iframe src="//player.bilibili.com/player.html?bvid=BV11CB5YWEyM&page=1" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true" style="width: 100%; height: 500px;"> </iframe> -->

## ✨ 简介

WatchCat 是一个简单易用的桌面自动化工具，它能帮助你：

- 🔍 **监控屏幕变化**：自动检测屏幕上的特定内容
- 🔔 **及时通知提醒**：当发现匹配时立即通知你
- 🤖 **自动化操作**：可以触发自定义的自动化操作

## 🎯 特性

- 💫 **智能识别**：基于 AI 的图像识别技术
- 🎨 **简单易用**：现代化的图形界面，无需编程知识
- 🔧 **灵活配置**：可自定义监控区域和通知方式
- 📦 **跨平台**：支持 macOS（Windows 和 Linux 即将支持）

## 💡 使用场景

- 📥 **下载监控**：及时知道下载完成
- 🎮 **游戏辅助**：自动检测游戏中的特定场景
- 📊 **数据监控**：监控仪表盘的数据变化
- 🔄 **工作流自动化**：自动化重复性的操作

## 🚀 开始使用

1. [快速上手](getting-started.md)
2. [下载安装](guide/installation.md)
3. [查看教程](guide/basic-usage.md)

## 🤝 参与贡献

WatchCat 是一个开源项目，我们欢迎任何形式的贡献：

- 🐛 [报告问题](https://github.com/cs-magic-open/watchcat/issues)
- 📝 [改进文档](development/contributing.md)
- 💻 [贡献代码](development/setup.md)

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
