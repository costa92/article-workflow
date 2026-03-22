#!/usr/bin/env python3
"""
article-workflow 交互式演示
让用户体验完整的内容创作工作流程
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Optional

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT / "shared"))

class InteractiveDemo:
    """交互式演示类"""
    
    def __init__(self):
        self.output_dir = PROJECT_ROOT / "demo_output"
        self.output_dir.mkdir(exist_ok=True)
        self.current_article = None
        self.demo_data = self.load_demo_data()
        
    def load_demo_data(self) -> Dict:
        """加载演示数据"""
        return {
            "topics": [
                "Python异步编程实战技巧",
                "React Hooks最佳实践指南",
                "微服务架构设计与实现",
                "机器学习模型部署实战",
                "数据库性能优化技巧"
            ],
            "audiences": [
                "Python中级开发者",
                "前端工程师",
                "后端架构师",
                "数据科学家",
                "全栈开发者"
            ],
            "platforms": ["微信公众号", "知乎", "小红书", "Twitter", "Newsletter"],
            "keywords": {
                "Python": ["异步编程", "asyncio", "协程", "并发", "性能优化"],
                "React": ["Hooks", "状态管理", "组件设计", "性能优化", "TypeScript"],
                "微服务": ["架构设计", "服务发现", "负载均衡", "容错处理", "监控"],
                "机器学习": ["模型部署", "TensorFlow", "PyTorch", "推理优化", "MLOps"],
                "数据库": ["索引优化", "查询调优", "分库分表", "缓存策略", "高可用"]
            }
        }
    
    def print_header(self, title: str):
        """打印标题"""
        print("\n" + "=" * 60)
        print(f"🎯 {title}")
        print("=" * 60)
    
    def print_step(self, step_num: int, title: str):
        """打印步骤"""
        print(f"\n{step_num}. {title}")
        print("-" * 40)
    
    def select_option(self, prompt: str, options: List[str]) -> int:
        """选择选项"""
        print(f"\n{prompt}")
        for i, option in enumerate(options, 1):
            print(f"  {i}. {option}")
        
        while True:
            try:
                choice = int(input(f"\n请选择 (1-{len(options)}): "))
                if 1 <= choice <= len(options):
                    return choice - 1
                else:
                    print(f"请输入 1-{len(options)} 之间的数字")
            except ValueError:
                print("请输入有效的数字")
    
    def step1_content_planning(self):
        """步骤1: 内容规划"""
        self.print_step(1, "内容规划")
        
        # 选择主题
        topic_idx = self.select_option("请选择文章主题:", self.demo_data["topics"])
        topic = self.demo_data["topics"][topic_idx]
        
        # 选择受众
        audience_idx = self.select_option("请选择目标读者:", self.demo_data["audiences"])
        audience = self.demo_data["audiences"][audience_idx]
        
        # 选择平台
        print("\n请选择目标平台 (可多选，输入数字，用逗号分隔):")
        for i, platform in enumerate(self.demo_data["platforms"], 1):
            print(f"  {i}. {platform}")
        
        platform_choices = input("选择平台 (如: 1,3,5): ").strip()
        selected_platforms = []
        for choice in platform_choices.split(","):
            try:
                idx = int(choice.strip()) - 1
                if 0 <= idx < len(self.demo_data["platforms"]):
                    selected_platforms.append(self.demo_data["platforms"][idx])
            except:
                pass
        
        if not selected_platforms:
            selected_platforms = ["微信公众号", "知乎"]
        
        # 获取关键词
        topic_type = topic.split()[0]  # 获取主题的第一个词
        keywords = self.demo_data["keywords"].get(topic_type, ["技术", "教程", "编程"])
        
        # 生成规划结果
        planning_result = {
            "topic": topic,
            "audience": audience,
            "platforms": selected_platforms,
            "keywords": keywords,
            "expected_word_count": 2500,
            "deadline": "2025-03-25",
            "outline": [
                "引言和背景介绍",
                "核心概念解析",
                "实战技巧分享",
                "常见问题与解决方案",
                "总结与展望"
            ]
        }
        
        # 保存规划结果
        planning_file = self.output_dir / "planning_result.json"
        with open(planning_file, 'w', encoding='utf-8') as f:
            json.dump(planning_result, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ 内容规划完成!")
        print(f"   主题: {topic}")
        print(f"   目标读者: {audience}")
        print(f"   目标平台: {', '.join(selected_platforms)}")
        print(f"   关键词: {', '.join(keywords)}")
        print(f"   规划文件: {planning_file}")
        
        return planning_result
    
    def step2_article_generation(self, planning_result: Dict):
        """步骤2: 文章生成"""
        self.print_step(2, "文章生成")
        
        topic = planning_result["topic"]
        keywords = planning_result["keywords"]
        
        print(f"正在生成文章: {topic}...")
        time.sleep(1)  # 模拟生成过程
        
        # 生成示例文章
        article_content = f"""---
title: {topic}：从理论到实践
author: 技术博主
date: 2025-03-20
tags: {keywords}
abstract: 本文深入探讨{topic}的核心概念和实际应用，包含详细的代码示例和最佳实践建议。
---

# {topic}：从理论到实践

## 引言
在现代软件开发中，{topic.split()[0]}技术变得越来越重要。本文将通过实际案例，详细介绍相关技术的核心原理和应用技巧。

## 核心概念
### 1. 基础原理
{topic.split()[0]}技术的核心在于...

### 2. 关键技术点
- 技术点1: 详细说明
- 技术点2: 实际应用
- 技术点3: 注意事项

## 实战技巧
### 代码示例1: 基础用法
```python
def example_function():
    # 示例代码
    return "Hello, World!"
```

### 代码示例2: 高级应用
```python
class AdvancedExample:
    def __init__(self):
        self.data = []
    
    def process_data(self):
        # 数据处理逻辑
        return processed_data
```

## 常见问题与解决方案
### 问题1: 性能瓶颈
**解决方案**: 优化算法，使用缓存策略

### 问题2: 内存泄漏
**解决方案**: 合理管理资源，及时释放

## 总结
通过本文的学习，你应该对{topic}有了更深入的理解。记住几个关键点：
1. 掌握核心原理
2. 熟练应用实战技巧
3. 注意常见问题

## 扩展阅读
- 官方文档链接
- 相关技术文章
- 开源项目示例
"""
        
        # 保存文章
        article_file = self.output_dir / "generated_article.md"
        with open(article_file, 'w', encoding='utf-8') as f:
            f.write(article_content)
        
        # 生成代码示例文件
        code_file = self.output_dir / "code_examples.py"
        with open(code_file, 'w', encoding='utf-8') as f:
            f.write("""# 代码示例文件

def main_example():
    \"\"\"主要示例函数\"\"\"
    print("Hello from code example!")
    
    # 模拟数据处理
    data = [1, 2, 3, 4, 5]
    result = sum(data)
    print(f"计算结果: {result}")
    
    return result

if __name__ == "__main__":
    main_example()
""")
        
        print(f"\n✅ 文章生成完成!")
        print(f"   文章文件: {article_file} (~{len(article_content)}字符)")
        print(f"   代码示例: {code_file}")
        print(f"   包含: 5个章节，2个代码示例，完整结构")
        
        self.current_article = article_content
        return article_content
    
    def step3_content_review(self, article_content: str):
        """步骤3: 内容审查"""
        self.print_step(3, "内容审查")
        
        print("正在审查文章质量...")
        time.sleep(1)  # 模拟审查过程
        
        # 模拟审查评分
        review_scores = {
            "readability": 88,
            "logical_flow": 92,
            "technical_accuracy": 90,
            "practicality": 85,
            "structure": 89,
            "engagement": 87,
            "originality": 82
        }
        
        total_score = sum(review_scores.values()) / len(review_scores)
        
        # 生成审查报告
        review_report = {
            "article_id": f"demo-{int(time.time())}",
            "review_scores": review_scores,
            "total_score": round(total_score, 1),
            "status": "approved" if total_score >= 55 else "rejected",
            "feedback": [
                "文章结构清晰，逻辑连贯",
                "技术内容准确，具有参考价值",
                "代码示例实用，易于理解",
                "建议增加更多实际案例"
            ],
            "improvement_suggestions": [
                "在实战技巧部分增加更多代码示例",
                "优化部分章节的过渡衔接",
                "考虑添加性能对比数据"
            ]
        }
        
        # 保存审查报告
        review_file = self.output_dir / "review_report.json"
        with open(review_file, 'w', encoding='utf-8') as f:
            json.dump(review_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ 内容审查完成!")
        print(f"   总分: {review_report['total_score']}/100")
        print(f"   状态: {review_report['status']}")
        print(f"   审查报告: {review_file}")
        
        if review_report['status'] == 'approved':
            print("   🎉 文章通过审查，可以继续下一步!")
        else:
            print("   ⚠️ 文章未通过审查，需要修改后重新审查")
        
        return review_report
    
    def step4_seo_optimization(self, article_content: str):
        """步骤4: SEO优化"""
        self.print_step(4, "SEO优化")
        
        print("正在分析文章SEO表现...")
        time.sleep(1)
        
        # 提取标题（假设第一行是标题）
        lines = article_content.split('\n')
        original_title = None
        for line in lines:
            if line.startswith('title:'):
                original_title = line.replace('title:', '').strip()
                break
        
        if not original_title:
            original_title = "技术文章示例"
        
        # 生成SEO优化建议
        seo_optimized = {
            "original_title": original_title,
            "optimized_titles": [
                f"{original_title} - 完整实战指南",
                f"掌握{original_title.split('：')[0]}的10个关键技巧",
                f"2025最新{original_title}完全解析",
                f"从入门到精通：{original_title.split('：')[0]}实战"
            ],
            "meta_description": f"深入讲解{original_title.split('：')[0]}的核心原理和实际应用，包含详细的技术分析和代码示例，适合开发者学习和参考。",
            "keywords": ["技术教程", "编程技巧", "实战指南", "最佳实践"],
            "optimization_score": 89,
            "ab_testing_recommendation": {
                "test_type": "title_test",
                "variants": 4,
                "sample_size": 2000,
                "duration": "5_days",
                "expected_improvement": "15-25%"
            }
        }
        
        # 保存SEO报告
        seo_file = self.output_dir / "seo_report.json"
        with open(seo_file, 'w', encoding='utf-8') as f:
            json.dump(seo_optimized, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ SEO优化完成!")
        print(f"   优化分数: {seo_optimized['optimization_score']}/100")
        print(f"   建议A/B测试: {len(seo_optimized['optimized_titles'])}个标题变体")
        print(f"   SEO报告: {seo_file}")
        
        return seo_optimized
    
    def step5_multi_platform_adaptation(self, article_content: str, platforms: List[str]):
        """步骤5: 多平台适配"""
        self.print_step(5, "多平台适配")
        
        print(f"正在适配到 {len(platforms)} 个平台...")
        time.sleep(1)
        
        adapted_versions = {}
        
        for platform in platforms:
            print(f"  适配 {platform}...")
            time.sleep(0.5)
            
            if platform == "微信公众号":
                content = f"""# 微信公众号版本

{article_content.split('---')[2].split('#')[1]}

## 文章特点
- 专业的技术内容
- 详细的代码示例
- 实用的技巧分享

## 阅读提示
建议在电脑端阅读，方便查看代码示例。

## 互动环节
欢迎在评论区分享你的经验和问题！

---
*本文由article-workflow自动生成*"""
                
            elif platform == "知乎":
                content = f"""# 知乎专业版本

## 问题：{article_content.split('---')[2].split('#')[1].split('：')[0]}有哪些值得学习的技巧？

### 背景
随着技术的发展，{article_content.split('---')[2].split('#')[1].split('：')[0]}变得越来越重要。

### 核心内容
{article_content.split('## 核心概念')[1].split('##')[0]}

### 详细分析
{article_content.split('## 实战技巧')[1].split('##')[0]}

### 总结
掌握这些技巧可以显著提升开发效率。

---
**相关推荐**：
- 官方文档
- 开源项目
- 进阶教程

*欢迎点赞、收藏、关注*"""
                
            elif platform == "小红书":
                content = f"""# 小红书版本 📚

{article_content.split('---')[2].split('#')[1]}

## 核心要点 ✨
1. 掌握基础原理
2. 学习实战技巧
3. 避免常见错误

## 实用技巧 💡
- 技巧1：简单易学
- 技巧2：效果明显
- 技巧3：节省时间

## 效果对比 📊
使用前 vs 使用后
效率提升：200% ⚡️

#技术分享 #编程技巧 #学习笔记 #干货分享"""
                
            elif platform == "Twitter":
                content = f"""🚀 技术分享：{article_content.split('---')[2].split('#')[1]}

✨ 核心要点：
• 掌握关键原理
• 应用实战技巧
• 优化开发流程

⚡️ 效率提升显著！

#Tech #Programming #Coding #Developer"""
                
            else:  # Newsletter或其他平台
                content = f"""# 技术通讯：{article_content.split('---')[2].split('#')[1]}

## 本期要点
{article_content.split('## 核心概念')[1].split('##')[0][:500]}...

## 完整阅读
阅读完整文章请访问：[文章链接]

## 下期预告
下期我们将分享更多技术干货！

---
*感谢阅读本期技术通讯*"""
            
            # 保存适配版本
            platform_file = self.output_dir / f"{platform}_version.txt"
            with open(platform_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            adapted_versions[platform] = {
                "file": str(platform_file),
                "length": len(content),
                "format": "适合平台特点的格式"
            }
        
        # 保存适配报告
        adaptation_file = self.output_dir / "adaptation_report.json"
        with open(adaptation_file, 'w', encoding='utf-8') as f:
            json.dump(adapted_versions, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ 多平台适配完成!")
        print(f"   适配平台: {', '.join(platforms)}")
        print(f"   生成文件: {len(adapted_versions)}个")
        print(f"   适配报告: {adaptation_file}")
        
        return adapted_versions
    
    def step6_data_analytics(self):
        """步骤6: 数据分析"""
        self.print_step(6, "数据分析")
        
        print("正在分析内容表现数据...")
        time.sleep(1)
        
        # 模拟数据分析
        analytics_data = {
            "analysis_period": "7_days",
            "overall_metrics": {
                "total_views": 12500,
                "average_read_time": "3分15秒",
                "completion_rate": 68.5,
                "engagement_rate": 15.2,
                "share_rate": 8.7
            },
            "platform_performance": {
                "微信公众号": {
                    "views": 6800,
                    "engagement": 16.8,
                    "conversion": 4.2
                },
                "知乎": {
                    "views": 4200,
                    "engagement": 21.5,
                    "upvotes": 850
                },
                "小红书": {
                    "views": 950,
                    "engagement": 8.4,
                    "saves": 320
                },
                "Twitter": {
                    "views": 550,
                    "engagement": 6.2,
                    "retweets": 45
                }
            },
            "audience_insights": {
                "primary_audience": "技术开发者",
                "technical_level": "中级",
                "interests": ["编程", "技术学习", "效率工具"],
                "active_time": "工作日 20:00-22:00"
            },
            "content_analysis": {
                "popular_sections": ["实战技巧", "代码示例"],
                "drop_off_points": ["理论原理"],
                "reading_depth": 72.3
            },
            "recommendations": [
                {
                    "priority": "high",
                    "action": "增加更多实操案例",
                    "reason": "实操内容阅读完成率更高",
                    "expected_impact": "+5-8%阅读完成率"
                },
                {
                    "priority": "medium",
                    "action": "优化标题吸引力",
                    "reason": "当前标题点击率一般",
                    "expected_impact": "+10-15%点击率"
                },
                {
                    "priority": "low",
                    "action": "增加视觉元素",
                    "reason": "提升内容可读性",
                    "expected_impact": "+3-5%分享率"
                }
            ]
        }
        
        # 保存分析报告
        analytics_file = self.output_dir / "analytics_report.json"
        with open(analytics_file, 'w', encoding='utf-8') as f:
            json.dump(analytics_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ 数据分析完成!")
        print(f"   总阅读量: {analytics_data['overall_metrics']['total_views']}次")
        print(f"   平均阅读完成率: {analytics_data['overall_metrics']['completion_rate']}%")
        print(f"   最高互动平台: 知乎 ({analytics_data['platform_performance']['知乎']['engagement']}%)")
        print(f"   分析报告: {analytics_file}")
        print(f"   优化建议: {len(analytics_data['recommendations'])}项")
        
        return analytics_data
    
    def run_demo(self):
        """运行完整演示"""
        self.print_header("article-workflow 交互式演示")
        
        print("欢迎使用 article-workflow 演示!")
        print("本演示将带你体验完整的内容创作工作流程。")
        
        input("\n按 Enter 键开始...")
        
        try:
            # 步骤1: 内容规划
            planning_result = self.step1_content_planning()
            
            # 步骤2: 文章生成
            article_content = self.step2_article_generation(planning_result)
            
            # 步骤3: 内容审查
            review_report = self.step3_content_review(article_content)
            
            if review_report['status'] != 'approved':
                print("\n⚠️ 文章未通过审查，演示结束。")
                return
            
            # 步骤4: SEO优化
            seo_result = self.step4_seo_optimization(article_content)
            
            # 步骤5: 多平台适配
            platforms = planning_result.get("platforms", ["微信公众号", "知乎"])
            adapted_versions = self.step5_multi_platform_adaptation(article_content, platforms)
            
            # 步骤6: 数据分析
            analytics_data = self.step6_data_analytics()
            
            # 总结
            self.print_header("演示完成!")
            
            print("🎉 恭喜你完成了完整的 article-workflow 体验!")
            print("\n📊 成果总结:")
            print(f"   1. 📝 生成1篇技术文章 ({len(article_content)}字符)")
            print(f"   2. 🔍 内容审查评分: {review_report['total_score']}/100")
            print(f"   3. 🔎 SEO优化分数: {seo_result['optimization_score']}/100")
            print(f"   4. 🌍 适配{len(adapted_versions)}个内容平台")
            print(f"   5. 📈 模拟数据分析报告完成")
            print(f"   6. 💡 获得{len(analytics_data['recommendations'])}项优化建议")
            
            print(f"\n📁 生成的文件保存在: {self.output_dir}/")
            print("   包含: 文章、审查报告、SEO报告、平台适配版本、分析报告")
            
            print("\n🚀 真实使用步骤:")
            print("   1. 配置API密钥: python scripts/config_wizard.py")
            print("   2. 运行完整流水线: python scripts/pipeline_cli.py run full-pipeline")
            print("   3. 查看使用指南: cat USAGE_GUIDE.md")
            
            print("\n💡 提示: 在实际项目中，所有步骤都是自动化的!")
            print("   你只需要提供主题和要求，article-workflow会处理剩下的一切。")
            
        except KeyboardInterrupt:
            print("\n\n演示被用户中断。")
        except Exception as e:
            print(f"\n❌ 演示过程中出现错误: {e}")
            import traceback
            traceback.print_exc()


def main():
    """主函数"""
    demo = InteractiveDemo()
    demo.run_demo()


if __name__ == "__main__":
    main()