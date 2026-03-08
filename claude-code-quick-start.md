---
title: "5 分钟上手 Claude Code：终端里的 AI 编程搭档"
date: 2026-03-07
tags: [Claude Code, AI 编程, 命令行工具, Anthropic]
category: AI 工具
status: draft
description: "一条命令装好 Claude Code，5 分钟学会交互模式、管道模式和 CLAUDE.md 项目配置，附常见问题解决。"
---

# 5 分钟上手 Claude Code：终端里的 AI 编程搭档

上周帮同事排查一个跨三个文件的 Bug，我在终端里输了一句话，Claude Code 自己读了代码、定位了问题、改好了文件。整个过程不到两分钟，同事当场问我装的什么。

这篇文章把我的安装和日常用法整理出来，5 分钟跟着做完就能用。

> [!info] 环境说明
> macOS / Linux / Windows 均可，无需预装 Node.js。Claude Code 当前版本 v2.1.x，需要 Claude Pro（$20/月）或 Max 订阅。也支持 API Key 按量付费。

## 安装：一条命令搞定

npm 安装方式已被官方标记为废弃，现在推荐用原生安装器：

```bash
# macOS / Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex
```

装完验证一下：

```bash
claude --version
# 输出类似：2.1.71 (Claude Code)
```

首次运行需要登录：

```bash
claude auth login
```

浏览器会弹出 Anthropic 的授权页面，登录后终端自动完成认证。用 `claude auth status` 确认登录状态。

![Claude Code 终端界面](https://cdn.jsdelivr.net/gh/costa92/article-images/images/claude_code_cover.jpg)

装好登录完，就可以开始用了。Claude Code 有三种用法，覆盖日常开发的大部分场景。

## 三种使用方式

### 交互模式：日常主力

直接输入 `claude` 进入对话界面，像聊天一样描述你的需求。我日常 80% 的使用场景都在这个模式下：

```bash
claude
```

进去之后，你可以说：

- "这个函数有什么 Bug"
- "给这个项目加个 Dockerfile"
- "把这段代码从 JavaScript 重构成 TypeScript"

Claude Code 会自动读取你当前目录的代码，理解项目结构，然后执行修改。每次修改文件前会先问你确认。

### 单次模式：管道利器

加 `-p` 参数，Claude Code 输出结果后直接退出，适合写脚本或串管道。我写部署脚本时经常用这个模式做代码审查：

```bash
# 让 Claude 解释一段代码
claude -p "解释一下 src/auth.ts 的认证流程"

# 结合管道使用
cat error.log | claude -p "分析这段报错日志的根因"
```

### 继续上次对话

用 `-c` 恢复最近一次会话，上下文全都还在：

```bash
claude -c
```

## 四个常用斜杠命令

在交互模式中，这几个命令最常用：

| 命令 | 作用 |
|------|------|
| `/init` | 在项目根目录生成 CLAUDE.md 配置文件 |
| `/model` | 切换模型（Opus、Sonnet、Haiku） |
| `/clear` | 清除当前对话上下文 |
| `/help` | 查看所有可用命令 |

其中 `/init` 生成的 CLAUDE.md 是个关键文件——你可以在里面写项目的编码规范、常用命令、架构说明，Claude Code 每次启动都会读取它，相当于给 AI 一份项目手册。

![CLAUDE.md 配置文件示例](https://cdn.jsdelivr.net/gh/costa92/article-images/images/claude_code_claudemd.jpg)

## 实际效果：一个小例子

假设你有个 Python 项目，想加个命令行参数解析。在项目目录启动 Claude Code：

```bash
cd my-project
claude
```

然后输入：

> 给 main.py 加上 argparse，支持 --port 和 --debug 两个参数

Claude Code 会先读取你的 main.py 理解现有结构，然后生成修改方案。这时终端会显示一个 diff 视图，列出每处要改动的代码。你输入 `y` 确认后，修改直接写入文件。

如果改完发现不对，不用手动回退——在对话里说"回滚刚才的修改"，Claude Code 会自动用 Git 把文件还原到修改前的状态。

## 两个常见问题

刚装完容易碰到这两个问题，提前知道能省不少时间：

**装完输入 `claude` 提示"command not found"**：安装器把二进制文件放在 `~/.local/bin`，但当前终端的 PATH 还没刷新。关掉终端重新打开就行，不需要重新安装。

**对话到一半想换个模型试试**：直接在对话里输入 `/model`，选 Opus（最强但偏慢）或 Haiku（最快），不用退出重进。

## 下一步

装好 Claude Code 后，建议做这两件事：

1. 在你最常用的项目里跑一下 `/init`，让它生成 CLAUDE.md，然后把你的项目规范写进去
2. 搜索「Claude Code MCP 服务器配置」了解如何接入数据库、Slack 等外部工具，这是 Claude Code 的扩展能力核心

---

**参考资料**

- Anthropic 官方文档：搜索「Claude Code documentation anthropic」
- Claude Code GitHub 仓库：搜索「anthropics/claude-code GitHub」
- 安装指南：搜索「Claude Code native installer setup」
