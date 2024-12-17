# Auto GUI

一个基于图像识别的自动化工具。

## 系统要求

- Python 3.x
- Poetry（依赖管理）
- macOS（目前仅支持）

## 安装

```bash
# 安装依赖
poetry install
```

## 使用前配置

### macOS 通知权限设置

1. 打开 System Settings（系统设置）
2. 进入 Notifications（通知）
3. 找到并点击 "Notificator" 应用
4. 启用通知权限
   - 允许通知（Allow notifications）
   - 建议同时开启横幅通知（Banners）以获得最佳体验

如果没有看到通知，请确保完成以上设置步骤。

## 打包分发

### 使用 Poetry 构建

```bash
# 构建项目
poetry build

# 构建完成后会在 dist/ 目录下生成以下文件：
# - *.whl (wheel 格式，用于 pip 安装)
# - *.tar.gz (源码分发格式)
```

### 安装已打包的版本

```bash
# 使用 pip 安装 wheel 包
pip install dist/*.whl

# 或者安装源码包
pip install dist/*.tar.gz
```

### 发布到 PyPI（可选）

如果需要发布到 PyPI，请先在 pyproject.toml 中更新项目信息（作者、描述等），然后：

```bash
# 发布到 PyPI
poetry publish

# 或者只构建不发布
poetry build
```

## 使用方法

[待补充]
