# 打包与发布指南

本文档说明如何打包和发布 WatchCat 应用。

## 打包流程

WatchCat 使用 PyInstaller 进行打包，通过 GitHub Actions 自动构建各个平台的发布版本。

### 本地打包测试

在本地进行打包测试时，请确保已安装所有依赖：

```bash
# 安装项目依赖
poetry install --with dev

# 使用 PyInstaller 打包
poetry run pyinstaller --clean --onefile --windowed transparent_overlay/main.py

打包后的文件将在 `dist` 目录下生成。在 macOS 系统上，你可以通过以下两种方式运行打包后的程序：

1. 命令行方式：
   ```bash
   cd dist
   ./main
   ```

2. 图形界面方式：
   在 Finder 中双击 `main.app` 文件夹

### 发布新版本

1. 更新版本号
   ```bash
   poetry version [patch|minor|major]
   ```

2. 提交变更并创建标签
   ```bash
   git add pyproject.toml
   git commit -m "chore: bump version to $(poetry version -s)"
   git tag "v$(poetry version -s)"
   git push origin main --tags
   ```

3. GitHub Actions 将自动构建以下格式的发布包：
   - Windows: `.exe`
   - macOS: `.dmg`
   - Linux: 可执行文件

## 平台特定说明

### Windows

Windows 版本会打包成单个 `.exe` 文件，用户可以直接运行。

### macOS

macOS 版本打包为 `.dmg` 格式，用户可以：
1. 双击打开 DMG 文件
2. 将应用拖拽到 Applications 文件夹
3. 从 Applications 文件夹启动应用

### Linux

Linux 版本打包为单个可执行文件，用户需要：
1. 添加执行权限：`chmod +x watchcat-linux`
2. 运行程序：`./watchcat-linux`

## 注意事项

1. 发布前确保：
   - 所有测试通过
   - 更新日志已更新
   - 文档已更新

2. 版本号规范：
   - 遵循语义化版本 (Semantic Versioning)
   - 格式：`MAJOR.MINOR.PATCH`
   - 示例：`v1.2.3`
