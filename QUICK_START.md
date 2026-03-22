# ⚡ article-workflow 快速开始指南

## 🎯 5分钟上手

### 第1步：环境准备 (1分钟)
```bash
# 克隆项目（如果尚未克隆）
git clone <repository-url>
cd article-workflow

# 检查Python环境
python --version  # 需要 Python 3.8+

# 安装基础依赖
pip install -r requirements.txt  # 如果有requirements.txt
```

### 第2步：配置设置 (2分钟)
```bash
# 运行配置向导
python scripts/config_wizard.py

# 按照提示输入：
# 1. Gemini API密钥 (用于AI内容生成)
# 2. 微信公众号AppID和Secret (可选)
# 3. 输出目录路径 (默认: output/)
# 4. 其他可选配置

# 或者手动创建配置文件
mkdir -p config
cat > config/config.json << 'EOF'
{
  "api": {
    "gemini_api_key": "your-api-key-here"
  },
  "content": {
    "default_author": "你的名字",
    "default_category": "技术教程"
  },
  "paths": {
    "output_dir": "output"
  }
}
EOF
```

### 第3步：快速测试 (1分钟)
```bash
# 测试基本功能
python tests/test_integration.py

# 运行交互式演示
python interactive_demo.py

# 查看可用技能
python scripts/pipeline_cli.py list-skills
```

### 第4步：第一个工作流 (1分钟)
```bash
# 最简单的使用方式：生成一篇文章
python scripts/pipeline_cli.py run article-generator --topic "Python入门教程"

# 或者使用完整流水线
python scripts/pipeline_cli.py run full-pipeline --topic "技术文章示例"
```

## 📋 常用命令速查

### 核心工作流命令
```bash
# 1. 文章生成
python scripts/pipeline_cli.py run article-generator --topic "你的主题"

# 2. 内容审查
python scripts/pipeline_cli.py run content-reviewer --input output/你的文章.md

# 3. SEO优化
python scripts/pipeline_cli.py run wechat-seo-optimizer --input output/你的文章.md

# 4. 微信格式转换
python scripts/pipeline_cli.py run wechat-article-converter --input output/你的文章.md

# 5. 多平台分发
python scripts/pipeline_cli.py run content-repurposer --input output/你的文章.md --platforms wechat zhihu

# 6. 数据分析
python scripts/pipeline_cli.py run content-analytics --article-id 你的文章ID

# 7. A/B测试
python scripts/pipeline_cli.py run ab-testing --test-type title-test --baseline "原始标题"
```

### 快捷命令
```bash
# 一键完成所有步骤
python scripts/pipeline_cli.py run full-pipeline --topic "完整主题"

# 批量处理多篇文章
python scripts/batch_processor.py --input-dir articles/ --output-dir output/

# 查看工作流状态
python scripts/pipeline_cli.py status

# 清理输出目录
python scripts/pipeline_cli.py clean
```

## 🎨 使用场景示例

### 场景1：快速生成技术博客
```bash
# 生成一篇关于Docker的文章
python scripts/pipeline_cli.py run article-generator \
  --topic "Docker容器化部署指南" \
  --style "技术教程" \
  --word-count 2000 \
  --output output/docker-guide.md

# 自动审查和优化
python scripts/pipeline_cli.py run content-reviewer --input output/docker-guide.md
python scripts/pipeline_cli.py run wechat-seo-optimizer --input output/docker-guide.md
```

### 场景2：多平台内容分发
```bash
# 生成文章
python scripts/pipeline_cli.py run article-generator --topic "React性能优化技巧"

# 适配到多个平台
python scripts/pipeline_cli.py run content-repurposer \
  --input output/react-performance.md \
  --platforms wechat zhihu xiaohongshu newsletter \
  --output-dir output/platforms/
```

### 场景3：数据驱动的内容优化
```bash
# 运行A/B测试
python scripts/pipeline_cli.py run ab-testing \
  --test-type title-test \
  --baseline "React性能优化" \
  --variants "10个React性能优化技巧" "React应用性能提升指南" \
  --sample-size 1000

# 分析内容表现
python scripts/pipeline_cli.py run content-analytics \
  --article-id react-performance \
  --period 30-days \
  --output-format html
```

## 🔧 配置文件详解

### 最小配置 (`config/config.json`)
```json
{
  "api": {
    "gemini_api_key": "your-gemini-api-key"
  },
  "content": {
    "default_author": "你的名字"
  }
}
```

### 完整配置示例
```json
{
  "api": {
    "gemini_api_key": "your-gemini-api-key",
    "wechat_appid": "your-wechat-appid",
    "wechat_secret": "your-wechat-secret",
    "image_api_key": "your-image-api-key"
  },
  "content": {
    "default_author": "技术博主",
    "default_category": "技术教程",
    "default_tags": ["技术", "编程", "AI"],
    "writing_styles": {
      "technical": "专业严谨",
      "casual": "轻松易懂",
      "academic": "学术风格"
    }
  },
  "paths": {
    "output_dir": "output",
    "temp_dir": "temp",
    "template_dir": "templates"
  },
  "pipeline": {
    "max_retry_count": 3,
    "review_score_threshold": 55,
    "enable_debug": false,
    "log_level": "INFO"
  },
  "platforms": {
    "wechat": {
      "max_length": 20000,
      "enable_images": true
    },
    "zhihu": {
      "max_length": 50000,
      "tag_count": 5
    },
    "xiaohongshu": {
      "max_length": 1000,
      "image_count": 9
    }
  }
}
```

## 🚀 进阶使用

### 自定义模板
```bash
# 创建自定义文章模板
cp templates/article_template.md my_template.md
# 编辑my_template.md，然后使用：
python scripts/pipeline_cli.py run article-generator --template my_template.md
```

### 批量处理
```bash
# 处理目录下的所有Markdown文件
python scripts/batch_processor.py \
  --input-dir my_articles/ \
  --output-dir processed_articles/ \
  --steps review optimize convert
```

### 集成到其他系统
```python
# 在你的Python代码中使用
import sys
sys.path.append('path/to/article-workflow/shared')

from shared import PipelineManager, ConfigLoader

# 初始化
config = ConfigLoader()
pipeline = PipelineManager("my-pipeline")

# 运行工作流
pipeline.run_workflow("article-generator", {"topic": "你的主题"})
```

## 📊 监控和调试

### 查看日志
```bash
# 启用详细日志
export ARTICLE_WORKFLOW_DEBUG=true
python scripts/pipeline_cli.py run article-generator --topic "测试"

# 查看日志文件
tail -f logs/pipeline.log
```

### 性能监控
```bash
# 查看工作流执行时间
python scripts/pipeline_cli.py run article-generator --topic "测试" --timing

# 生成性能报告
python scripts/performance_report.py --output report.html
```

## 🆘 常见问题

### Q1: 没有API密钥怎么办？
A: 可以先用本地模式，生成基础内容：
```bash
python scripts/pipeline_cli.py run article-generator --topic "测试" --local-mode
```

### Q2: 输出文件在哪里？
A: 默认在 `output/` 目录，可以在配置中修改 `output_dir`。

### Q3: 如何自定义输出格式？
A: 使用 `--output-format` 参数：
```bash
python scripts/pipeline_cli.py run article-generator --topic "测试" --output-format html
```

### Q4: 支持哪些内容平台？
A: 目前支持：微信公众号、知乎、小红书、Twitter、Newsletter、技术博客。

### Q5: 如何添加新的内容平台？
A: 在 `skills/content-repurposer/` 中添加新的平台适配器。

## 📈 下一步学习

### 基础掌握后
1. 阅读 `USAGE_GUIDE.md` - 完整使用指南
2. 查看 `EXAMPLE_USAGE.md` - 详细案例
3. 运行 `interactive_demo.py` - 交互式体验

### 进阶学习
1. 研究 `PROJECT_ANALYSIS.md` - 项目架构分析
2. 查看 `MISSING_FEATURES_IMPLEMENTATION_PLAN.md` - 功能规划
3. 阅读技能包的 `SKILL.md` 文档

### 生产环境部署
1. 配置环境变量管理
2. 设置自动化任务调度
3. 集成到CI/CD流水线
4. 配置监控和告警

## 🎯 立即开始

选择最适合你的方式：

### 方式1：体验完整流程 (推荐)
```bash
./PRACTICAL_EXAMPLE.sh
```

### 方式2：交互式学习
```bash
python interactive_demo.py
```

### 方式3：直接使用
```bash
# 生成你的第一篇文章
python scripts/pipeline_cli.py run article-generator --topic "你的第一个主题"

# 查看生成的文章
cat output/你的文章.md
```

---

**提示**: 如果在使用过程中遇到问题，请查看：
- `README.md` - 项目概述
- `USAGE_GUIDE.md` - 详细使用说明  
- `CHECKLIST.md` - 功能验证清单
- 或提交Issue到项目仓库

**祝你使用愉快！** 🚀