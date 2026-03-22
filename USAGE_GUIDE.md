# article-workflow 使用指南

## 🚀 3分钟快速上手

### 1. 安装插件
```bash
# 添加 marketplace
/plugin marketplace add costa92/article-workflow

# 安装插件
/plugin install article-workflow@article-workflow-marketplace
```

### 2. 一键配置（推荐）
```bash
# 运行快速开始脚本
./scripts/quick_start.sh
```
脚本会自动：
- ✅ 检查 Python 环境
- ✅ 安装所有依赖
- ✅ 运行配置向导
- ✅ 创建必要目录
- ✅ 测试安装结果

### 3. 开始创作
```bash
# 写一篇技术文章
请帮我写一篇关于 Docker 容器化的技术文章

# 或使用完整流水线
帮我完成一篇关于 AI 编程的文章，从写作到发布微信公众号
```

## 📋 核心技能速查表

| 技能 | 触发词 | 功能 | 示例 |
|------|--------|------|------|
| **文章生成** | `写文章`<br>`写一篇`<br>`article` | 生成技术博客文章，包含代码示例和AI配图 | `写一篇关于 Python 异步编程的教程` |
| **内容审查** | `审查文章`<br>`内容审查`<br>`review article` | 7维评分（可读性、逻辑流等），≥55分可发布 | `审查文章 output/tutorial.md` |
| **微信格式转换** | `转微信格式`<br>`微信排版`<br>`上传草稿箱` | Markdown转微信公众号HTML，支持16个主题 | `把文章转成微信格式，用 tech 主题` |
| **SEO优化** | `标题优化`<br>`SEO`<br>`取标题` | 优化文章标题、摘要和关键词，标题A/B测试 | `为这篇文章优化标题和摘要` |
| **多平台分发** | `分发到平台`<br>`多平台分发` | 文章适配到小红书、知乎、Twitter、Newsletter | `将文章分发到小红书、知乎和 Twitter` |
| **数据分析** | `分析数据`<br>`数据复盘` | 公众号数据分析，阅读/互动/增长分析 | `分析最近发布的5篇文章的数据表现` |
| **A/B测试** | `A/B测试`<br>`测试标题`<br>`测试封面` | 标题、摘要、封面图的数据驱动优化测试 | `创建标题A/B测试，基线："原始标题"，变体："变体1" "变体2"` |
| **完整流水线** | `帮我完成一篇...` | 端到端处理：写作→审查→优化→转换→发布→分发→分析 | `帮我完成一篇关于 RAG 的文章，从写作到发布微信公众号` |

## 🔧 常用配置

### 配置文件位置
```
config/config.json                    # 本地配置文件（推荐）
~/.claude/env.json                    # Claude环境配置
环境变量                              # 临时配置
```

### 必填配置项
```json
{
  "gemini_api_key": "your-gemini-api-key"  // AI图片生成
}
```

### 可选配置项
```json
{
  "wechat_appid": "your-wechat-appid",     // 微信草稿箱上传
  "wechat_secret": "your-wechat-secret",   // 微信草稿箱上传
  "default_author": "Your Name",           // 默认作者
  "article_generation": {                   // 文章生成设置
    "default_word_count": 1500,            // 默认字数
    "auto_generate_images": true           // 自动生成图片
  }
}
```

### 🎯 高级配置示例
```json
{
  "review_settings": {                     // 内容审查设置
    "mode": "quick",                       // 审查模式：quick/full
    "passing_score": 55,                   // 通过分数阈值
    "auto_fix_issues": false,              // 是否自动修复可修复问题
    "strict_mode": false                   // 严格模式：对AI痕迹更敏感
  },
  
  "pipeline_settings": {                   // 流水线配置
    "max_review_retries": 3,               // 内容审查最大重试次数
    "max_error_retries": 2,                // 其他错误最大重试次数
    "enable_user_confirmations": true,     // 是否启用用户确认节点
    "save_pipeline_metadata": true,        // 是否保存流水线元数据
    "auto_cleanup_days": 30,               // 自动清理多少天前的数据
    "parallel_execution": false            // 是否启用并行执行
  },
  
  "wechat_conversion": {                   // 微信转换配置
    "default_theme": "coffee",             // 默认主题
    "auto_upload_draft": false,            // 是否自动上传到草稿箱
    "generate_preview": true,              // 是否生成预览HTML
    "compress_images": true                // 是否压缩图片
  }
}
```

## 🛠️ CLI工具常用命令

### 流水线管理
```bash
# 创建新流水线
python scripts/pipeline_cli.py create --topic "文章主题"

# 查看所有流水线
python scripts/pipeline_cli.py list

# 查看流水线详情
python scripts/pipeline_cli.py show <pipeline_id>

# 运行流水线
python scripts/pipeline_cli.py run

# 测试组件功能
python scripts/pipeline_cli.py test
```

### 配置管理
```bash
# 交互式配置向导
python scripts/config_wizard.py

# 验证配置有效性
python scripts/config_wizard.py --validate

# 导出配置
python scripts/config_wizard.py --export config.json
```

## 🎯 典型使用场景

### 场景1：快速写一篇技术文章
```bash
# 1. 写文章
请帮我写一篇关于 Kubernetes 部署最佳实践的文章

# 2. 审查质量
审查文章 output/kubernetes-best-practices.md

# 3. 转换为微信格式
把文章转成微信格式，用 coffee 主题
```

### 场景2：完整内容生产工作流
```bash
# 使用 content-pipeline agent
帮我完成一篇关于 Claude Code 使用技巧的文章，从写作到发布微信公众号
```
**执行流程**：
1. 文章生成 → 2. 内容审查 → 3. SEO优化 → 4. 微信格式转换 → 5. 上传草稿箱 → 6. 用户确认发布

### 场景3：批量内容规划
```bash
# 使用 content-planner skill
帮我规划下个月的公众号选题，方向是 AI 开发工具
```

### 场景4：多平台内容分发
```bash
# 1. 首先完成主要文章的创作
帮我完成一篇关于 Docker 微服务架构的文章

# 2. 安装并配置 content-repurposer skill
# （安装指南见 README.md "外部技能包" 部分）

# 3. 分发到多个平台
将 output/docker-microservices.md 分发到小红书、知乎和 Twitter
```

### 场景5：数据分析与优化
```bash
# 1. 发布文章后等待3-7天收集数据

# 2. 安装并配置 content-analytics skill
# （安装指南见 README.md "外部技能包" 部分）

# 3. 分析数据表现
分析最近发布的5篇文章的数据表现，生成优化建议报告
```

## 🔍 故障排除速查

### 问题1：图片生成失败
```bash
# 检查 API 密钥
cat config/config.json | grep gemini_api_key

# 临时解决方案
# 编辑 config.json，设置 "auto_generate_images": false
```

### 问题2：微信上传失败
```bash
# 查看本机公网 IP
curl ifconfig.me

# 将 IP 添加到微信公众号 IP 白名单
# 登录 mp.weixin.qq.com → 设置与开发 → 基本配置 → IP 白名单
```

### 问题3：审查评分低（<55分）
```bash
# 查看详细评分报告
find output/ -name "review_report_*.md" -exec cat {} \;

# 根据建议修改文章
# 🔴 标记的问题需要优先修复
```

### 问题4：技能不显示
```bash
# 检查是否有本地同名技能冲突
ls ~/.claude/skills/ | grep -E "article-generator|content-reviewer"

# 重启 Claude Code 会话
```

## 📁 输出文件结构

项目生成的文件组织清晰：

```
output/
├── drafts/          # 草稿文件
│   └── 2025-03-15-topic.md
├── published/       # 已发布文章
│   └── 2025-03-15-published.md
├── reviews/         # 审查报告
│   └── review_report_2025-03-15.md
├── wechat/          # 微信格式文件
│   ├── 2025-03-15-wechat.html
│   └── 2025-03-15-preview.html
└── analytics/       # 数据分析报告
    └── 2025-03-15-analytics.md
```

## ⚡ 高效使用技巧

### 1. 使用环境变量（安全推荐）
```bash
# 设置环境变量
export GEMINI_API_KEY="your-actual-key"
export WECHAT_APPID="your-appid"

# 或使用 .env 文件
echo "GEMINI_API_KEY=your-key" > .env
source .env
```

### 2. 自定义文章模板
```bash
# 复制默认模板
cp skills/article-generator/templates/default.md custom.md

# 修改模板后，在 config.json 中设置
"article_generation": {
  "template": "custom"
}
```

### 3. 自动化工作流
```bash
# 创建自动化脚本 auto_publish.sh
#!/bin/bash
python scripts/pipeline_cli.py create --topic "$1"
python scripts/pipeline_cli.py run

# 使用 cron 定时发布
0 10 * * * cd /path/to/article-workflow && ./auto_publish.sh "今日主题"
```

## 📊 性能调优与监控

### 1. 性能优化配置
```json
{
  "pipeline_settings": {
    "auto_cleanup_days": 7,               // 减少数据保留天数，节省空间
    "parallel_execution": true,           // 启用并行执行，提高效率
    "max_workers": 2                      // 限制并发任务数，避免资源耗尽
  }
}
```

### 2. 内存和资源管理
```bash
# 限制并发任务数
export ARTICLE_WORKFLOW_MAX_WORKERS=2

# 减少日志级别，节省资源
export ARTICLE_WORKFLOW_LOG_LEVEL=WARNING

# 启用性能监控
export ARTICLE_WORKFLOW_PERF_MONITOR=1
```

### 3. 实时监控命令
```bash
# 实时查看流水线状态
python scripts/pipeline_cli.py list --watch

# 查看性能统计
python scripts/pipeline_cli.py stats --format json

# 监控资源使用情况
python scripts/pipeline_cli.py monitor --interval 10

# 查看错误日志
find config/pipeline_metadata -name "*.yaml" -exec grep -l "error\|failed" {} \;
```

### 4. 数据清理策略
```bash
# 保留最新的10个流水线
python scripts/pipeline_cli.py cleanup --keep 10

# 清理所有已完成流水线
python scripts/pipeline_cli.py cleanup --status completed

# 清理30天前的数据
python scripts/pipeline_cli.py cleanup --days 30

# 查看占用空间
du -sh config/pipeline_metadata/
```

### 5. 调试和性能分析
```bash
# 启用详细调试模式
export ARTICLE_WORKFLOW_DEBUG=1
export ARTICLE_WORKFLOW_LOG_LEVEL=DEBUG

# 性能分析（需要安装相应工具）
python -m cProfile -o profile.stats scripts/pipeline_cli.py run
python -m pstats profile.stats

# 内存分析
python -m memory_profiler scripts/pipeline_cli.py run
```

## 📞 获取帮助

### 文档资源
```bash
# 查看完整文档
cat README.md | less

# 查看使用示例
cat EXAMPLES.md | less

# 查看配置说明
cat config/config.example.json
```

### 调试模式
```bash
# 启用详细日志
export ARTICLE_WORKFLOW_DEBUG=1
python scripts/pipeline_cli.py run

# 查看流水线元数据
find config/pipeline_metadata -name "*.yaml" | head -5
```

### 社区支持
- **GitHub Issues**：报告问题和功能请求
- **文档**：查看详细使用说明
- **示例**：参考 EXAMPLES.md

## 🎉 开始创作吧！

article-workflow 将复杂的文章创作流程自动化，让你专注于内容本身。从简单的技术博客到完整的微信公众号发布，都能轻松完成。

**记住核心命令**：
```bash
# 快速开始
./scripts/quick_start.sh

# 写文章
请帮我写一篇关于 [你的主题] 的文章

# 完整流程
帮我完成一篇关于 [主题] 的文章，从写作到发布微信公众号
```

祝你创作愉快！🚀