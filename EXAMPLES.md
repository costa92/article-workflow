# 使用示例

本文档提供 article-workflow 插件的详细使用示例。

## 快速开始

### 1. 安装插件

```bash
# 添加 marketplace
/plugin marketplace add costa92/article-workflow

# 安装插件
/plugin install article-workflow@article-workflow-marketplace
```

### 2. 配置插件

```bash
# 运行配置向导（推荐）
python scripts/config_wizard.py

# 或手动配置
cp config/config.example.json config/config.json
# 编辑 config/config.json 填入你的 API 密钥
```

### 3. 安装 Python 依赖

```bash
# 安装文章生成依赖
pip install -r skills/article-generator/requirements.txt

# 安装微信格式转换依赖
pip install -r skills/wechat-article-converter/requirements.txt
```

## 基础使用示例

### 示例 1：生成单篇文章

**场景**：快速生成一篇技术博客文章

```bash
# 使用 Claude Code 直接调用
请帮我写一篇关于 Docker 容器化最佳实践的技术文章
```

**输出**：
- 生成 Markdown 文件：`output/docker-best-practices-20250315.md`
- 包含 AI 生成的配图
- 包含代码示例和最佳实践说明

### 示例 2：审查文章质量

**场景**：审查已生成的文章

```bash
# 审查指定文章
审查文章 output/docker-best-practices-20250315.md
```

**输出**：
- 7 维评分报告（可读性、逻辑流、标题吸引力等）
- 详细修改建议
- 发布建议（≥55分可发布）

### 示例 3：转换为微信格式

**场景**：将 Markdown 文章转换为微信公众号格式

```bash
# 转换为微信格式
把 output/docker-best-practices-20250315.md 转成微信格式，用 tech 主题
```

**输出**：
- 微信公众号 HTML 文件
- 本地预览文件
- 可选：上传到微信公众号草稿箱

## 端到端流水线示例

### 示例 4：完整文章创作流水线

**场景**：从选题到发布的完整流程

```bash
# 使用 content-pipeline agent
帮我完成一篇关于 Claude Code 使用技巧的文章，从写作到发布微信公众号
```

**流水线步骤**：
1. **选题规划**（可选）：生成选题卡片
2. **文章生成**：写作出完整文章
3. **内容审查**：7 维评分，≥55分通过
4. **SEO 优化**：生成5个标题方案，选择最佳
5. **格式转换**：转换为微信公众号格式
6. **上传草稿箱**：上传到微信公众号
7. **用户确认**：预览确认后发布

### 示例 5：批量内容生产

**场景**：规划一个月的内容日历

```bash
# 使用 content-planner skill
帮我规划下个月的公众号选题，方向是 AI 开发工具，目标读者是开发者
```

**输出**：
- 月度选题日历（4-8个选题）
- 每个选题的详细说明
- 发布时间建议

## 高级使用示例

### 示例 6：爆款文章拆解

**场景**：学习爆款文章的写作技巧

```bash
# 使用 content-remixer skill
拆解这篇爆款文章 https://example.com/viral-ai-article
```

**输出**：
- 创意积木库（结构模式、叙事手法等）
- 可复用的写作模板
- 直接用于新文章创作

### 示例 7：多平台分发

**场景**：将文章分发到多个平台

```bash
# 使用 content-repurposer skill（需单独安装）
将 output/my-article.md 分发到小红书、知乎和 Twitter
```

**输出**：
- 小红书格式（图片+文案）
- 知乎回答格式
- Twitter 线程格式

### 示例 8：数据分析复盘

**场景**：分析已发布文章的数据表现

```bash
# 使用 content-analytics skill（需单独安装）
分析最近发布的5篇文章的数据表现
```

**输出**：
- 阅读量、点赞、分享数据
- 增长趋势分析
- 内容健康度诊断
- 优化建议

## 使用 CLI 工具

### 示例 9：管理流水线

```bash
# 查看 CLI 帮助
python scripts/pipeline_cli.py --help

# 创建新流水线
python scripts/pipeline_cli.py create

# 列出所有流水线
python scripts/pipeline_cli.py list

# 查看流水线详情
python scripts/pipeline_cli.py show 2025-03-15-001

# 运行流水线
python scripts/pipeline_cli.py run

# 测试组件
python scripts/pipeline_cli.py test

# 清理旧数据
python scripts/pipeline_cli.py cleanup --keep 10
```

### 示例 10：配置向导使用

```bash
# 运行配置向导
python scripts/config_wizard.py

# 向导会逐步引导配置：
# 1. Gemini API 密钥（必填）
# 2. 微信公众号配置（可选）
# 3. 作者信息
# 4. 图片配置
# 5. 高级设置
```

## 故障排除示例

### 问题 1：图片生成失败

**症状**：文章生成时提示图片生成失败

**解决方案**：
```bash
# 1. 检查 Gemini API 密钥
cat config/config.json | grep gemini_api_key

# 2. 测试 API 密钥有效性
curl -X POST https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent \
  -H "Content-Type: application/json" \
  -H "x-goog-api-key: YOUR_API_KEY" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}'

# 3. 临时禁用图片生成
# 编辑 config.json，设置 "auto_generate_images": false
```

### 问题 2：微信上传失败

**症状**：上传到微信公众号草稿箱失败

**解决方案**：
```bash
# 1. 检查 IP 白名单配置
curl ifconfig.me
# 将显示的 IP 添加到微信公众号 IP 白名单

# 2. 检查 API 权限
# 登录 mp.weixin.qq.com → 设置与开发 → 接口权限
# 确保"素材管理"权限已开通

# 3. 测试 API 连接
python scripts/test_wechat_api.py
```

### 问题 3：审查评分低

**症状**：文章审查评分低于55分

**解决方案**：
```bash
# 1. 查看详细评分报告
cat output/review_report_*.md

# 2. 根据建议修改文章
# 重点修复 🔴 标记的问题

# 3. 重新审查
审查文章 output/modified-article.md

# 4. 如果多次重试失败，考虑重新选题
```

## 实际工作流示例

### 个人技术博主工作流

```bash
# 周一：规划周内容
帮我规划本周的3篇技术文章，方向是云原生开发

# 周二：写第一篇文章
写一篇关于 Kubernetes 服务发现的文章

# 周三：审查和优化
审查文章 output/kubernetes-service-discovery.md
把文章转成微信格式，用 tech 主题

# 周四：发布和分发
发布文章到微信公众号
将文章分发到知乎和掘金

# 周五：数据分析
分析本周发布文章的数据表现
```

### 团队内容协作工作流

```bash
# 1. 内容规划会议后
将选题"AI编程助手对比"添加到内容日历

# 2. 作者写作
写一篇对比 GitHub Copilot、Cursor 和 Claude Code 的文章

# 3. 编辑审查
审查文章 output/ai-coding-assistants-comparison.md
提供修改建议

# 4. SEO 优化
优化文章标题和摘要，提高搜索排名

# 5. 多平台发布
主站：发布完整文章
社交媒体：发布精华摘要
社区：发布讨论帖

# 6. 数据跟踪
跟踪各平台的数据表现，优化后续内容
```

## 最佳实践

### 1. 配置管理最佳实践

```bash
# 使用环境变量管理敏感信息
export GEMINI_API_KEY="your-actual-key"
export WECHAT_APPID="your-appid"
export WECHAT_SECRET="your-secret"

# 使用 .env 文件（推荐）
echo "GEMINI_API_KEY=your-key" > .env
echo "WECHAT_APPID=your-appid" >> .env
source .env
```

### 2. 文件组织最佳实践

```bash
# 推荐的文件结构
output/
├── drafts/          # 草稿文件
├── published/       # 已发布文章
├── reviews/         # 审查报告
├── wechat/          # 微信格式文件
└── analytics/       # 数据分析报告

# 使用日期和主题命名
output/published/2025-03-15-docker-best-practices.md
output/wechat/2025-03-15-docker-wechat.html
```

### 3. 质量保证最佳实践

```bash
# 始终进行内容审查
审查文章 文章路径.md

# 使用完整审查模式进行重要文章
审查文章 重要文章.md --mode full

# 定期进行内容复盘
分析最近10篇文章的数据表现

# 建立内容质量标准
# 在 config.json 中设置：
# - passing_score: 55（最低通过分数）
# - auto_fix_issues: true（自动修复可修复问题）
```

### 4. 自动化工作流最佳实践

```bash
# 创建自动化脚本
#!/bin/bash
# auto_publish.sh
文章主题=$1
python scripts/pipeline_cli.py create --topic "$文章主题"
python scripts/pipeline_cli.py run --pipeline-id $(获取最新流水线ID)

# 使用 cron 定时任务
# 每天上午10点检查并发布排期文章
0 10 * * * cd /path/to/article-workflow && ./auto_publish.sh "今日主题"
```

## 扩展和自定义

### 自定义文章模板

```bash
# 1. 创建自定义模板
cp skills/article-generator/templates/default.md skills/article-generator/templates/custom.md

# 2. 修改模板
编辑 custom.md，添加公司品牌、特定格式等

# 3. 使用自定义模板
# 在 config.json 中添加：
"article_generation": {
  "template": "custom"
}
```

### 自定义微信主题

```bash
# 1. 查看现有主题
ls skills/wechat-article-converter/themes/

# 2. 复制并修改主题
cp skills/wechat-article-converter/themes/coffee.py skills/wechat-article-converter/themes/mybrand.py

# 3. 修改主题样式
编辑 mybrand.py，修改颜色、字体、间距等

# 4. 使用自定义主题
把文章转成微信格式，用 mybrand 主题
```

### 集成第三方工具

```bash
# 集成 Git 版本控制
git init
git add output/
git commit -m "添加新文章：$(date +%Y-%m-%d)"

# 集成 CI/CD 流水线
# .github/workflows/publish.yml
name: Publish Article
on:
  push:
    branches: [main]
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: 发布文章
        run: |
          python scripts/pipeline_cli.py run --pipeline-id ${{ secrets.PIPELINE_ID }}
```

## 获取帮助

### 查看文档
```bash
# 查看 README
cat README.md | less

# 查看 agent 文档
cat agents/content-pipeline.md | less

# 查看配置说明
cat config/config.example.json
```

### 调试模式
```bash
# 启用详细日志
export ARTICLE_WORKFLOW_DEBUG=1
python scripts/pipeline_cli.py run

# 查看流水线元数据
find config/pipeline_metadata -name "*.yaml" -exec cat {} \;

# 测试各个组件
python scripts/pipeline_cli.py test
```

### 社区支持
- GitHub Issues: 报告问题和功能请求
- 文档: 查看详细使用说明
- 示例: 参考本文件中的示例