# WatchCat

一个基于图像识别的桌面自动化工具。

## 系统要求

- Python 3.x
- Poetry（依赖管理）
- macOS（目前仅支持）

## 安装

### 方法一：直接安装应用程序（推荐）

1. 下载最新的 `WatchCat.dmg` 文件
2. 双击打开 DMG 文件
3. 将 WatchCat 应用拖到 Applications 文件夹
4. 从 Applications 文件夹运行应用

### 方法二：从源码安装

```bash
# 克隆仓库
git clone https://github.com/cs-magic-open/watchcat.git
cd watchcat

# 安装依赖
poetry install
```

## 使用前配置

### macOS 通知权限设置

1. 打开 System Settings（系统设置）
2. 进入 Notifications（通知）
3. 找到并点击 "WatchCat" 应用
4. 启用通知权限
   - 允许通知（Allow notifications）
   - 建议同时开启横幅通知（Banners）以获得最佳体验

如果没有看到通知，请确保完成以上设置步骤。

## 打包分发

### 打包为 macOS 应用程序

```bash
# 安装开发依赖
poetry install --with dev

# 使用 pyinstaller 打包
poetry run pyinstaller watchcat.spec

# 打包完成后，可以在 dist/WatchCat 目录下找到应用程序
```

打包完成后有以下使用方式：

1. 直接运行
   - 双击 `dist/WatchCat/WatchCat` 即可运行应用程序

2. 安装到系统
   - 将 `dist/WatchCat` 目录复制到 `/Applications` 文件夹

3. 创建安装包（推荐）
   ```bash
   # 安装 create-dmg 工具
   brew install create-dmg
   
   # 创建 DMG 安装包
   create-dmg \
     --volname "WatchCat" \
     --volicon "resources/icon.icns" \
     --window-pos 200 120 \
     --window-size 600 300 \
     --icon-size 100 \
     --icon "WatchCat" 175 120 \
     --hide-extension "WatchCat" \
     --app-drop-link 425 120 \
     "WatchCat.dmg" \
     "dist/WatchCat/"
   ```

### 使用 Poetry 构建 Python 包

如果你想将 WatchCat 作为 Python 包分发，可以使用以下命令：

```bash
# 构建项目
poetry build

# 构建完成后会在 dist/ 目录下生成以下文件：
# - *.whl (wheel 格式，用于 pip 安装)
# - *.tar.gz (源码分发格式)
```

安装已构建的包：
```bash
# 使用 pip 安装 wheel 包
pip install dist/*.whl

# 或者安装源码包
pip install dist/*.tar.gz
```

## 使用方法

[待补充]

## 贡献

欢迎提交 Pull Request 和 Issue！

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 联系方式

- Email: mark@cs-magic.com
- GitHub: [cs-magic-open/watchcat](https://github.com/cs-magic-open/watchcat)
