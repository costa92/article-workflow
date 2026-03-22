#!/bin/bash
# article-workflow 实战案例脚本
# 演示从选题到分析的完整流程

echo "🚀 开始 article-workflow 实战案例"
echo "========================================"

# 创建输出目录
mkdir -p output
mkdir -p output/images
mkdir -p output/repurposed

echo "📁 输出目录已创建: output/"

echo ""
echo "🎯 第1步: 内容规划"
echo "----------------------------------------"
cat > config/planning_input.json << 'EOF'
{
  "topic": "Python异步编程实战技巧",
  "target_audience": "Python中级开发者",
  "target_platforms": ["wechat", "zhihu", "blog"],
  "keywords": ["async", "await", "asyncio", "并发编程"],
  "expected_word_count": 2500,
  "deadline": "2025-03-25"
}
EOF

echo "✅ 规划配置文件已创建: config/planning_input.json"
echo "   主题: Python异步编程实战技巧"
echo "   目标读者: Python中级开发者"
echo "   目标平台: 微信公众号、知乎、技术博客"

echo ""
echo "✍️  第2步: 文章生成"
echo "----------------------------------------"
cat > output/generated_article.md << 'EOF'
---
title: Python异步编程实战技巧：从入门到精通
author: 技术博主
date: 2025-03-20
tags: [Python, 异步编程, asyncio, 性能优化]
abstract: 深入讲解Python异步编程的核心原理与实战技巧，包含大量代码示例和性能优化建议。
---

# Python异步编程实战技巧：从入门到精通

## 引言
在现代Web开发和数据处理中，异步编程已成为提升应用性能的关键技术。Python通过asyncio库提供了强大的异步支持，本文将详细介绍实际开发中的最佳实践。

## 核心概念
### 1. 协程(Coroutine)
协程是异步编程的基础单元，使用`async def`定义：
```python
import asyncio

async def fetch_data(url):
    # 模拟网络请求
    await asyncio.sleep(1)
    return f"Data from {url}"

async def main():
    data = await fetch_data("https://api.example.com")
    print(data)

asyncio.run(main())
```

### 2. 任务(Task)
任务用于并发执行协程：
```python
async def concurrent_tasks():
    task1 = asyncio.create_task(fetch_data("url1"))
    task2 = asyncio.create_task(fetch_data("url2"))
    
    results = await asyncio.gather(task1, task2)
    print(f"Results: {results}")
```

## 实战技巧

### 1. 错误处理
异步环境中的错误处理需要特别注意：
```python
async def safe_fetch(url):
    try:
        data = await fetch_data(url)
        return data
    except asyncio.TimeoutError:
        print(f"Timeout fetching {url}")
        return None
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None
```

### 2. 性能优化
```python
async def batch_process(urls, batch_size=10):
    """批量处理URL，控制并发数量"""
    results = []
    for i in range(0, len(urls), batch_size):
        batch = urls[i:i+batch_size]
        tasks = [fetch_data(url) for url in batch]
        batch_results = await asyncio.gather(*tasks)
        results.extend(batch_results)
    return results
```

## 常见陷阱与解决方案

### 1. 避免阻塞操作
❌ 错误示例：
```python
async def blocking_operation():
    import time
    time.sleep(5)  # 这会阻塞整个事件循环
```

✅ 正确示例：
```python
async def non_blocking_operation():
    await asyncio.sleep(5)  # 使用异步睡眠
```

### 2. 资源管理
使用`async with`管理异步资源：
```python
async def use_async_resource():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.example.com") as response:
            return await response.text()
```

## 总结
Python异步编程虽然学习曲线较陡，但一旦掌握将大幅提升应用性能。记住几个关键点：
1. 使用`async/await`定义协程
2. 使用`asyncio.create_task()`创建并发任务
3. 避免在协程中使用阻塞操作
4. 合理管理异步资源

通过本文的实战技巧，你应该能够开始在项目中应用异步编程，并享受其带来的性能优势。
EOF

echo "✅ 示例文章已生成: output/generated_article.md"
echo "   字数: ~1200字"
echo "   章节: 引言、核心概念、实战技巧、常见陷阱、总结"

echo ""
echo "🔍 第3步: 内容审查"
echo "----------------------------------------"
cat > output/review_report.json << 'EOF'
{
  "article_id": "python-async-example",
  "review_scores": {
    "readability": 90,
    "logical_flow": 92,
    "technical_accuracy": 94,
    "practicality": 88,
    "structure": 89,
    "engagement": 86,
    "originality": 82
  },
  "total_score": 88.7,
  "status": "approved",
  "feedback": [
    "文章结构清晰，技术内容准确",
    "代码示例实用，具有指导意义",
    "建议增加更多实际案例对比"
  ],
  "improvement_suggestions": [
    "在性能优化部分增加具体数据对比",
    "添加异步编程在不同场景下的应用示例"
  ]
}
EOF

echo "✅ 审查报告已生成: output/review_report.json"
echo "   总分: 88.7/100 ✅ 通过审查"
echo "   建议: 增加数据对比和应用示例"

echo ""
echo "🔎 第4步: SEO优化"
echo "----------------------------------------"
cat > output/seo_optimized.json << 'EOF'
{
  "original_title": "Python异步编程实战技巧：从入门到精通",
  "optimized_titles": [
    "掌握Python异步编程：10个实战技巧提升应用性能",
    "Python异步编程完全指南：从基础到高级应用",
    "异步编程实战：Python高性能并发处理技巧",
    "2025最新Python异步编程最佳实践总结"
  ],
  "meta_description": "深入讲解Python异步编程的核心原理与实战技巧，包含asyncio使用详解、代码示例和性能优化建议，适合中级Python开发者阅读。",
  "keywords": [
    "Python异步编程",
    "asyncio教程",
    "异步并发处理",
    "协程编程",
    "Python性能优化",
    "async/await实战"
  ],
  "optimization_score": 91,
  "ab_testing_recommendation": {
    "test_type": "title_test",
    "variants": 4,
    "sample_size": 3000,
    "duration": "7_days"
  }
}
EOF

echo "✅ SEO优化报告已生成: output/seo_optimized.json"
echo "   优化分数: 91/100"
echo "   A/B测试建议: 4个标题变体，测试7天"

echo ""
echo "🌍 第5步: 多平台适配"
echo "----------------------------------------"
echo "📱 小红书适配..."
cat > output/repurposed/xiaohongshu.md << 'EOF'
# Python异步编程实战技巧 🚀

最近在研究Python异步编程，总结了一些实战技巧分享给大家！

## 🔥 核心技巧

1. **使用async/await定义协程**
   - 避免阻塞操作
   - 合理使用await

2. **并发任务管理**
   ```python
   tasks = [fetch_data(url) for url in urls]
   results = await asyncio.gather(*tasks)
   ```

3. **错误处理要点**
   - 捕获TimeoutError
   - 避免协程泄漏

## 💡 实战建议

- 控制并发数量（建议10-20个）
- 使用异步上下文管理器
- 注意事件循环的生命周期

## 📊 性能对比
同步 vs 异步处理100个请求：
- 同步: 约100秒
- 异步: 约10秒 ⚡️

#Python编程 #异步编程 #技术分享 #程序员 #代码优化
EOF

echo "🎓 知乎适配..."
cat > output/repurposed/zhihu.md << 'EOF'
# Python 异步编程有哪些值得推荐的实战技巧？

## 问题背景
在现代高并发应用开发中，异步编程已成为提升性能的关键技术。Python通过asyncio库提供了完善的异步支持，但实际应用中仍有许多需要注意的技巧。

## 核心技巧详解

### 1. 协程定义与使用
```python
import asyncio

async def fetch_data(url: str) -> str:
    """异步获取数据"""
    # 模拟网络延迟
    await asyncio.sleep(1)
    return f"Data from {url}"
```

**要点**：
- 使用`async def`定义协程函数
- 在协程内部使用`await`等待异步操作
- 避免混用同步阻塞操作

### 2. 并发任务管理
```python
async def batch_fetch(urls: List[str]) -> List[str]:
    """批量并发获取数据"""
    tasks = []
    for url in urls:
        task = asyncio.create_task(fetch_data(url))
        tasks.append(task)
    
    # 等待所有任务完成
    return await asyncio.gather(*tasks)
```

**最佳实践**：
- 使用`asyncio.create_task()`创建任务
- 通过`asyncio.gather()`管理多个并发任务
- 合理设置并发限制，避免资源耗尽

### 3. 异步上下文管理器
```python
import aiohttp

async def fetch_with_session(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

### 4. 性能优化建议
1. **连接复用**：重复使用ClientSession
2. **超时设置**：为所有异步操作设置合理的超时
3. **错误重试**：实现带退避的重试机制
4. **监控指标**：记录关键性能指标

## 实际应用场景

### 场景1：Web爬虫
```python
async def crawl_website(base_url: str):
    # 并发获取页面内容
    # 异步解析数据
    # 批量存储结果
    pass
```

### 场景2：API聚合服务
```python
async def aggregate_apis(api_endpoints: List[str]):
    # 并发调用多个API
    # 合并处理结果
    # 返回统一格式
    pass
```

## 总结
Python异步编程需要理解事件循环机制，掌握协程、任务、Future等核心概念。在实际应用中，要注意错误处理、资源管理和性能优化。通过合理的并发控制和代码组织，可以充分发挥异步编程的优势。

**推荐阅读**：
1. [Python官方asyncio文档](https://docs.python.org/3/library/asyncio.html)
2. [《Python异步编程实战》](https://example.com/book)
3. [GitHub上的异步编程示例](https://github.com/example/async-examples)

---

*欢迎在评论区分享你的异步编程经验和问题！*
EOF

echo "🐦 Twitter适配..."
cat > output/repurposed/twitter.txt << 'EOF'
🚀 Python异步编程实战技巧发布！

✨ 核心要点：
• async/await协程定义
• 并发任务管理
• 错误处理最佳实践
• 性能优化建议

⚡️ 性能对比：异步处理100个请求仅需10秒，比同步快10倍！

#Python #异步编程 #编程技巧 #技术分享
EOF

echo "✅ 多平台适配完成"
echo "   • 小红书: output/repurposed/xiaohongshu.md"
echo "   • 知乎: output/repurposed/zhihu.md"  
echo "   • Twitter: output/repurposed/twitter.txt"

echo ""
echo "📊 第6步: 数据分析"
echo "----------------------------------------"
cat > output/analytics_report.json << 'EOF'
{
  "article_id": "python-async-example",
  "analysis_period": "7_days",
  "overall_performance": {
    "total_views": 8560,
    "average_read_completion": 71.5,
    "share_rate": 7.8,
    "like_rate": 11.3,
    "comment_rate": 3.2
  },
  "platform_performance": {
    "wechat": {
      "views": 5200,
      "read_completion": 68.2,
      "engagement_rate": 16.8,
      "conversion_rate": 4.2
    },
    "zhihu": {
      "views": 2800,
      "read_completion": 75.3,
      "engagement_rate": 21.5,
      "upvote_rate": 18.7
    },
    "xiaohongshu": {
      "views": 560,
      "engagement_rate": 8.4,
      "collect_rate": 12.3
    }
  },
  "audience_insights": {
    "primary_audience": "Python开发者",
    "technical_level": "中级",
    "reading_peak": "工作日 20:00-22:00",
    "popular_sections": ["代码示例", "实战技巧"],
    "drop_off_points": ["理论原理章节"]
  },
  "optimization_recommendations": [
    {
      "priority": "high",
      "action": "采纳A/B测试胜出标题",
      "expected_impact": "点击率提升18%+"
    },
    {
      "priority": "medium",
      "action": "增加更多实操案例",
      "expected_impact": "阅读完成率提升5%"
    },
    {
      "priority": "low",
      "action": "优化小红书的视觉呈现",
      "expected_impact": "平台互动率提升3%"
    }
  ],
  "next_steps": [
    "监控采纳建议后的数据变化",
    "建立内容表现跟踪体系",
    "定期进行内容策略复盘"
  ]
}
EOF

echo "✅ 数据分析报告已生成: output/analytics_report.json"
echo "   总阅读量: 8,560次"
echo "   最高互动率: 21.5% (知乎平台)"
echo "   优化建议: 3项高优先级建议"

echo ""
echo "========================================"
echo "🎉 实战案例完成！"
echo ""
echo "📁 生成的文件:"
echo "1. output/generated_article.md        - 示例文章"
echo "2. output/review_report.json         - 审查报告"
echo "3. output/seo_optimized.json         - SEO优化报告"
echo "4. output/repurposed/xiaohongshu.md  - 小红书版本"
echo "5. output/repurposed/zhihu.md        - 知乎版本"
echo "6. output/repurposed/twitter.txt     - Twitter版本"
echo "7. output/analytics_report.json      - 数据分析报告"
echo ""
echo "🚀 真实使用步骤:"
echo "1. 运行配置向导: python scripts/config_wizard.py"
echo "2. 生成文章: python scripts/pipeline_cli.py run article-generator"
echo "3. 审查文章: python scripts/pipeline_cli.py run content-reviewer"
echo "4. SEO优化: python scripts/pipeline_cli.py run wechat-seo-optimizer"
echo "5. 多平台分发: python scripts/pipeline_cli.py run content-repurposer"
echo "6. 数据分析: python scripts/pipeline_cli.py run content-analytics"
echo ""
echo "💡 提示: 在实际使用时，需要配置API密钥和平台认证信息。"