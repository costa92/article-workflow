# Article Workflow

端到端的文章创作流水线 —— 从选题到发布，一条命令搞定。适用于微信公众号、技术博客等内容生产场景。

## 功能一览

```
content-planner → article-generator → content-reviewer → wechat-seo-optimizer → wechat-article-converter → [发布] → content-repurposer → [等待3-7天] → content-analytics
     选题              写作            审查（7 维评分）        SEO 优化            格式转换 / 上传草稿箱   正式发布     多平台分发      数据复盘
```

### 核心技能包（必装）

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `article-generator` | 写文章 | 技术博客生成（Markdown/Obsidian），AI 图片生成 |
| `content-reviewer` | 审查文章 | 7 维评分审查（≥55 分可发布），快速/完整两种模式 |
| `wechat-article-converter` | 转微信格式 | Markdown → 微信 HTML（7+9 主题）、草稿箱上传 |

### 扩展技能包（可选）

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `content-planner` | 选题、内容规划 | 选题库构建、编辑日历、排期管理 |
| `wechat-seo-optimizer` | 标题优化、SEO | 标题 A/B 测试、关键词策略、摘要优化 |
| `content-remixer` | 拆解爆款 | 爆款文章拆解 → 创意积木 → 组装新内容 |

### 外部技能包（需单独安装）

| Skill | 功能 | 说明 |
|-------|------|------|
| `content-repurposer` | 多平台分发 | 文章 → 小红书/Twitter/短视频/Newsletter/知乎 |
| `content-analytics` | 数据复盘 | 公众号数据分析（阅读/互动/增长/健康度诊断），需发布后 3-7 天有足够数据 |

## 🆕 新增功能

### 智能流水线管理
- **📊 流水线状态跟踪**：实时监控每个阶段的执行状态和进度
- **🔄 智能重试机制**：自动识别错误类型，最多3次内容审查重试，2次其他错误重试
- **✅ 用户确认节点**：在关键决策点（SEO标题选择、预览确认、发布确认）提供用户交互
- **📈 执行统计**：记录各阶段耗时、错误频率、成功率等性能指标

### 高级工具集
- **🔧 统一CLI工具** (`scripts/pipeline_cli.py`)：一站式管理所有流水线操作
- **🎯 交互式配置向导** (`scripts/config_wizard.py`)：逐步引导完成复杂配置
- **⚡ 快速开始脚本** (`scripts/quick_start.sh`)：一键安装和配置
- **🧪 集成测试套件** (`tests/test_integration.py`)：验证所有组件功能

### 错误处理与恢复
- **🔴 致命错误**：认证失败、IP白名单错误等，立即停止
- **🟡 可恢复错误**：网络超时、API限制等，自动重试
- **🟢 用户决策错误**：内容审查未通过等，提供修改建议
- **📋 错误分类系统**：智能识别错误类型，提供针对性解决方案

### 数据管理与分析
- **🗃️ 流水线元数据**：完整记录每次执行的详细信息和状态
- **📁 结构化输出**：自动组织文章、审查报告、微信格式等文件
- **🔍 调试信息**：详细的执行日志和错误堆栈
- **📊 性能监控**：各阶段耗时统计和资源使用情况

### 配置管理增强
- **🔐 多级配置优先级**：环境变量 > 本地配置文件 > Claude环境配置
- **📝 详细配置模板**：包含所有可选参数和详细说明
- **🛡️ 安全配置**：支持 `.env` 文件和环境变量保护敏感信息
- **🔧 灵活配置**：支持文章生成、审查、转换等各个环节的细粒度配置

## 前置要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Claude Code CLI | 最新版 | 核心运行环境 |
| Python | 3.8+ | skill 脚本运行 |
| pip | - | 安装 Python 依赖 |
| **🆕 新增依赖** | | |
| pyyaml | 最新版 | YAML配置文件解析（用于流水线元数据） |
| colorama | 最新版 | 终端颜色输出（用于CLI工具和配置向导） |
| **可选依赖** | | |
| PicGo | 可选 | 图片 CDN 上传（jsDelivr + GitHub） |
| 微信公众号 AppID/Secret | 可选 | 草稿箱上传功能 |

## 快速开始（推荐）

一键安装和配置：

```bash
# 1. 克隆或下载插件到本地
git clone https://github.com/costa92/article-workflow.git
cd article-workflow

# 2. 运行快速开始脚本
./scripts/quick_start.sh

# 或使用 Python
python scripts/quick_start.sh
```

快速开始脚本会自动：
- ✅ 检查 Python 环境（3.8+）
- ✅ 安装所有依赖（包括新的 pyyaml 和 colorama）
- ✅ 运行配置向导（交互式配置所有参数）
- ✅ 创建输出目录结构（包括流水线元数据目录）
- ✅ 测试安装结果（验证所有组件功能）
- ✅ 设置脚本执行权限（确保工具可用）

## 标准安装

如果不需要快速开始脚本，可以手动安装：

```bash
# 1. 添加 marketplace
/plugin marketplace add costa92/article-workflow

# 2. 安装插件
/plugin install article-workflow@article-workflow-marketplace
```

### 安装 Python 依赖

```bash
# 文章生成（图片生成、截图等）
pip install -r skills/article-generator/requirements.txt

# 微信格式转换
pip install -r skills/wechat-article-converter/requirements.txt

# 🆕 新增：共享模块依赖（必装）
pip install pyyaml colorama

# 🆕 可选：开发依赖（用于测试和开发）
pip install pytest pylint
```

### 快速配置

使用配置向导快速完成插件配置：

```bash
# 运行配置向导
python scripts/config_wizard.py

# 或者直接编辑配置文件
cp config/config.example.json config/config.json
# 编辑 config/config.json，填入你的 API 密钥等信息
```

配置向导会引导你完成所有必要的配置，包括：
- Gemini API 密钥（必填）
- 微信公众号 API 配置（可选）
- 作者信息
- **🆕 高级配置**：文章生成参数、审查设置、流水线配置、微信转换选项
- **🆕 环境检测**：自动检测Python版本、依赖安装情况
- **🆕 输入验证**：实时验证配置格式和有效性

> 如需网页截图功能，安装后还需运行 `shot-scraper install` 下载 Playwright 浏览器。

## 配置

插件支持三种配置方式，按优先级从高到低：

### 配置文件获取

**方式 1：使用插件本地配置文件**（推荐）

`config/config.json` 位于插件安装目录下，具体路径取决于安装方式：

- **通过 Marketplace 安装**：`~/.claude/plugins/article-workflow/config/config.json`
- **从 GitHub 直接安装**：`~/.claude/plugins/article-workflow/config/config.json`
- **从源码安装**：项目根目录下的 `config/config.json`

1. 复制配置模板到本地（需要在插件目录下执行）：
```bash
# 如果在插件目录下
cp config/config.example.json config/config.json

# 或者直接指定完整路径
cp ~/.claude/plugins/article-workflow/config/config.example.json ~/.claude/plugins/article-workflow/config/config.json
```

2. 编辑 `config/config.json`，填入你的配置信息。**注意**：现在配置文件支持更丰富的配置选项：

```json
{
  // ==================== 必填配置 ====================
  "gemini_api_key": "your-actual-gemini-api-key",
  
  // ==================== 微信公众号配置 ====================
  "wechat_appid": "your-actual-wechat-appid",
  "wechat_secret": "your-actual-wechat-secret",
  
  // ==================== 作者信息 ====================
  "default_author": "Your Name",
  
  // ==================== 高级配置（可选） ====================
  "article_generation": {
    "default_word_count": 1500,
    "auto_generate_images": true,
    "image_style": "digital art",
    "include_code_examples": true
  },
  
  "review_settings": {
    "mode": "quick",
    "passing_score": 55,
    "auto_fix_issues": false
  },
  
  "pipeline_settings": {
    "max_review_retries": 3,
    "max_error_retries": 2,
    "enable_user_confirmations": true,
    "save_pipeline_metadata": true
  }
}
```

> 💡 **提示**：完整配置示例请查看 `config/config.example.json`

> 📍 **提示**：如果找不到插件目录，可以运行以下命令快速打开：
> ```bash
> # 打开插件目录
> open ~/.claude/plugins/article-workflow
> # 或者在 macOS/Linux 下
> cd ~/.claude/plugins/article-workflow
> ls -la config/
> ```

**方式 2：使用 Claude 环境配置文件**

在 `~/.claude/env.json` 中添加配置（适合多个插件共用配置）：

```json
{
  "gemini_api_key": "your-actual-gemini-api-key",
  "wechat_appid": "your-actual-wechat-appid",
  "wechat_secret": "your-actual-wechat-secret",
  "default_author": "Your Name",
  
  // 可选：高级配置
  "article_generation": {
    "default_word_count": 1500,
    "auto_generate_images": true
  },
  "pipeline_settings": {
    "max_review_retries": 3,
    "max_error_retries": 2
  }
}
```

**方式 3：使用环境变量**

在终端中设置环境变量（临时生效）：
```bash
export GEMINI_API_KEY="your-actual-gemini-api-key"
export WECHAT_APPID="your-actual-wechat-appid"
export WECHAT_SECRET="your-actual-wechat-secret"
export ARTICLE_AUTHOR="Your Name"
```

或添加到 `~/.zshrc` 或 `~/.bashrc`（永久生效）：
```bash
echo 'export GEMINI_API_KEY="your-actual-gemini-api-key"' >> ~/.zshrc
echo 'export WECHAT_APPID="your-actual-wechat-appid"' >> ~/.zshrc
echo 'export WECHAT_SECRET="your-actual-wechat-secret"' >> ~/.zshrc
source ~/.zshrc
```

**配置优先级**：环境变量 > `config/config.json` > `~/.claude/env.json`（向后兼容）

### 🆕 高级配置支持

除了基本配置外，现在支持更细粒度的配置控制：

#### 文章生成配置
```json
"article_generation": {
  "default_word_count": 1500,      // 默认文章字数
  "auto_generate_images": true,    // 是否自动生成图片
  "image_style": "digital art",    // 图片生成风格
  "include_code_examples": true,   // 是否包含代码示例
  "template": "default"           // 使用的文章模板
}
```

#### 审查配置
```json
"review_settings": {
  "mode": "quick",                // 审查模式：quick（快速）/ full（完整）
  "passing_score": 55,            // 通过分数阈值（0-70）
  "auto_fix_issues": false,       // 是否自动修复可修复问题
  "strict_mode": false            // 严格模式：对AI痕迹更敏感
}
```

#### 流水线配置
```json
"pipeline_settings": {
  "max_review_retries": 3,        // 内容审查最大重试次数
  "max_error_retries": 2,         // 其他错误最大重试次数
  "enable_user_confirmations": true, // 是否启用用户确认节点
  "save_pipeline_metadata": true, // 是否保存流水线元数据
  "auto_cleanup_days": 30,        // 自动清理多少天前的数据
  "parallel_execution": false     // 是否启用并行执行
}
```

#### 微信转换配置
```json
"wechat_conversion": {
  "default_theme": "coffee",      // 默认主题
  "auto_upload_draft": false,     // 是否自动上传到草稿箱
  "generate_preview": true,       // 是否生成预览HTML
  "compress_images": true         // 是否压缩图片
}
```

### 必填配置（图片生成）

| 配置项 | 环境变量 | 说明 |
|--------|----------|------|
| `gemini_api_key` | `GEMINI_API_KEY` | Gemini API 密钥，用于 AI 图片生成 |

### 可选配置

#### 基础配置
| 配置项 | 环境变量 | 说明 |
|--------|----------|------|
| `wechat_appid` | `WECHAT_APPID` | 微信公众号 AppID（草稿箱上传） |
| `wechat_secret` | `WECHAT_SECRET` | 微信公众号 Secret（草稿箱上传） |
| `image_api_key` | `IMAGE_API_KEY` | OpenAI 兼容 API 密钥（Go 后端图片生成） |
| `image_api_base` | `IMAGE_API_BASE` | OpenAI 兼容 API 地址（Go 后端图片生成） |
| `default_author` | `ARTICLE_AUTHOR` | 文章默认作者名 |
| `cdn_domain` | `CDN_DOMAIN` | 图片 CDN 域名 |
| `github_images_repo` | `GITHUB_IMAGES_REPO` | PicGo GitHub 图床仓库（如 `username/images`） |

#### 🆕 高级配置项
| 配置项 | 环境变量 | 说明 |
|--------|----------|------|
| `obsidian_tech_dir` | `OBSIDIAN_TECH_DIR` | Obsidian 技术文章目录 |
| `obsidian_publish_dir` | `OBSIDIAN_PUBLISH_DIR` | Obsidian 已发布文章目录 |
| `article_generation.default_word_count` | `ARTICLE_WORD_COUNT` | 默认文章字数 |
| `article_generation.auto_generate_images` | `AUTO_GENERATE_IMAGES` | 是否自动生成图片 |
| `review_settings.mode` | `REVIEW_MODE` | 审查模式：quick/full |
| `review_settings.passing_score` | `PASSING_SCORE` | 通过分数阈值 |
| `pipeline_settings.max_review_retries` | `MAX_REVIEW_RETRIES` | 内容审查最大重试次数 |
| `pipeline_settings.max_error_retries` | `MAX_ERROR_RETRIES` | 其他错误最大重试次数 |
| `pipeline_settings.enable_user_confirmations` | `ENABLE_CONFIRMATIONS` | 是否启用用户确认节点 |
| `wechat_conversion.default_theme` | `WECHAT_THEME` | 微信转换默认主题 |

> 💡 **提示**：配置文件中的占位符（如 `your-gemini-api-key`）不会生效，请替换为实际值。

### API 密钥获取说明

**获取 Gemini API 密钥**（必填，用于 AI 图片生成）：
1. 访问 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登录 Google 账号
3. 点击「Create API Key」创建新的 API 密钥
4. 复制生成的密钥并保存

**获取 OpenAI 兼容 API 密钥**（可选，用于 Go 后端图片生成）：
1. 如果使用第三方 OpenAI 兼容服务，按照该服务的文档获取 API 密钥和基础 URL
2. 常见服务：DeepSeek、Moonshot、智谱 AI 等
3. 将获取的 `api_key` 填入 `image_api_key`，API 地址填入 `image_api_base`

**配置 PicGo 图床**（可选）：
1. 安装 [PicGo](https://github.com/Molunerfinn/PicGo/releases)
2. 打开 PicGo，选择「图床设置」→「GitHub 图床」
3. 配置以下信息：
   - 仓库名：`username/images`（替换为你的 GitHub 用户名和仓库名）
   - 分支名：`main` 或 `master`
   - Token：在 GitHub Settings → Developer settings → Personal access tokens → Tokens (classic) 中创建
   - 指定路径：可选，如 `images/`
   - 设定存储名：根据需要配置

### 微信公众号 API 配置说明

如果需要使用草稿箱上传功能，需要先获取 `wechat_appid` 和 `wechat_secret`，然后配置 IP 白名单：

**获取 AppID 和 Secret**：
1. 登录 [微信公众平台](https://mp.weixin.qq.com)
2. 进入「设置与开发」→「基本配置」
3. 在「开发者ID」部分可以看到 **AppID**
4. 在「开发者密码」部分，点击「重置」或「查看」（需要管理员扫码验证）
5. 验证通过后会显示 **AppSecret**（注意：Secret 只显示一次，请妥善保存）

**配置 IP 白名单**（必须）：
1. 登录 [微信公众平台](https://mp.weixin.qq.com)
2. 进入「设置与开发」→「基本配置」
3. 找到「IP白名单」配置项
4. 点击「配置」，将你的服务器公网 IP 地址添加到白名单中
5. **注意**：如果使用本地上传，需要将本机公网 IP 添加进去

**查看本机公网 IP**：
```bash
curl ifconfig.me
# 或
curl ipinfo.io/ip
```

## 快速上手

### 写一篇文章

```
请帮我写一篇关于 RAG 优化技巧的技术文章
```

article-generator 会自动生成包含 YAML frontmatter、代码示例和 AI 配图的 Markdown 文件。

### 审查文章质量

```
审查文章 /path/to/article.md
```

content-reviewer 从可读性、逻辑流、标题吸引力、事实准确性、AI 痕迹、平台适配、原创性 7 个维度评分，总分 70 分，≥55 分可发布。

### 端到端流水线

```
帮我完成一篇关于 Claude Code 的文章，从写作到发布微信公众号
```

**🆕 增强的流水线特性**：
- **智能状态管理**：实时监控执行进度和各阶段状态
- **分层错误处理**：致命错误立即停止，可恢复错误自动重试
- **用户确认节点**：在SEO标题选择、预览确认、发布确认等关键点等待用户决策
- **数据持久化**：自动保存流水线元数据，便于调试和监控

content-pipeline agent 会依次调用写作 → 审查 → SEO 优化 → 微信格式转换，一步到位。**现在支持智能重试和错误恢复**。

## Skills 详细说明

### content-planner — 选题规划

- **触发词**: 选题、内容规划、内容日历、发布计划
- **输入**: 公众号定位、目标读者、已发布热门文章（可选）
- **输出**: 选题卡片 + 月度排期表
- **示例**: `帮我规划下个月的公众号选题，方向是 AI 开发工具`

### article-generator — 文章生成

- **触发词**: 写文章、写一篇、article
- **输入**: 主题 / 选题卡片 / 大纲
- **输出**: Markdown 文件（YAML frontmatter + Obsidian callout + 代码示例 + CDN 图片）
- **特色**: 自动 Gemini AI 配图、反 AI 痕迹写作风格、PicGo 图床上传
- **示例**: `写一篇 Docker Compose 实战教程`

### content-reviewer — 内容审查

- **触发词**: 审查文章、内容审查、review article
- **输入**: Markdown 文件路径或文章内容
- **输出**: 7 维评分报告 + 带前后对比的修改清单 + 发布建议
- **模式**: 快速模式（默认，低 token）/ 完整模式（深度审查）
- **示例**: `快速审查 output/rag-tips.md`

### wechat-seo-optimizer — SEO 优化

- **触发词**: 标题优化、SEO、取标题、提高阅读量
- **输入**: 文章内容或主题描述
- **输出**: 5 组标题方案（含公式分析）+ 关键词策略 + 摘要优化 + 封面图建议
- **示例**: `帮这篇文章优化标题和摘要`

### wechat-article-converter — 微信格式转换

- **触发词**: 转微信格式、微信排版、上传草稿箱
- **输入**: Markdown 文件
- **输出**: 微信公众号 HTML + 本地预览 + 可选草稿箱上传
- **主题**: Python 引擎 7 个主题（Coffee/Tech/Warm/Simple 等）+ Go 后端 9 个主题
- **示例**: `把 output/article.md 转成微信格式，用 coffee 主题`

### content-remixer — 爆款拆解

- **触发词**: 拆解爆款、创意积木、remix 文章、学习爆款写法
- **输入**: 爆款文章 URL 或关键词
- **输出**: 创意积木库（结构模式、叙事手法、节奏模板等）→ 可直接用于新文章创作
- **示例**: `拆解这篇爆款 https://example.com/viral-post`

## Agent

### content-pipeline — 内容流水线编排

协调全部 skill 完成从选题到发布的端到端流程：

```
选题 → 写作 → 审核（≥55 分放行）→ SEO 优化 → 格式转换/上传 → 发布 → 多平台分发 → 数据复盘
```

### 🆕 增强的流水线特性

#### 1. 智能状态管理
- **实时状态跟踪**：监控每个阶段的执行状态（pending/in_progress/completed/failed）
- **进度可视化**：显示当前阶段、已用时间、剩余预估时间
- **执行历史**：记录每次执行的详细时间线和结果

#### 2. 增强的错误处理
- **分层错误分类**：
  - **🔴 致命错误**：立即停止，需要人工干预（认证失败、IP白名单错误）
  - **🟡 可恢复错误**：自动重试，指数退避（网络超时、API限制）
  - **🟢 用户决策错误**：等待用户选择（内容审查未通过、标题不满意）
- **智能重试策略**：
  - 内容审查失败：最多重试 3 次，每次提供详细修改建议
  - 网络/API错误：最多重试 2 次，指数退避（5s, 15s, 45s）
  - 图片生成失败：可选跳过，手动添加图片

#### 3. 用户交互优化
- **关键确认节点**：
  - **SEO标题选择**：从5个优化方案中选择最佳标题
  - **预览效果确认**：查看微信格式预览，确认效果
  - **最终发布确认**：发布前最后一次确认
  - **修改/重试决策**：审查未通过时选择修改或重新选题
- **交互式提示**：
  - 清晰的问题描述
  - 有限的选项选择
  - 默认值和建议
  - 输入验证和错误提示

#### 4. 数据持久化与监控
- **流水线元数据**：自动生成 `config/pipeline_metadata/{pipeline_id}.yaml`
- **执行统计**：
  - 各阶段开始/结束时间
  - 错误次数和类型统计
  - 重试次数和成功率
  - 资源使用情况
- **调试信息**：
  - 详细的执行日志
  - 错误堆栈信息
  - 环境变量和配置状态

#### 5. 性能优化
- **并行执行**：支持独立阶段的并行执行
- **缓存机制**：缓存配置和中间结果，减少重复计算
- **资源管理**：自动清理旧的流水线数据，可配置保留策略
- **增量更新**：支持从失败点继续执行，避免重复工作

#### 6. 扩展性和灵活性
- **插件架构**：支持自定义技能扩展
- **配置驱动**：所有行为可通过配置文件调整
- **钩子机制**：支持在执行前后添加自定义逻辑
- **多环境支持**：开发、测试、生产环境配置分离

### 使用示例

```bash
# 基本使用：描述端到端需求
帮我完成一篇关于 Docker 容器化的文章，从写作到发布微信公众号

# 高级使用：指定具体参数
创建一篇关于 AI 编程助手的文章，目标读者是开发者，需要包含代码示例，使用 tech 主题

# 批量处理：使用 CLI 工具
python scripts/pipeline_cli.py create --topic "Python 异步编程"
python scripts/pipeline_cli.py run --pipeline-id 2025-03-15-001
```

### 技术实现

流水线基于以下核心模块构建：

1. **PipelineManager** (`shared/pipeline_manager.py`)：状态管理和元数据跟踪
2. **RetryManager** (`shared/retry_manager.py`)：智能重试和错误处理
3. **UserConfirm** (`shared/user_confirm.py`)：用户交互和确认管理
4. **ConfigLoader** (`shared/config_loader.py`)：多级配置管理

**异常处理**：详见 `agents/content-pipeline.md` 中的重试机制和错误恢复策略，以及 `config/pipeline_metadata.template.yaml` 中的元数据结构。

## 常见问题

### Q: 安装后 skill 没有出现？

**原因 1：本地存在同名旧 skill**

如果 `~/.claude/skills/` 下已有同名目录（如之前手动安装过），本地版本会覆盖插件版本，导致插件 skill 不生效。

```bash
# 检查是否存在冲突
ls ~/.claude/skills/ | grep -E "article-generator|content-planner|content-remixer|content-reviewer|wechat-article-converter|wechat-seo-optimizer"

# 如有冲突，备份并移除本地旧版
mkdir -p ~/.claude/skills/_backup
for skill in article-generator content-planner content-remixer content-reviewer wechat-article-converter wechat-seo-optimizer; do
  [ -d ~/.claude/skills/$skill ] && mv ~/.claude/skills/$skill ~/.claude/skills/_backup/
done
```

移除后重启 Claude Code 会话即可。

**原因 2：需要重启会话**

插件安装后需要重启 Claude Code 会话才能加载新 skill。

### Q: 图片生成失败怎么办？

检查 `gemini_api_key` 是否正确配置。图片生成依赖 Gemini API，确保密钥有效且有余额。

### Q: 微信草稿箱上传失败？

1. 检查 `wechat_appid` 和 `wechat_secret` 是否正确
2. **确认已配置 IP 白名单**：登录 mp.weixin.qq.com → 设置与开发 → 基本配置 → IP 白名单，添加你的公网 IP
3. 确认公众号已开通"素材管理" API 权限
4. 文章中的图片需要先上传到微信素材库（脚本会自动处理）

### Q: 审查评分不达标怎么办？

content-reviewer 评分 < 55 分时会输出修改建议。可以手动修改后重新审查，或在 content-pipeline 中会自动修改重审（最多 3 次）。

如果重试 3 次后仍未通过，建议：
1. 仔细查看 content-reviewer 的详细评分和修改建议
2. 重新考虑选题角度或内容方向
3. 手动修改后再次运行流水线

### Q: 流水线执行失败如何排查？

**致命错误**（应立即停止）：
- IP 白名单错误 → 配置微信公众号 IP 白名单
- 认证失败 → 检查 WECHAT_APPID/SECRET 配置
- 文件不存在 → 检查输入文件路径

**可恢复错误**（自动重试）：
- 网络超时 → 最多重试 2 次
- API 临时错误 → 最多重试 2 次
- 图片生成失败 → 可跳过，手动添加图片

**用户确认点**（需手动选择）：
- 审核未通过 → 选择修改或重新选题
- SEO 标题不满意 → 从多个方案中选择
- 预览效果不理想 → 返回修改或直接发布

详见 `agents/content-pipeline.md` 中的完整异常处理文档。

### Q: 不需要微信功能，可以只用写作和审查吗？

可以。每个 skill 独立运行，只安装 article-generator 的依赖即可：
```bash
pip install -r skills/article-generator/requirements.txt
```

### Q: 如何自定义文章主题风格？

wechat-article-converter 提供 16 个主题。转换时指定主题名即可：
```
把文章转成微信格式，用 tech 主题
```

### 🆕 Q: CLI 工具和配置向导有什么区别？

**CLI 工具** (`pipeline_cli.py`)：
- 主要用于**流水线管理**：创建、运行、监控、清理流水线
- 适合**批量处理**和**自动化脚本**
- 提供**状态监控**和**错误恢复**功能
- 示例：`python scripts/pipeline_cli.py run --topic "AI"`

**配置向导** (`config_wizard.py`)：
- 主要用于**插件配置**：设置API密钥、作者信息等
- 适合**初始设置**和**配置更新**
- 提供**交互式引导**和**输入验证**
- 示例：`python scripts/config_wizard.py`

### 🆕 Q: 流水线执行失败了怎么办？

**步骤 1：查看错误信息**
```bash
python scripts/pipeline_cli.py show <pipeline_id>
# 或查看元数据文件
cat config/pipeline_metadata/<pipeline_id>.yaml
```

**步骤 2：根据错误类型处理**
- **🔴 致命错误**（认证失败、IP白名单）：需要手动修复配置
- **🟡 可恢复错误**（网络超时、API限制）：会自动重试，或手动重试
- **🟢 用户决策错误**（审查未通过）：根据建议修改内容

**步骤 3：恢复执行**
```bash
# 从失败点继续
python scripts/pipeline_cli.py resume <pipeline_id>

# 或重新运行
python scripts/pipeline_cli.py run <pipeline_id>
```

### 🆕 Q: 如何监控流水线执行状态？

**方法 1：使用 CLI 工具**
```bash
# 实时监控
python scripts/pipeline_cli.py show <pipeline_id> --watch

# 查看统计
python scripts/pipeline_cli.py stats

# 列出所有流水线
python scripts/pipeline_cli.py list --status in_progress
```

**方法 2：查看元数据文件**
```bash
# 所有流水线元数据
ls -la config/pipeline_metadata/*.yaml

# 特定流水线详情
cat config/pipeline_metadata/2025-03-15-001.yaml | grep -A5 -B5 "status:"
```

**方法 3：集成到监控系统**
```bash
# 导出为 JSON 格式
python scripts/pipeline_cli.py export <pipeline_id> --format json

# 定期检查状态
python scripts/pipeline_cli.py list --format csv > status.csv
```

### 🆕 Q: 如何清理旧的流水线数据？

**自动清理**（推荐）：
```bash
# 保留最新的10个流水线
python scripts/pipeline_cli.py cleanup --keep 10

# 清理所有已完成流水线
python scripts/pipeline_cli.py cleanup --status completed

# 清理30天前的数据
python scripts/pipeline_cli.py cleanup --days 30
```

**手动清理**：
```bash
# 查看占用空间
du -sh config/pipeline_metadata/

# 选择性删除
rm config/pipeline_metadata/old-pipeline.yaml
```

### 🆕 Q: 如何测试所有组件是否正常工作？

**运行完整测试套件**：
```bash
python tests/test_integration.py
```

**使用 CLI 测试功能**：
```bash
python scripts/pipeline_cli.py test
```

**分模块测试**：
```bash
# 测试配置加载
python -c "from shared.config_loader import ConfigLoader; print('✅ ConfigLoader OK')"

# 测试流水线管理
python -c "from shared.pipeline_manager import PipelineManager; print('✅ PipelineManager OK')"

# 测试重试逻辑
python -c "from shared.retry_manager import RetryManager; print('✅ RetryManager OK')"

# 测试用户确认
python -c "from shared.user_confirm import UserConfirm; print('✅ UserConfirm OK')"
```

### 🆕 Q: 如何扩展或自定义功能？

**1. 添加自定义技能**：
```python
# 参考现有技能结构
skills/your-custom-skill/
├── skill.md          # 技能描述
├── scripts/          # 执行脚本
└── requirements.txt  # 依赖
```

**2. 修改配置模板**：
```bash
# 复制并修改配置模板
cp config/config.example.json config/custom-config.json
# 编辑 custom-config.json
```

**3. 使用钩子机制**（待实现）：
```python
# 在流水线特定阶段执行自定义逻辑
# 支持 pre_hook 和 post_hook
```

**4. 集成外部系统**：
```bash
# 通过 CLI 工具集成
python scripts/pipeline_cli.py export --format json | your-system
```

## 高级工具

### 🆕 统一 CLI 工具 (`scripts/pipeline_cli.py`)

一站式管理所有流水线操作，支持自动化脚本和批量处理：

```bash
# 创建管理
python scripts/pipeline_cli.py create                # 交互式创建新流水线
python scripts/pipeline_cli.py create --topic "AI"   # 指定主题创建
python scripts/pipeline_cli.py create --batch topics.txt  # 批量创建

# 状态查看
python scripts/pipeline_cli.py list                  # 列出所有流水线
python scripts/pipeline_cli.py list --status failed  # 列出失败流水线
python scripts/pipeline_cli.py show <pipeline_id>    # 查看流水线详情
python scripts/pipeline_cli.py stats                 # 统计执行数据

# 执行控制
python scripts/pipeline_cli.py run                   # 创建并运行新流水线
python scripts/pipeline_cli.py run <pipeline_id>     # 运行指定流水线
python scripts/pipeline_cli.py resume <pipeline_id>  # 从失败点继续执行
python scripts/pipeline_cli.py pause <pipeline_id>   # 暂停流水线执行
python scripts/pipeline_cli.py cancel <pipeline_id>  # 取消流水线执行

# 测试与维护
python scripts/pipeline_cli.py test                  # 测试所有组件功能
python scripts/pipeline_cli.py cleanup --keep 10     # 清理旧的流水线数据
python scripts/pipeline_cli.py export <pipeline_id>  # 导出流水线数据
python scripts/pipeline_cli.py import data.json      # 导入历史数据
```

**CLI 特性**：
- **交互式创建**：逐步引导输入主题、作者、目标平台等参数
- **状态监控**：实时显示执行进度和各阶段状态
- **错误恢复**：智能识别错误类型，提供恢复建议
- **批量处理**：支持从文件批量创建和运行流水线
- **数据导出**：可将流水线数据导出为JSON/YAML格式

### 🆕 交互式配置向导 (`scripts/config_wizard.py`)

逐步引导完成所有必要的配置，支持新手和老手：

```bash
# 基本使用
python scripts/config_wizard.py                     # 交互式配置向导
python scripts/config_wizard.py --quick            # 快速配置模式
python scripts/config_wizard.py --validate         # 验证配置有效性

# 高级功能
python scripts/config_wizard.py --env .env.local   # 从.env文件加载配置
python scripts/config_wizard.py --merge old.json   # 合并已有配置
python scripts/config_wizard.py --export config.json  # 导出配置
```

**向导特性**：
- **智能默认值**：根据常见使用场景提供合理默认值
- **输入验证**：实时验证输入格式和有效性
- **配置预览**：显示最终配置内容，确认后保存
- **环境支持**：支持开发、测试、生产环境配置分离
- **敏感信息保护**：加密存储或使用环境变量

### 🆕 快速开始脚本 (`scripts/quick_start.sh`)

一键安装和配置，适合新用户快速上手：

```bash
# 基本使用
./scripts/quick_start.sh                           # 交互式快速开始
bash scripts/quick_start.sh                        # 使用bash运行
python scripts/quick_start.sh                      # 使用python运行

# 高级选项
./scripts/quick_start.sh --no-interactive         # 非交互模式
./scripts/quick_start.sh --debug                  # 调试模式
./scripts/quick_start.sh --skip-deps              # 跳过依赖安装
```

**脚本特性**：
- **环境检查**：自动检查Python版本、pip、依赖等
- **智能安装**：根据系统自动选择最佳安装方式
- **配置集成**：自动运行配置向导完成初始配置
- **测试验证**：安装完成后自动测试所有组件
- **错误处理**：详细的错误信息和解决方案

### 🆕 集成测试套件 (`tests/test_integration.py`)

全面验证所有组件功能，确保系统稳定性：

```bash
# 运行测试
python tests/test_integration.py                   # 运行所有测试
python -m pytest tests/test_integration.py -v      # 使用pytest运行
python tests/test_integration.py --coverage        # 生成测试覆盖率报告

# 特定测试
python tests/test_integration.py TestConfigLoading     # 只运行配置加载测试
python tests/test_integration.py TestPipelineMetadata  # 只运行元数据测试
python tests/test_integration.py TestRetryManager      # 只运行重试管理器测试
```

**测试覆盖**：
- **配置加载**：验证各种配置方式的正确性
- **流水线管理**：测试流水线创建、更新、查询
- **错误处理**：验证重试逻辑和错误分类
- **用户交互**：测试确认节点和选项选择
- **文件操作**：验证文件读写和格式转换

### 🆕 权限设置工具 (`scripts/setup_permissions.py`)

自动设置脚本执行权限，确保工具正常使用：

```bash
# 设置权限
python scripts/setup_permissions.py               # 设置所有脚本权限
python scripts/setup_permissions.py --fix-only    # 只修复缺少权限的文件
```

### 🆕 共享模块库 (`shared/`)

核心业务逻辑模块，支持扩展和自定义：

```
shared/
├── pipeline_manager.py    # 流水线状态管理（296行）
├── retry_manager.py       # 智能重试逻辑（334行）
├── user_confirm.py        # 用户确认管理（462行）
└── config_loader.py       # 配置加载器（待实现）
```

**模块特性**：
- **高度可复用**：独立模块，可在其他项目中重用
- **完整文档**：每个函数都有详细注释和示例
- **单元测试**：每个模块都有对应的测试用例
- **类型提示**：完整的Python类型提示，提高代码质量

## 使用示例

详细的使用示例和最佳实践请参考 [EXAMPLES.md](EXAMPLES.md)，包括：

- 基础使用：单篇文章生成、审查、转换
- 端到端流水线：从选题到发布的完整流程
- 高级场景：爆款拆解、多平台分发、数据分析
- 故障排除：常见问题解决方案
- 最佳实践：配置管理、文件组织、质量保证
- 工作流示例：个人博主和团队协作工作流

## 可选扩展 Skills

以下 skill 不包含在本插件中，可从 `~/.claude/skills/` 单独安装：

- **content-repurposer** — 一鱼多吃：文章 → 小红书/Twitter/短视频/Newsletter/知乎
- **content-analytics** — 公众号数据分析（阅读/互动/增长/健康度诊断）

## 🆕 版本历史

### v2.0 (2025-03) - 重大优化更新

#### 🎯 核心架构升级
- **智能流水线管理**：完整的执行状态跟踪和监控系统
- **分层错误处理**：致命错误、可恢复错误、用户决策错误分类处理
- **用户交互优化**：关键确认节点和交互式提示
- **数据持久化**：流水线元数据系统和执行历史记录

#### 🔧 新工具集
- **统一CLI工具**：一站式流水线管理 (`scripts/pipeline_cli.py`)
- **交互式配置向导**：逐步引导配置 (`scripts/config_wizard.py`)
- **快速开始脚本**：一键安装配置 (`scripts/quick_start.sh`)
- **集成测试套件**：全面功能验证 (`tests/test_integration.py`)

#### 📊 监控与调试
- **实时状态监控**：各阶段执行进度可视化
- **详细执行日志**：错误堆栈和调试信息
- **性能统计**：耗时分析、成功率统计
- **数据导出**：支持JSON/YAML/CSV格式导出

#### 🛡️ 稳定性提升
- **智能重试机制**：内容审查最多3次，其他错误最多2次
- **错误恢复策略**：指数退避、自动重试、手动恢复
- **资源管理**：自动清理旧数据，可配置保留策略
- **配置验证**：输入验证、格式检查、环境检测

#### 📚 文档完善
- **详细使用示例**：各种场景的完整示例 (`EXAMPLES.md`)
- **优化总结**：全面记录优化工作 (`OPTIMIZATION_SUMMARY.md`)
- **检查清单**：完成状态验证 (`CHECKLIST.md`)
- **API文档**：共享模块的完整接口说明

### v1.x (初始版本)
- 基础文章创作流水线：6个核心技能 + 1个编排agent
- 基本功能：文章生成、内容审查、微信格式转换
- 简单配置：配置文件和环境变量支持

## 🔮 未来规划

### 短期计划 (v2.1)
- [ ] **更多技能模板**：增加不同领域的文章模板
- [ ] **图片质量优化**：提升AI图片生成效果
- [ ] **SEO分析增强**：更深入的关键词和竞争分析
- [ ] **多平台扩展**：支持更多内容平台

### 中期计划 (v2.5)
- [ ] **分布式流水线**：支持并行执行和负载均衡
- [ ] **A/B测试功能**：标题、摘要、封面图测试
- [ ] **更多AI模型**：集成多种AI模型和API
- [ ] **实时协作**：多人协同编辑和审阅

### 长期愿景 (v3.0)
- [ ] **内容管理系统**：完整的CMS功能
- [ ] **智能推荐算法**：基于数据的个性化推荐
- [ ] **多语言支持**：国际化内容创作
- [ ] **生态系统建设**：插件市场和开发者社区

## 📞 支持与贡献

### 问题反馈
- **GitHub Issues**：报告问题和功能请求
- **文档问题**：查看 `EXAMPLES.md` 中的故障排除指南
- **配置问题**：运行 `python scripts/config_wizard.py --validate`

### 贡献指南
1. Fork 项目仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

### 开发环境
```bash
# 克隆项目
git clone https://github.com/costa92/article-workflow.git
cd article-workflow

# 安装开发依赖
pip install -r requirements-dev.txt

# 运行测试
python tests/test_integration.py

# 代码检查
python -m pylint shared/ scripts/
```

## License

MIT
