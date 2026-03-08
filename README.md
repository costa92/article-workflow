# Article Workflow

端到端的文章创作流水线 —— 从选题到发布，一条命令搞定。适用于微信公众号、技术博客等内容生产场景。

## 功能一览

```
content-planner → article-generator → content-reviewer → wechat-seo-optimizer → wechat-article-converter
     选题              写作            审查（7 维评分）        SEO 优化            格式转换 / 上传草稿箱
```

| Skill | 触发词 | 功能 |
|-------|--------|------|
| `content-planner` | `/content-planner`、选题、内容规划 | 选题库构建、编辑日历、排期管理 |
| `article-generator` | `/article-generator`、写文章 | 技术博客生成（Markdown/Obsidian），AI 图片生成 |
| `content-reviewer` | `/content-reviewer`、审查文章 | 7 维评分审查（≥55 分可发布），快速/完整两种模式 |
| `wechat-seo-optimizer` | `/wechat-seo-optimizer`、标题优化 | 标题 A/B 测试、关键词策略、摘要优化 |
| `wechat-article-converter` | `/wechat-article-converter`、转微信格式 | Markdown → 微信 HTML（7+9 主题）、草稿箱上传 |
| `content-remixer` | `/content-remixer`、拆解爆款 | 爆款文章拆解 → 创意积木 → 组装新内容 |

**编排 Agent**: `content-pipeline` — 协调全部 skill 完成端到端流水线

## 前置要求

| 依赖 | 版本 | 说明 |
|------|------|------|
| Claude Code CLI | 最新版 | 核心运行环境 |
| Python | 3.8+ | skill 脚本运行 |
| pip | - | 安装 Python 依赖 |
| PicGo | 可选 | 图片 CDN 上传（jsDelivr + GitHub） |
| 微信公众号 AppID/Secret | 可选 | 草稿箱上传功能 |

## 安装

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
```

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

2. 编辑 `config/config.json`，填入你的配置信息：
```json
{
  "gemini_api_key": "your-actual-gemini-api-key",
  "wechat_appid": "your-actual-wechat-appid",
  "wechat_secret": "your-actual-wechat-secret",
  "default_author": "Your Name"
}
```

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
  "default_author": "Your Name"
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

### 必填配置（图片生成）

### 必填配置（图片生成）

| 配置项 | 环境变量 | 说明 |
|--------|----------|------|
| `gemini_api_key` | `GEMINI_API_KEY` | Gemini API 密钥，用于 AI 图片生成 |

### 可选配置

| 配置项 | 环境变量 | 说明 |
|--------|----------|------|
| `wechat_appid` | `WECHAT_APPID` | 微信公众号 AppID（草稿箱上传） |
| `wechat_secret` | `WECHAT_SECRET` | 微信公众号 Secret（草稿箱上传） |
| `image_api_key` | `IMAGE_API_KEY` | OpenAI 兼容 API 密钥（Go 后端图片生成） |
| `image_api_base` | `IMAGE_API_BASE` | OpenAI 兼容 API 地址（Go 后端图片生成） |
| `default_author` | `ARTICLE_AUTHOR` | 文章默认作者名 |
| `cdn_domain` | `CDN_DOMAIN` | 图片 CDN 域名 |
| `github_images_repo` | `GITHUB_IMAGES_REPO` | PicGo GitHub 图床仓库（如 `username/images`） |

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

content-pipeline agent 会依次调用写作 → 审查 → SEO 优化 → 微信格式转换，一步到位。

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
选题 → 写作 → 审核（≥55 分放行）→ SEO 优化 → 格式转换/上传 → 多平台分发 → 数据复盘
```

使用方式：直接描述你的端到端需求，agent 自动编排各阶段。

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

content-reviewer 评分 < 55 分时会输出修改建议。可以手动修改后重新审查，或在 content-pipeline 中会自动修改重审（最多 3 轮）。

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

## 可选扩展 Skills

以下 skill 不包含在本插件中，可从 `~/.claude/skills/` 单独安装：

- **content-repurposer** — 一鱼多吃：文章 → 小红书/Twitter/短视频/Newsletter/知乎
- **content-analytics** — 公众号数据分析（阅读/互动/增长/健康度诊断）

## License

MIT
