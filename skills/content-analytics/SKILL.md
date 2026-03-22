# content-analytics Skill

## 🎯 功能概述

深度分析微信公众号等平台的内容表现数据，提供多维度洞察和优化建议。

## 📊 数据源支持

### 核心数据源（3个）
1. **微信后台数据** - CSV/Excel导出文件
2. **流水线元数据** - 本地执行历史和审查数据
3. **手动上传数据** - 自定义格式数据文件

### 数据源特性对比
| 数据源 | 数据类型 | 更新频率 | 分析深度 | 主要用途 |
|--------|----------|----------|----------|----------|
| 微信数据 | 实际表现数据 | 每日/每周 | ⭐⭐⭐⭐⭐ | 实际效果分析 |
| 流水线数据 | 创作过程数据 | 实时 | ⭐⭐⭐⭐ | 质量控制和预测 |
| 文件数据 | 自定义格式 | 手动 | ⭐⭐⭐ | 特定需求分析 |

## 🚀 快速开始

### 基本使用
```bash
# 分析微信后台导出的数据文件
分析微信数据文件 /path/to/wechat_data_2025-03.csv

# 使用流水线数据进行分析
分析最近发布的5篇文章的数据表现

# 直接使用 CLI
python skills/content-analytics/main.py --source wechat --data wechat_stats.csv
```

### 常用命令
```bash
# 分析流水线数据（默认）
python skills/content-analytics/main.py

# 分析微信后台数据
python skills/content-analytics/main.py --source wechat --data wechat_export.csv

# 比较不同数据源
python skills/content-analytics/main.py --compare wechat:wechat_data.csv pipeline:

# 生成详细报告
python skills/content-analytics/main.py --source pipeline --output detailed_report.md
```

## ⚙️ 配置说明

### 配置文件结构
```json
{
  "content_analytics": {
    "enabled_sources": ["wechat", "pipeline"],
    "output_dir": "output/analytics",
    "analysis_period": {
      "start_date": "2025-01-01",
      "end_date": "2025-03-31",
      "use_rolling_window": true,
      "window_size_days": 30
    },
    
    "wechat_data": {
      "expected_columns": ["文章标题", "发布时间", "阅读数", "在看数", "点赞数", "分享数"],
      "date_format": "%Y-%m-%d %H:%M:%S",
      "encoding": "utf-8"
    },
    
    "metrics_config": {
      "primary_metrics": ["read_count", "like_rate", "share_rate"],
      "secondary_metrics": ["comment_count", "favorite_count", "reach_rate"],
      "thresholds": {
        "high_performance": 80,
        "low_performance": 20,
        "avg_performance": 50
      }
    },
    
    "report_config": {
      "format": ["markdown", "html"],
      "include_charts": true,
      "include_raw_data": false,
      "auto_generate": true
    }
  }
}
```

### 配置优先级
1. 命令行参数
2. 配置文件中的 content_analytics 部分
3. 环境变量
4. 默认值

## 🔍 分析维度

### 1. 表现分析
- **阅读量分布**：最小值、最大值、中位数、标准差
- **顶尖文章**：阅读量最高的5篇文章
- **表现波动**：阅读量的稳定性和波动性分析

### 2. 互动分析
- **点赞率**：点赞数/阅读数比例
- **分享率**：分享数/阅读数比例
- **评论率**：评论数/阅读数比例
- **互动率趋势**：各互动指标的上升/下降趋势

### 3. 趋势分析
- **日趋势**：每日阅读量和互动率变化
- **星期趋势**：星期几的表现差异
- **小时趋势**：发布时间的影响
- **月度趋势**：长期表现趋势分析

### 4. 相关性分析
- **审查评分 vs 表现**：质量与实际效果的关系
- **文章长度 vs 互动**：字数对互动率的影响
- **发布时间 vs 阅读量**：发布时机的重要性

## 🎯 优化建议生成

### 1. 基于表现的建议
- **低表现内容优化**：识别表现不佳的文章并提供改进建议
- **高峰发布时间**：推荐最佳发布时间段
- **内容类型调整**：基于数据的受欢迎内容类型建议

### 2. 基于互动的建议
- **提高点赞率**：优化内容结尾、增加价值声明
- **提高分享率**：增加实用技巧、可操作建议
- **提高评论率**：添加讨论问题、投票功能

### 3. 基于趋势的建议
- **季节性调整**：不同季节的内容策略建议
- **星期优化**：针对星期几的内容规划
- **时间窗口优化**：基于小时表现的发布策略

## 📈 报告生成

### 1. 报告类型
- **概要报告**：关键指标总结和快速建议
- **详细报告**：完整分析和深度洞察
- **对比报告**：不同数据源或时间段的对比分析
- **趋势报告**：长期表现趋势和预测

### 2. 输出格式
- **Markdown**：适合技术文档和知识库
- **HTML**：适合网页展示和分享
- **JSON**：适合程序处理和集成
- **CSV**：适合数据分析和电子表格

### 3. 报告内容
```markdown
# 内容数据分析报告

## 📊 数据概览
- 分析文章: 25篇
- 时间范围: 2025-01-01 ~ 2025-03-31
- 总阅读量: 156,820次

## 🏆 表现分析
- 平均阅读量: 6,273次/篇
- 最高阅读量: 18,542次 (标题: "Docker实战指南")
- 互动率: 点赞 2.3%, 分享 1.8%

## 📈 趋势洞察
- 最佳发布时间: 20:00 (平均阅读量 8,420次)
- 最佳发布星期: 周三 (互动率 2.8%)
- 表现上升趋势: +15% (环比上月)

## 🎯 优化建议
1. 优化低表现内容 (<3,000次阅读)
2. 集中在20:00-21:00时段发布
3. 增加周三的内容更新频率
```

## 🛠️ 技术实现

### 核心类结构
```
ContentAnalytics
├── data_sources: Dict[str, DataSource]
│   ├── WeChatDataSource
│   ├── PipelineDataSource
│   └── FileDataSource
├── analyzers: Dict[str, ContentAnalyzer]
└── report_generators: Dict[str, ReportGenerator]

ContentAnalyzer
├── performance_analysis()
├── interaction_analysis()
├── trend_analysis()
└── recommendation_generation()

ReportGenerator
├── generate_markdown_report()
├── generate_html_report()
└── save_report()
```

### 数据处理流程
1. **数据加载**：根据数据源类型加载数据
2. **数据清洗**：处理缺失值、格式转换、异常值处理
3. **指标计算**：计算各类表现和互动指标
4. **趋势分析**：时间序列分析和模式识别
5. **建议生成**：基于分析的优化建议
6. **报告生成**：格式化输出分析结果

### 算法支持
- **统计分析**：描述性统计、相关性分析、假设检验
- **时间序列**：移动平均、季节分解、趋势预测
- **聚类分析**：内容类型聚类、表现群体识别
- **预测模型**：阅读量预测、互动率预测

## 📊 高级分析功能

### 1. A/B测试分析
```python
# 分析标题A/B测试结果
analyze_ab_test(
    variation_a={"title": "标题A", "reads": 5000},
    variation_b={"title": "标题B", "reads": 7500},
    significance_level=0.05
)
```

### 2. 用户画像关联
```python
# 分析不同用户群体的内容偏好
analyze_user_segments(
    data=user_engagement_data,
    segments=["技术新手", "中级开发者", "专家"],
    metrics=["阅读量", "停留时间", "互动率"]
)
```

### 3. 内容健康度评分
```python
# 计算内容健康度综合评分
calculate_content_health_score(
    performance_metrics=performance_data,
    quality_metrics=quality_data,
    engagement_metrics=engagement_data,
    weights={"performance": 0.4, "quality": 0.3, "engagement": 0.3}
)
```

## 🔍 故障排除

### 常见问题
1. **数据格式错误**
   ```bash
   # 验证数据格式
   python skills/content-analytics/main.py --validate wechat_export.csv
   
   # 重新导出数据
   # 微信后台 → 统计 → 图文分析 → 导出CSV
   ```

2. **缺少列或数据**
   ```bash
   # 检查数据列
   head -1 wechat_export.csv | tr ',' '\n'
   
   # 修复配置
   # 在 config.json 中调整 expected_columns
   ```

3. **编码问题**
   ```bash
   # 检查文件编码
   file -I wechat_export.csv
   
   # 转码为UTF-8
   iconv -f GBK -t UTF-8 wechat_export.csv > wechat_export_utf8.csv
   ```

### 调试模式
```bash
# 启用详细日志
export ARTICLE_WORKFLOW_DEBUG=1
export ARTICLE_WORKFLOW_LOG_LEVEL=DEBUG

# 运行分析
python skills/content-analytics/main.py --source wechat --data data.csv
```

## 📈 最佳实践

### 1. 数据采集策略
- **频率**：每周至少导出一次微信数据
- **保存**：保留至少90天的历史数据
- **备份**：定期备份分析结果和原始数据

### 2. 分析周期
- **日报**：关键指标日常监控
- **周报**：表现趋势和优化建议
- **月报**：深度分析和策略调整

### 3. 行动建议优先级
1. **紧急修复**：表现严重下滑、质量缺陷
2. **持续优化**：中等表现内容的逐步改进
3. **战略调整**：基于长期趋势的内容策略调整

### 4. 结果追踪
- **建立基线**：记录改进前的表现数据
- **跟踪变化**：记录每次优化后的效果变化
- **迭代优化**：基于效果调整优化策略

## 🚀 扩展开发

### 1. 添加新数据源
1. 创建新的数据源类，继承 `DataSource`
2. 实现平台特定的数据加载逻辑
3. 在 `ContentAnalytics` 中注册新数据源
4. 更新配置模板和文档

### 2. 自定义分析维度
1. 修改 `ContentAnalyzer` 的分析方法
2. 添加新的分析维度和指标
3. 更新报告生成逻辑
4. 测试分析效果

### 3. 集成机器学习
1. 添加预测模型模块
2. 训练内容表现预测模型
3. 集成到分析流程中
4. 验证预测准确性

## 🎉 总结

content-analytics 技能包提供了：

1. **多数据源支持**：微信后台、流水线元数据、自定义文件
2. **深度分析维度**：表现、互动、趋势、相关性
3. **智能建议生成**：基于数据的优化建议
4. **丰富报告格式**：Markdown、HTML、JSON、CSV
5. **可扩展架构**：支持新数据源、新分析维度、机器学习集成

通过集成这个技能包，article-workflow 实现了：
- **数据驱动决策**：基于实际表现优化内容策略
- **质量效果关联**：分析内容质量与实际效果的关联性
- **趋势预测能力**：识别趋势并预测未来表现
- **持续优化机制**：建立基于数据的持续改进循环

这将使内容创作者能够基于数据做出更明智的决策，持续提升内容表现和影响力。