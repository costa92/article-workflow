# A/B Testing Skill

## 🎯 功能概述

实现数据驱动的内容优化，通过科学测试找到最佳的内容元素组合。

## 📋 支持的测试类型

### 核心测试类型（6种）
1. **标题测试** - 不同标题的点击率对比
2. **摘要测试** - 不同摘要的阅读完成率对比  
3. **封面图测试** - 不同封面的吸引度对比
4. **CTA测试** - 不同号召性用语的转化率对比
5. **布局测试** - 不同内容布局的阅读体验对比
6. **发布时间测试** - 不同时间段的发布效果对比

### 测试类型特性对比
| 测试类型 | 测试周期 | 样本需求 | 关键指标 | 优化潜力 |
|----------|----------|----------|----------|----------|
| 标题测试 | 3-7天 | 500-1000次 | 点击率 | ⭐⭐⭐⭐⭐ |
| 摘要测试 | 5-10天 | 1000-2000次 | 阅读完成率 | ⭐⭐⭐⭐ |
| 封面图测试 | 2-5天 | 300-800次 | 视觉吸引度 | ⭐⭐⭐⭐⭐ |
| CTA测试 | 7-14天 | 2000-5000次 | 转化率 | ⭐⭐⭐⭐ |
| 布局测试 | 10-20天 | 5000+次 | 阅读时长 | ⭐⭐⭐ |
| 时间测试 | 14-30天 | 10000+次 | 峰值阅读量 | ⭐⭐⭐ |

## 🚀 快速开始

### 基本使用
```bash
# 创建标题A/B测试
创建标题A/B测试，基线："Docker入门指南"，变体："Docker实战教程" "容器化部署"

# 创建摘要A/B测试  
创建摘要A/B测试，基线："本文介绍Docker基础知识"，变体："掌握Docker核心概念" "从零开始学Docker"

# 获取测试结果
查看标题测试 "title_test_20250319_1430" 的结果

# 获取下一个测试变体
获取测试 "title_test_20250319_1430" 的下一个变体
```

### 常用CLI命令
```bash
# 创建标题测试
python skills/ab-testing/main.py create title --baseline "原始标题" --variations "变体1" "变体2" "变体3"

# 添加测试结果
python skills/ab-testing/main.py result <test_id> <variation_name> --success --metric 0.85

# 获取下一个测试变体
python skills/ab-testing/main.py next <test_id>

# 获取测试结果
python skills/ab-testing/main.py get <test_id>

# 列出所有测试
python skills/ab-testing/main.py list --status running
```

## ⚙️ 配置说明

### 配置文件结构
```json
{
  "ab_testing": {
    "enabled_test_types": ["title", "summary", "cover", "cta"],
    "output_dir": "output/ab_tests",
    
    "default_params": {
      "target_sample_size": 1000,
      "min_duration_days": 7,
      "confidence_level": 0.95,
      "traffic_allocation": "equal",
      "auto_complete_tests": true,
      "generate_reports": true
    },
    
    "test_type_params": {
      "title": {
        "target_sample_size": 500,
        "min_duration_days": 3,
        "confidence_level": 0.9
      },
      "summary": {
        "target_sample_size": 1000,
        "min_duration_days": 5,
        "confidence_level": 0.95
      },
      "cover": {
        "target_sample_size": 300,
        "min_duration_days": 2,
        "confidence_level": 0.9
      },
      "cta": {
        "target_sample_size": 2000,
        "min_duration_days": 14,
        "confidence_level": 0.99
      }
    },
    
    "metrics_config": {
      "primary_metric": "conversion_rate",
      "secondary_metrics": ["click_rate", "engagement_rate", "completion_rate"],
      "thresholds": {
        "minimum_detectable_effect": 0.1,
        "statistical_power": 0.8,
        "significance_level": 0.05
      }
    },
    
    "reporting": {
      "auto_generate": true,
      "formats": ["markdown", "html", "json"],
      "include_charts": true,
      "send_notifications": false
    }
  }
}
```

### 配置优先级
1. 命令行参数
2. 特定测试类型参数
3. 默认参数
4. 系统默认值

## 🔬 测试方法论

### 1. 测试设计原则
- **单一变量原则**：每次只测试一个元素的变化
- **随机分配原则**：用户随机分配到不同变体
- **足够样本原则**：确保统计显著性
- **控制组原则**：保持基线作为对照

### 2. 样本量计算
```python
# 样本量计算公式
def calculate_sample_size(baseline_rate: float, 
                         minimum_detectable_effect: float,
                         power: float = 0.8,
                         alpha: float = 0.05):
    """
    计算A/B测试所需样本量
    
    Args:
        baseline_rate: 基线转化率 (0-1)
        minimum_detectable_effect: 最小可检测效应
        power: 统计功效 (默认0.8)
        alpha: 显著性水平 (默认0.05)
    """
    # 使用标准样本量计算公式
    pass
```

### 3. 统计显著性检验
```python
# Z检验实现
def z_test(conversion_a: int, sample_a: int,
           conversion_b: int, sample_b: int):
    """
    执行Z检验判断两个变体是否有显著差异
    
    Returns:
        z_score: Z分数
        p_value: P值
        is_significant: 是否显著
    """
    pass
```

### 4. 置信区间计算
```python
# 置信区间计算
def confidence_interval(conversions: int, samples: int, 
                       confidence_level: float = 0.95):
    """
    计算转化率的置信区间
    
    Returns:
        (lower_bound, upper_bound): 置信区间上下界
    """
    pass
```

## 📊 测试执行流程

### 1. 测试创建阶段
```
1. 定义测试目标
2. 确定测试类型和变体
3. 计算所需样本量
4. 创建测试配置
5. 设置流量分配
```

### 2. 测试运行阶段
```
1. 用户随机分配到变体
2. 收集用户行为数据
3. 实时更新测试统计
4. 监控测试质量
5. 检查停止条件
```

### 3. 测试分析阶段
```
1. 计算各变体表现
2. 进行统计显著性检验
3. 计算置信区间
4. 确定获胜变体
5. 生成分析报告
```

### 4. 优化实施阶段
```
1. 实施获胜变体
2. 监控优化效果
3. 记录学习经验
4. 规划下一轮测试
```

## 🎯 高级测试场景

### 1. 多变量测试 (MVT)
```bash
# 同时测试标题和封面图
创建多变量测试：
- 标题变体: ["标题A", "标题B", "标题C"]
- 封面变体: ["封面A", "封面B"]
- CTA变体: ["CTA A", "CTA B"]

# 分析交互效应
分析标题和封面的交互效应
```

### 2. 分段测试
```bash
# 针对不同用户群体测试
创建分段测试：
- 新用户: 测试新手友好标题
- 老用户: 测试进阶内容标题
- 付费用户: 测试高级功能标题
```

### 3. 序列测试
```bash
# 连续优化测试
创建序列测试：
1. 第一轮: 测试标题结构
2. 第二轮: 在最佳标题基础上测试关键词
3. 第三轮: 在最佳组合基础上测试情感词
```

### 4. 贝叶斯优化
```bash
# 使用贝叶斯方法优化
使用贝叶斯优化进行标题测试：
- 初始化: 随机测试几个标题
- 迭代: 基于后验分布选择最有希望的标题
- 收敛: 快速找到最优标题
```

## 📈 报告与可视化

### 1. 测试报告内容
```markdown
# A/B测试报告

## 测试概览
- 测试ID: title_test_20250319_1430
- 测试类型: 标题测试
- 测试状态: 已完成
- 测试时长: 5天

## 表现对比
| 变体 | 曝光量 | 点击量 | 点击率 | 提升幅度 | 统计显著性 |
|------|--------|--------|--------|----------|------------|
| 基线 | 1,234 | 123 | 10.0% | - | - |
| 变体A | 1,245 | 186 | 15.0% | +50% | ✅ 显著 |
| 变体B | 1,230 | 135 | 11.0% | +10% | ⚠️ 不显著 |

## 获胜分析
🏆 获胜变体: 变体A
📈 提升幅度: +50% (统计显著)
💡 获胜原因: 包含具体数字和行动动词

## 优化建议
1. 将"变体A"设置为新的基线标题
2. 在类似内容中应用相同模式
3. 进一步测试不同数字和动词组合
```

### 2. 可视化图表
- **转化率对比图**: 柱状图显示各变体表现
- **置信区间图**: 误差棒显示统计不确定性
- **趋势变化图**: 折线图显示随时间变化
- **提升瀑布图**: 显示相对基线的提升幅度
- **样本累积图**: 显示样本积累过程

### 3. 报告类型
- **概要报告**: 关键结果和决策建议
- **详细报告**: 完整数据和分析过程
- **技术报告**: 统计检验详细结果
- **业务报告**: 商业影响和实施计划

## 🛠️ 技术实现

### 核心类结构
```
ABTestManager
├── tests: Dict[str, ABTest]
│   ├── ABTest
│   │   ├── baseline: Variation
│   │   ├── variations: List[Variation]
│   │   ├── test_type: TestType
│   │   └── status: str
│   └── Variation
│       ├── content: str
│       ├── stats: Dict
│       └── results: List
├── config_loader: ConfigLoader
└── report_generator: ReportGenerator
```

### 统计引擎
```
StatisticalEngine
├── sample_size_calculator()
├── z_test_calculator()
├── confidence_interval_calculator()
├── bayesian_analyzer()
└── multivariate_analyzer()
```

### 数据管道
```
DataPipeline
├── data_collector()
├── data_validator()
├── data_aggregator()
├── real_time_updater()
└── historical_analyzer()
```

## 🔍 故障排除

### 常见问题
1. **样本量不足**
   ```bash
   # 检查当前样本量
   python skills/ab-testing/main.py get <test_id> | grep impressions
   
   # 延长测试时间或增加流量
   调整测试参数 --target-sample-size 2000
   ```

2. **统计不显著**
   ```bash
   # 分析原因
   python skills/ab-testing/main.py get <test_id> | grep confidence
   
   # 可能原因：
   # - 变体差异太小
   # - 样本量不足
   # - 数据噪声太大
   ```

3. **测试时间过长**
   ```bash
   # 检查测试进度
   python skills/ab-testing/main.py list --status running
   
   # 加速方法：
   # - 增加测试流量
   # - 降低置信水平要求
   # - 提前结束不显著测试
   ```

### 调试模式
```bash
# 启用详细日志
export AB_TESTING_DEBUG=1
export AB_TESTING_LOG_LEVEL=DEBUG

# 运行测试
python skills/ab-testing/main.py create title --baseline "测试" --variations "A" "B"
```

## 📈 最佳实践

### 1. 测试设计最佳实践
- **明确目标**: 每次测试只解决一个具体问题
- **合理变体**: 变体之间应有明显差异
- **足够样本**: 确保统计功效
- **控制变量**: 保持其他条件一致

### 2. 测试执行最佳实践
- **随机分配**: 确保样本代表性
- **实时监控**: 及时发现异常
- **数据质量**: 确保数据准确性
- **伦理考虑**: 尊重用户隐私

### 3. 测试分析最佳实践
- **统计严谨**: 使用正确的统计方法
- **多维度分析**: 考虑细分群体表现
- **业务解读**: 结合业务背景理解结果
- **谨慎决策**: 避免过度解读随机波动

### 4. 优化循环最佳实践
- **快速迭代**: 小步快跑，持续优化
- **知识积累**: 记录测试经验和洞察
- **规模扩展**: 将成功模式应用到其他场景
- **文化培养**: 建立数据驱动的决策文化

## 🚀 扩展开发

### 1. 添加新测试类型
1. 在 `TestType` 枚举中添加新类型
2. 创建对应的测试创建方法
3. 定义类型特定的参数和指标
4. 更新配置模板和文档

### 2. 集成机器学习
1. 添加预测模型预测测试结果
2. 使用强化学习优化测试策略
3. 实现个性化测试分配
4. 构建智能测试推荐系统

### 3. 实时分析扩展
1. 添加流式数据处理能力
2. 实现实时监控和告警
3. 构建动态测试调整机制
4. 支持大规模并发测试

## 🎉 总结

A/B Testing 技能包提供了：

1. **科学测试框架**: 基于统计学的严谨测试方法
2. **多类型支持**: 6种核心测试类型和扩展能力
3. **智能优化**: 自动停止、获胜判定、报告生成
4. **可视化分析**: 丰富的图表和报告输出
5. **可扩展架构**: 支持新测试类型和高级功能

通过集成这个技能包，article-workflow 实现了：
- **数据驱动优化**: 基于实际测试数据优化内容
- **持续改进循环**: 建立测试-分析-优化的持续循环
- **风险控制**: 小范围测试验证后再大规模应用
- **知识积累**: 积累内容优化的经验和模式

这将使内容创作者能够：
1. **科学决策**: 基于数据而非直觉做出决策
2. **快速迭代**: 快速测试和验证各种优化想法
3. **效果最大化**: 找到最佳的内容元素组合
4. **持续学习**: 建立持续改进的内容优化体系