# 安装指南

## 系统要求

### Windows
- Windows 10 或 Windows 11
- Python 3.9+
- Poetry

### macOS
- macOS 10.15+
- Python 3.9+
- Poetry
- Xcode Command Line Tools

### Linux
- 支持X11的Linux发行版
- Python 3.9+
- Poetry
- Qt依赖：
  ```bash
  # Ubuntu/Debian
  sudo apt-get install -y python3-pyqt6
  
  # Fedora
  sudo dnf install python3-qt6
  ```

## 安装步骤

### 1. 安装 Python

访问 [Python官网](https://www.python.org/downloads/) 下载并安装Python 3.9或更高版本。

### 2. 安装 Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 3. 克隆项目

```bash
git clone https://github.com/cs-magic-open/watchcat.git
cd watchcat
```

### 4. 安装依赖

```bash
poetry install
```

### 5. 验证安装

```bash
poetry run python -m watchcat --version
```

## 常见问题

### Poetry安装失败
- 确保Python版本兼容
- 检查网络连接
- 尝试使用镜像源：
  ```bash
  poetry config repositories.tencent https://mirrors.cloud.tencent.com/pypi/simple
  ```

### PyQt6安装问题
- Windows: 确保安装了Visual C++ Build Tools
- Linux: 确保安装了Qt依赖
- macOS: 确保安装了Xcode Command Line Tools

### 权限问题
- Windows: 以管理员身份运行命令提示符
- Linux/macOS: 使用sudo安装系统依赖

## 卸载

```bash
# 删除虚拟环境
poetry env remove python

# 删除项目文件
rm -rf watchcat/
```
