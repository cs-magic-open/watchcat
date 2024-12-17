# 开发环境搭建

## 环境准备

### 1. Python 环境

推荐使用 pyenv 管理 Python 版本：

```bash
# macOS
brew install pyenv

# 安装 Python
pyenv install 3.12.0
pyenv global 3.12.0
```

### 2. Poetry 安装

```bash
curl -sSL https://install.python-poetry.org | python3 -

# 验证安装
poetry --version
```

### 3. 开发工具

推荐使用 VSCode 作为开发环境：

1. 安装 VSCode
2. 安装扩展：
   - Python
   - Pylance
   - Python Test Explorer
   - GitLens
   - Python Docstring Generator

### 4. 克隆项目

```bash
git clone https://github.com/cs-magic-open/watchcat.git
cd watchcat
```

## 项目设置

### 1. 安装依赖

```bash
# 安装所有依赖（包括开发依赖）
poetry install --with dev,test,docs

# 激活虚拟环境
poetry shell
```

### 2. 配置 IDE

#### VSCode 设置

创建 `.vscode/settings.json`：

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.testing.pytestEnabled": true,
    "editor.formatOnSave": true,
    "editor.rulers": [88],
    "files.trimTrailingWhitespace": true
}
```

#### PyCharm 设置

1. 打开项目设置
2. 配置 Python 解释器：选择 Poetry 环境
3. 启用 Black 格式化
4. 配置 pytest 为默认测试运行器

## 开发工作流

### 1. 创建新分支

```bash
git checkout -b feature/your-feature
```

### 2. 运行测试

```bash
# 运行所有测试
poetry run pytest

# 运行特定测试文件
poetry run pytest tests/test_window.py

# 运行带覆盖率的测试
poetry run pytest --cov=watchcat
```

### 3. 代码质量检查

```bash
# 运行 black 格式化
poetry run black .

# 运行 pylint
poetry run pylint watchcat

# 运行 mypy 类型检查
poetry run mypy watchcat
```

### 4. 构建文档

```bash
# 启动文档服务器
poetry run mkdocs serve

# 构建文档
poetry run mkdocs build
```

## 调试技巧

### 使用 VSCode 调试

1. 创建 `.vscode/launch.json`：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": false
        },
        {
            "name": "Python: WatchCat",
            "type": "python",
            "request": "launch",
            "module": "watchcat",
            "console": "integratedTerminal",
            "justMyCode": false
        }
    ]
}
```

### 使用日志调试

```python
from watchcat.logger import logger

def my_function():
    logger.debug("Debug information")
    logger.info("Processing...")
    try:
        # 你的代码
        pass
    except Exception as e:
        logger.error(f"Error occurred: {e}")
```

### 性能分析

```python
import cProfile
import pstats

def profile_code():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # 你的代码
    
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats()
```

## 常见问题

### 1. Poetry 环境问题

```bash
# 重建虚拟环境
poetry env remove python
poetry install

# 更新依赖
poetry update
```

### 2. PyQt 调试

```python
from PyQt6.QtCore import qDebug

qDebug("Debug message")
```

### 3. 内存泄漏调试

```python
from memory_profiler import profile

@profile
def memory_intensive_function():
    # 你的代码
    pass
```

## 性能优化

### 1. 代码优化

```python
# 使用生成器而不是列表
def process_items():
    return (item for item in items)

# 使用 slots
class OptimizedClass:
    __slots__ = ['name', 'value']
```

### 2. PyQt 优化

```python
# 避免频繁更新
self.setUpdatesEnabled(False)
# 进行更新
self.setUpdatesEnabled(True)

# 批量处理信号
self.blockSignals(True)
# 处理
self.blockSignals(False)
```
