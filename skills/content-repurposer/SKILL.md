# content-repurposer Skill

## 🎯 功能概述

将同一篇技术文章适配到多个内容平台的格式要求，实现"一鱼多吃"。

## 📋 支持平台

### 核心平台（4个）
1. **小红书** - 图片为主，生活化表述
2. **知乎** - 问答式，专业深度
3. **Twitter** - 简短动态，话题驱动  
4. **Newsletter** - 邮件订阅，结构化内容

### 平台特性对比
| 平台 | 字数限制 | 图片数量 | 风格 | 主要受众 |
|------|----------|----------|------|----------|
| 小红书 | 1000 | 9张 | 生活化、实用 | 年轻用户 |
| 知乎 | 20000 | 5张 | 专业、深入 | 专业人士 |
| Twitter | 280 | 4张 | 简短、动态 | 技术社区 |
| Newsletter | 5000 | 3张 | 正式、结构化 | 订阅用户 |

## 🚀 快速开始

### 基本使用
```bash
# 将文章分发到所有启用的平台
将 output/my-article.md 分发到小红书、知乎和 Twitter

# 或直接使用 CLI
python skills/content-repurposer/main.py output/my-article.md --platforms xiaohongshu zhihu twitter
```

### 常用命令
```bash
# 列出所有支持的平台
python skills/content-repurposer/main.py --list

# 查看平台详细信息
python skills/content-repurposer/main.py --info xiaohongshu

# 指定平台分发
python skills/content-repurposer/main.py article.md --platforms zhihu newsletter
```

## ⚙️ 配置说明

### 配置文件结构
```json
{
  "platform_repurposing": {
    "enabled_platforms": ["xiaohongshu", "zhihu", "twitter", "newsletter"],
    "output_dir": "output/repurposed",
    
    "xiaohongshu": {
      "enable_hashtags": true,
      "default_hashtags": ["#技术分享", "#程序员日常", "#学习笔记"]
    },
    
    "zhihu": {
      "question_style": true,
      "include_references": true
    },
    
    "twitter": {
      "max_threads": 5,
      "add_mentions": true,
      "default_mentions": ["@tech_community"]
    },
    
    "newsletter": {
      "template": "weekly",
      "include_archive_link": true
    }
  }
}
```

### 配置优先级
1. 命令行参数
2. 配置文件中的 platform_repurposing 部分
3. 环境变量
4. 默认值

## 🔧 适配规则

### 小红书适配规则
1. **标题简化**：移除技术术语，增加生活化表述
2. **内容缩短**：长段落简化为要点，适合图片说明
3. **格式优化**：添加小红书常用标签和话题
4. **图片适配**：支持最多9张图片，强调视觉效果

### 知乎适配规则
1. **标题转换**：转换为问题式标题，增加悬念
2. **内容深化**：添加引言和总结，增加专业性
3. **结构优化**：使用知乎特有的标题层级
4. **引用规范**：添加参考文献和扩展阅读

### Twitter适配规则
1. **标题精炼**：限制在280字符内，添加话题标签
2. **内容分线程**：长内容自动分线程
3. **互动优化**：添加@提及和投票
4. **时效性**：强调实时性和动态性

### Newsletter适配规则
1. **标题正式化**：添加【技术周刊】前缀
2. **结构化内容**：添加标准的开头和结尾
3. **链接优化**：添加相关阅读和归档链接
4. **排版标准**：符合邮件阅读习惯

## 🎯 使用场景

### 场景1：内容矩阵搭建
```bash
# 一次性生成所有平台版本
帮我完成一篇关于 Docker 微服务的文章，并分发到所有平台

# 结果：
# - 小红书：生活化的Docker入门指南
# - 知乎：Docker微服务架构深度解析  
# - Twitter：Docker最新特性动态
# - Newsletter：Docker周刊总结
```

### 场景2：平台专属运营
```bash
# 针对特定平台优化
将 output/ai-trends.md 特别优化为小红书版本

# 生成小红书特色的内容：
# - 9张精美技术图解
# - 简短的实用技巧
# - 热门话题标签
```

### 场景3：测试不同平台效果
```bash
# A/B测试不同平台版本
将同一篇文章用不同方式适配，测试哪个平台效果最好

# 跟踪指标：
# - 小红书：点赞、收藏、评论
# - 知乎：赞同、收藏、分享
# - Twitter：转发、点赞、回复
# - Newsletter：打开率、点击率、退订率
```

## 🛠️ 技术实现

### 核心类结构
```
MultiPlatformRepurposer
├── platforms: Dict[str, PlatformAdapter]
│   ├── XiaohongshuAdapter
│   ├── ZhihuAdapter
│   ├── TwitterAdapter
│   └── NewsletterAdapter
├── config_loader: ConfigLoader
└── output_dir: Path
```

### 适配器模式
- **基类**：`PlatformAdapter` 定义标准接口
- **具体适配器**：每个平台实现自己的适配逻辑
- **统一调用**：通过统一接口调用不同平台适配器

### 配置驱动
- 支持多级配置优先级
- 可单独配置每个平台参数
- 支持运行时动态调整

## 📊 输出管理

### 文件结构
```
output/repurposed/
├── article_xiaohongshu.txt    # 小红书版本
├── article_zhihu.md           # 知乎版本  
├── article_twitter.txt        # Twitter线程
├── article_newsletter.md      # Newsletter版本
└── repurpose_results.json     # 处理结果记录
```

### 结果记录
```json
{
  "article": "output/my-article.md",
  "platforms": ["xiaohongshu", "zhihu", "twitter"],
  "output_files": {
    "xiaohongshu": "output/repurposed/article_xiaohongshu.txt",
    "zhihu": "output/repurposed/article_zhihu.md",
    "twitter": "output/repurposed/article_twitter.txt"
  }
}
```

## 🔍 故障排除

### 常见问题
1. **配置加载失败**
   ```bash
   # 检查配置文件
   python scripts/config_wizard.py --validate
   
   # 重新生成配置
   python scripts/config_wizard.py
   ```

2. **内容适配不理想**
   ```bash
   # 手动调整适配规则
   # 修改 skills/content-repurposer/main.py 中的 PlatformAdapter 子类
   ```

3. **平台不支持**
   ```bash
   # 查看支持的平台
   python skills/content-repurposer/main.py --list
   
   # 自定义平台适配器
   # 继承 PlatformAdapter 并实现适配逻辑
   ```

### 调试模式
```bash
# 启用详细日志
export ARTICLE_WORKFLOW_DEBUG=1

# 运行分发
python skills/content-repurposer/main.py article.md --platforms zhihu
```

## 📈 最佳实践

### 1. 内容策略
- **小红书**：突出实用技巧和视觉效果
- **知乎**：注重深度分析和专业视角  
- **Twitter**：强调实时性和社区互动
- **Newsletter**：提供总结性内容和价值提炼

### 2. 发布时间
- 小红书：工作日晚上8-10点
- 知乎：周末上午10-12点
- Twitter：工作日下午3-5点
- Newsletter：周一上午9-10点

### 3. 质量保证
- 分发前进行平台特定优化
- 检查字数限制和格式要求
- 添加平台特色的互动元素
- 确保内容和平台调性匹配

### 4. 数据分析
- 分别跟踪各平台表现
- 对比不同平台的用户互动
- 分析最适合不同内容的平台
- 持续优化分发策略

## 🚀 扩展开发

### 添加新平台
1. 创建新的适配器类，继承 `PlatformAdapter`
2. 实现平台特定的适配逻辑
3. 在 `MultiPlatformRepurposer` 中注册新平台
4. 更新配置模板和文档

### 自定义适配规则
1. 修改现有适配器类的适配方法
2. 添加新的配置参数
3. 更新对应的模板文件
4. 测试适配效果

## 🎉 总结

content-repurposer 技能包提供了：

1. **多平台覆盖**：支持4个主流内容平台
2. **智能适配**：自动根据平台特性优化内容
3. **配置灵活**：可自定义每个平台的适配规则
4. **效果跟踪**：完整的处理记录和结果分析

通过集成这个技能包，article-workflow 实现了真正的"一鱼多吃"，极大提升了内容分发的效率和覆盖范围。