# 贡献指南

欢迎为 WatchCat 项目做出贡献！这个指南将帮助你了解如何参与项目开发。

## 开发流程

1. Fork 项目仓库
2. 创建你的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交你的修改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建一个 Pull Request

## 代码风格

我们使用 [Black](https://github.com/psf/black) 作为 Python 代码格式化工具：

```bash
# 安装 black
poetry add --group dev black

# 格式化代码
poetry run black .
```

### Python 代码风格指南

- 使用 4 个空格缩进
- 行长度限制在 88 个字符以内
- 使用类型注解
- 编写文档字符串
- 遵循 PEP 8 规范

示例：

```python
from typing import Optional, List

class MyClass:
    """MyClass 的简短描述。

    更详细的描述，可以包含多行文本。

    Attributes:
        name: 对象名称
        value: 对象值
    """

    def __init__(self, name: str, value: Optional[int] = None) -> None:
        self.name = name
        self.value = value or 0

    def process_items(self, items: List[str]) -> List[str]:
        """处理项目列表。

        Args:
            items: 要处理的项目列表

        Returns:
            处理后的项目列表
        """
        return [item.upper() for item in items]
```

## 测试

我们使用 pytest 进行测试。所有的测试文件都应该放在 `tests` 目录下：

```bash
# 运行测试
poetry run pytest

# 运行特定测试
poetry run pytest tests/test_window.py

# 运行带覆盖率报告的测试
poetry run pytest --cov=watchcat
```

### 编写测试

```python
import pytest
from watchcat import Window

def test_window_opacity():
    window = Window()
    window.set_opacity(0.5)
    assert window.opacity == 0.5

def test_invalid_opacity():
    window = Window()
    with pytest.raises(ValueError):
        window.set_opacity(2.0)
```

## 文档

使用 MkDocs 构建文档：

```bash
# 安装文档工具
poetry install --with docs

# 本地预览文档
poetry run mkdocs serve

# 构建文档
poetry run mkdocs build
```

### 文档风格指南

1. 使用清晰的标题层次
2. 提供代码示例
3. 解释所有参数和返回值
4. 包含使用场景和注意事项

## 提交消息规范

使用语义化的提交消息：

- `feat`: 新功能
- `fix`: 修复问题
- `docs`: 文档修改
- `style`: 代码格式修改
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

示例：
```
feat(window): 添加窗口拖拽功能

- 实现窗口标题栏拖拽
- 添加边框拖拽调整大小
- 更新相关文档
```

## 版本发布

我们使用语义化版本号：

- MAJOR.MINOR.PATCH
- MAJOR: 不兼容的 API 修改
- MINOR: 向下兼容的功能性新增
- PATCH: 向下兼容的问题修正

## 分支策略

- `main`: 稳定版本分支
- `develop`: 开发分支
- `feature/*`: 特性分支
- `bugfix/*`: 修复分支
- `release/*`: 发布分支

## 问题反馈

1. 使用 GitHub Issues 报告问题
2. 清晰描述问题和复现步骤
3. 提供相关的日志和截图
4. 说明运行环境和版本信息

## 联系我们

- GitHub Issues: [issues](https://github.com/cs-magic-open/watchcat/issues)
- Email: mark@cs-magic.com

## 行为准则

请参阅我们的 [行为准则](CODE_OF_CONDUCT.md)。

## 许可证

通过提交 pull request，你同意你的贡献将使用项目的 MIT 许可证。
