# 贡献指南

感谢您有兴趣为 article-workflow 项目做出贡献！本文档将指导您如何参与项目开发。

## 开发环境设置

### 1. 克隆项目
```bash
git clone https://github.com/costa92/article-workflow.git
cd article-workflow
```

### 2. 创建虚拟环境（推荐）
```bash
python -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows
```

### 3. 安装依赖
```bash
# 安装开发依赖
pip install -r requirements-dev.txt

# 安装项目依赖
pip install -r skills/article-generator/requirements.txt
pip install -r skills/wechat-article-converter/requirements.txt
pip install pyyaml colorama
```

## 开发工作流

### 代码规范

#### 1. 代码风格
- 遵循 **PEP 8** 规范
- 使用 **black** 进行代码格式化
- 使用 **isort** 进行 import 排序

```bash
# 自动格式化
python -m black shared/ scripts/
python -m isort shared/ scripts/
```

#### 2. 类型提示
所有函数都需要完整的类型提示：

```python
def process_article(
    file_path: str,
    config: Optional[Dict[str, Any]] = None
) -> Tuple[bool, str]:
    """处理文章
    
    Args:
        file_path: 文章文件路径
        config: 配置字典
        
    Returns:
        (成功标志, 结果消息)
    """
    # 函数实现
```

#### 3. 文档要求
每个函数都需要 docstring，遵循 Google 风格：

```python
def calculate_score(article: Dict[str, Any]) -> float:
    """计算文章评分
    
    Args:
        article: 文章字典，包含标题、内容等
        
    Returns:
        文章评分（0-100）
        
    Raises:
        ValueError: 如果文章格式不正确
    """
```

### 测试要求

#### 1. 编写测试
所有新功能都需要相应的测试用例：

```python
def test_pipeline_creation():
    """测试流水线创建功能"""
    pipeline = PipelineManager()
    assert pipeline.pipeline_id is not None
    assert pipeline.metadata['status'] == 'pending'
```

#### 2. 运行测试
```bash
# 运行所有测试
python tests/test_integration.py

# 运行特定测试
python -m pytest tests/test_integration.py::TestPipelineManager

# 生成覆盖率报告
python -m pytest tests/ --cov=shared --cov-report=html
```

#### 3. 测试覆盖要求
- 核心功能：100% 覆盖
- 边界条件：必须测试
- 错误处理：必须测试

### 代码质量检查

```bash
# 代码检查
python -m pylint shared/ scripts/

# 类型检查
python -m mypy shared/ --strict

# 安全检查
python -m bandit -r shared/
```

## 贡献流程

### 1. 创建分支
```bash
# 从 develop 分支创建新分支
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
# 或
git checkout -b bugfix/issue-number
```

### 2. 开发功能
- 编写代码
- 添加测试
- 更新文档
- 确保所有测试通过

### 3. 提交代码
```bash
# 添加更改
git add .

# 提交（遵循 Conventional Commits）
git commit -m "feat: 添加新的流水线监控功能"
# 或
git commit -m "fix: 修复配置加载错误 #123"
```

**提交信息格式**：
- `feat:` 新功能
- `fix:` bug修复
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建过程或辅助工具

### 4. 推送分支
```bash
git push origin feature/your-feature-name
```

### 5. 创建 Pull Request
1. 访问 GitHub 仓库
2. 点击 "New Pull Request"
3. 选择你的分支
4. 填写 PR 描述，说明：
   - 解决的问题
   - 实现的功能
   - 测试情况
   - 相关 issue

## 项目结构

### 核心目录
```
article-workflow/
├── shared/              # 共享模块
│   ├── pipeline_manager.py
│   ├── retry_manager.py
│   └── user_confirm.py
├── scripts/            # 工具脚本
│   ├── pipeline_cli.py
│   ├── config_wizard.py
│   └── quick_start.sh
├── tests/              # 测试文件
│   └── test_integration.py
├── config/             # 配置文件
│   ├── config.example.json
│   └── pipeline_metadata/
├── skills/             # 技能包
│   ├── article-generator/
│   └── wechat-article-converter/
└── agents/             # Agent定义
    └── content-pipeline.md
```

### 模块设计原则

#### 1. 单一职责
每个模块只负责一个功能领域：
- `pipeline_manager.py`: 流水线状态管理
- `retry_manager.py`: 重试逻辑管理
- `user_confirm.py`: 用户交互管理

#### 2. 依赖注入
避免硬编码依赖：
```python
# 好：通过参数传递依赖
def process_article(article: str, config_loader: ConfigLoader):
    config = config_loader.load()
    
# 不好：内部创建依赖
def process_article(article: str):
    config_loader = ConfigLoader()  # 硬编码依赖
```

#### 3. 错误处理
使用适当的异常类型：
```python
class PipelineError(Exception):
    """流水线错误基类"""
    pass

class ConfigError(PipelineError):
    """配置错误"""
    pass

class NetworkError(PipelineError):
    """网络错误"""
    pass
```

## 常见任务指南

### 添加新技能
1. 在 `skills/` 目录下创建新目录
2. 创建 `skill.md` 描述文件
3. 添加执行脚本
4. 添加依赖文件 `requirements.txt`
5. 更新文档和测试

### 修改配置系统
1. 更新 `config/config.example.json`
2. 更新 `shared/config_loader.py`
3. 更新相关文档
4. 添加迁移脚本（如果需要）

### 修复 bug
1. 创建最小复现用例
2. 编写测试暴露问题
3. 修复代码
4. 确保所有测试通过
5. 更新相关文档

## 代码审查标准

### 必须满足
- [ ] 代码通过所有测试
- [ ] 代码风格符合规范
- [ ] 有完整的类型提示
- [ ] 有适当的文档
- [ ] 没有引入安全漏洞

### 建议满足
- [ ] 添加了相应的测试
- [ ] 性能没有明显下降
- [ ] 代码可读性好
- [ ] 错误处理完善
- [ ] 向后兼容（如果需要）

## 发布流程

### 版本号规范
遵循语义化版本控制：
- `MAJOR`: 不兼容的 API 修改
- `MINOR`: 向下兼容的功能性新增
- `PATCH`: 向下兼容的问题修正

### 发布步骤
1. 更新 `CHANGELOG.md`
2. 更新版本号
3. 运行完整测试套件
4. 创建发布分支
5. 合并到 main 分支
6. 打标签并发布

## 获取帮助

### 沟通渠道
- **GitHub Issues**: 报告问题和功能请求
- **Discussions**: 技术讨论和问题咨询
- **Pull Requests**: 代码贡献

### 资源链接
- [代码规范](https://www.python.org/dev/peps/pep-0008/)
- [类型提示](https://docs.python.org/3/library/typing.html)
- [测试指南](https://docs.pytest.org/)
- [文档规范](https://google.github.io/styleguide/pyguide.html)

## 行为准则

请遵守以下行为准则：
- 尊重所有贡献者
- 建设性讨论
- 包容不同观点
- 帮助新人入门

感谢您的贡献！🎉