#!/usr/bin/env python3
"""
A/B Testing System for Content Optimization

功能：实现标题、摘要、封面图等元素的A/B测试
支持：多变量测试、统计分析、自动优化、结果可视化
"""

import os
import sys
import json
import yaml
import random
import statistics
import math
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# 添加共享模块路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared"))

from shared import ConfigLoader, PipelineManager


class TestType(Enum):
    """测试类型枚举"""
    TITLE = "title"
    SUMMARY = "summary"
    COVER = "cover"
    CTA = "cta"  # 号召性用语
    LAYOUT = "layout"
    TIMING = "timing"


class Variation:
    """测试变体类"""
    
    def __init__(self, name: str, content: str, metadata: Dict[str, Any] = None):
        self.name = name
        self.content = content
        self.metadata = metadata or {}
        self.stats = {
            "impressions": 0,
            "clicks": 0,
            "conversions": 0,
            "engagement": 0,
            "start_time": datetime.now(),
            "last_update": datetime.now()
        }
        self.results = []
    
    def add_result(self, success: bool, metric_value: float = None):
        """添加测试结果"""
        result = {
            "timestamp": datetime.now(),
            "success": success,
            "metric_value": metric_value
        }
        self.results.append(result)
        self.stats["last_update"] = datetime.now()
        
        if success:
            self.stats["conversions"] += 1
        self.stats["impressions"] += 1
    
    def update_stats(self, impressions: int = 0, clicks: int = 0, 
                     conversions: int = 0, engagement: float = 0):
        """批量更新统计"""
        self.stats["impressions"] += impressions
        self.stats["clicks"] += clicks
        self.stats["conversions"] += conversions
        self.stats["engagement"] += engagement
        self.stats["last_update"] = datetime.now()
    
    def get_conversion_rate(self) -> float:
        """获取转化率"""
        if self.stats["impressions"] == 0:
            return 0.0
        return self.stats["conversions"] / self.stats["impressions"] * 100
    
    def get_confidence_interval(self) -> Tuple[float, float]:
        """获取置信区间"""
        if len(self.results) < 2:
            return (0.0, 0.0)
        
        successes = [r["metric_value"] for r in self.results if r["metric_value"] is not None]
        if not successes:
            return (0.0, 0.0)
        
        mean = statistics.mean(successes)
        stdev = statistics.stdev(successes) if len(successes) > 1 else 0
        
        # 95% 置信区间
        z_score = 1.96
        margin = z_score * stdev / math.sqrt(len(successes))
        
        return (mean - margin, mean + margin)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "name": self.name,
            "content": self.content,
            "metadata": self.metadata,
            "stats": self.stats,
            "conversion_rate": self.get_conversion_rate(),
            "confidence_interval": self.get_confidence_interval(),
            "total_results": len(self.results)
        }


class ABTest:
    """A/B测试类"""
    
    def __init__(self, test_id: str, test_type: TestType, 
                 baseline: Variation, variations: List[Variation]):
        self.test_id = test_id
        self.test_type = test_type
        self.baseline = baseline
        self.variations = variations
        self.start_time = datetime.now()
        self.end_time = None
        self.status = "running"  # running, completed, paused
        self.target_sample_size = 1000  # 目标样本量
        self.min_duration_days = 7  # 最小测试天数
        self.traffic_allocation = {
            baseline.name: 0.5,  # 基线分配50%流量
        }
        # 其他变体平均分配剩余流量
        remaining_traffic = 0.5 / len(variations)
        for variation in variations:
            self.traffic_allocation[variation.name] = remaining_traffic
    
    def add_variation_result(self, variation_name: str, success: bool, 
                            metric_value: float = None):
        """为特定变体添加结果"""
        if variation_name == self.baseline.name:
            self.baseline.add_result(success, metric_value)
        else:
            for variation in self.variations:
                if variation.name == variation_name:
                    variation.add_result(success, metric_value)
                    break
    
    def update_variation_stats(self, variation_name: str, **stats):
        """更新变体统计"""
        if variation_name == self.baseline.name:
            self.baseline.update_stats(**stats)
        else:
            for variation in self.variations:
                if variation.name == variation_name:
                    variation.update_stats(**stats)
                    break
    
    def get_winner(self) -> Optional[Variation]:
        """获取获胜变体"""
        if self.status != "completed":
            return None
        
        all_variations = [self.baseline] + self.variations
        winner = max(all_variations, key=lambda v: v.get_conversion_rate())
        
        # 检查是否显著优于基线
        baseline_rate = self.baseline.get_conversion_rate()
        winner_rate = winner.get_conversion_rate()
        
        if winner_rate > baseline_rate and self.is_statistically_significant(winner, self.baseline):
            return winner
        return self.baseline  # 如果没有显著差异，保持基线
    
    def is_statistically_significant(self, variation_a: Variation, 
                                     variation_b: Variation, 
                                     confidence_level: float = 0.95) -> bool:
        """检查两个变体之间是否有统计显著性差异"""
        # 使用Z检验
        rate_a = variation_a.get_conversion_rate() / 100
        rate_b = variation_b.get_conversion_rate() / 100
        
        n_a = variation_a.stats["impressions"]
        n_b = variation_b.stats["impressions"]
        
        if n_a == 0 or n_b == 0:
            return False
        
        # 计算Z值
        p_pool = (rate_a * n_a + rate_b * n_b) / (n_a + n_b)
        se = math.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))
        
        if se == 0:
            return False
        
        z_score = abs(rate_a - rate_b) / se
        
        # 临界Z值
        critical_z = 1.96 if confidence_level == 0.95 else 2.58
        
        return z_score > critical_z
    
    def check_stopping_conditions(self) -> bool:
        """检查是否满足停止条件"""
        # 检查是否达到最小样本量
        total_impressions = sum(v.stats["impressions"] for v in [self.baseline] + self.variations)
        if total_impressions >= self.target_sample_size:
            return True
        
        # 检查是否达到最小测试天数
        days_running = (datetime.now() - self.start_time).days
        if days_running >= self.min_duration_days:
            return True
        
        # 检查是否有变体显著优于基线
        for variation in self.variations:
            if self.is_statistically_significant(variation, self.baseline):
                return True
        
        return False
    
    def complete_test(self):
        """完成测试"""
        self.status = "completed"
        self.end_time = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "test_id": self.test_id,
            "test_type": self.test_type.value,
            "baseline": self.baseline.to_dict(),
            "variations": [v.to_dict() for v in self.variations],
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "status": self.status,
            "traffic_allocation": self.traffic_allocation,
            "winner": self.get_winner().name if self.get_winner() else None
        }


class ABTestManager:
    """A/B测试管理器"""
    
    def __init__(self, config_loader: ConfigLoader):
        self.config_loader = config_loader
        self.tests = {}  # test_id -> ABTest
        self.output_dir = Path("output/ab_tests")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def load_config(self):
        """加载配置"""
        config = self.config_loader.load_config()
        ab_test_config = config.get("ab_testing", {})
        
        # 设置输出目录
        custom_output_dir = ab_test_config.get("output_dir")
        if custom_output_dir:
            self.output_dir = Path(custom_output_dir)
            self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 配置测试参数
        self.default_params = {
            "target_sample_size": ab_test_config.get("target_sample_size", 1000),
            "min_duration_days": ab_test_config.get("min_duration_days", 7),
            "confidence_level": ab_test_config.get("confidence_level", 0.95),
            "traffic_allocation": ab_test_config.get("traffic_allocation", "equal")
        }
    
    def create_title_test(self, original_title: str, 
                          variations: List[str], 
                          test_id: str = None) -> str:
        """创建标题A/B测试"""
        if test_id is None:
            test_id = f"title_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # 创建基线变体
        baseline = Variation("baseline", original_title, {"type": "title"})
        
        # 创建变体
        variation_objs = []
        for i, variation_title in enumerate(variations, 1):
            variation = Variation(f"variation_{i}", variation_title, {"type": "title"})
            variation_objs.append(variation)
        
        # 创建测试
        test = ABTest(test_id, TestType.TITLE, baseline, variation_objs)
        test.target_sample_size = self.default_params["target_sample_size"]
        test.min_duration_days = self.default_params["min_duration_days"]
        
        self.tests[test_id] = test
        
        # 保存测试配置
        self.save_test_config(test)
        
        return test_id
    
    def create_summary_test(self, original_summary: str,
                           variations: List[str],
                           test_id: str = None) -> str:
        """创建摘要A/B测试"""
        if test_id is None:
            test_id = f"summary_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        baseline = Variation("baseline", original_summary, {"type": "summary"})
        
        variation_objs = []
        for i, variation_summary in enumerate(variations, 1):
            variation = Variation(f"variation_{i}", variation_summary, {"type": "summary"})
            variation_objs.append(variation)
        
        test = ABTest(test_id, TestType.SUMMARY, baseline, variation_objs)
        test.target_sample_size = self.default_params["target_sample_size"]
        test.min_duration_days = self.default_params["min_duration_days"]
        
        self.tests[test_id] = test
        self.save_test_config(test)
        
        return test_id
    
    def create_cover_test(self, cover_options: List[Dict[str, Any]], 
                         test_id: str = None) -> str:
        """创建封面图A/B测试"""
        if test_id is None:
            test_id = f"cover_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if not cover_options:
            raise ValueError("至少需要一个封面选项")
        
        # 第一个作为基线
        baseline_data = cover_options[0]
        baseline = Variation("baseline", baseline_data.get("url", ""), baseline_data)
        
        # 其他作为变体
        variation_objs = []
        for i, cover_data in enumerate(cover_options[1:], 1):
            variation = Variation(f"variation_{i}", cover_data.get("url", ""), cover_data)
            variation_objs.append(variation)
        
        test = ABTest(test_id, TestType.COVER, baseline, variation_objs)
        test.target_sample_size = self.default_params["target_sample_size"]
        test.min_duration_days = self.default_params["min_duration_days"]
        
        self.tests[test_id] = test
        self.save_test_config(test)
        
        return test_id
    
    def get_next_variation(self, test_id: str) -> Variation:
        """根据流量分配获取下一个测试变体"""
        if test_id not in self.tests:
            raise ValueError(f"测试 {test_id} 不存在")
        
        test = self.tests[test_id]
        
        # 根据流量分配随机选择变体
        variations = [test.baseline] + test.variations
        weights = [test.traffic_allocation.get(v.name, 0) for v in variations]
        
        # 归一化权重
        total_weight = sum(weights)
        if total_weight == 0:
            # 如果权重为零，平均分配
            weights = [1/len(variations)] * len(variations)
        else:
            weights = [w/total_weight for w in weights]
        
        return random.choices(variations, weights=weights, k=1)[0]
    
    def add_test_result(self, test_id: str, variation_name: str, 
                       success: bool, metric_value: float = None):
        """添加测试结果"""
        if test_id not in self.tests:
            raise ValueError(f"测试 {test_id} 不存在")
        
        test = self.tests[test_id]
        test.add_variation_result(variation_name, success, metric_value)
        
        # 检查是否满足停止条件
        if test.check_stopping_conditions() and test.status == "running":
            test.complete_test()
            self.generate_test_report(test)
        
        # 保存更新
        self.save_test_config(test)
    
    def update_test_stats(self, test_id: str, variation_name: str, **stats):
        """批量更新测试统计"""
        if test_id not in self.tests:
            raise ValueError(f"测试 {test_id} 不存在")
        
        test = self.tests[test_id]
        test.update_variation_stats(variation_name, **stats)
        
        # 检查是否满足停止条件
        if test.check_stopping_conditions() and test.status == "running":
            test.complete_test()
            self.generate_test_report(test)
        
        # 保存更新
        self.save_test_config(test)
    
    def get_test_results(self, test_id: str) -> Dict[str, Any]:
        """获取测试结果"""
        if test_id not in self.tests:
            raise ValueError(f"测试 {test_id} 不存在")
        
        test = self.tests[test_id]
        return test.to_dict()
    
    def list_tests(self, status: str = None) -> List[Dict[str, Any]]:
        """列出所有测试"""
        tests_list = []
        
        for test_id, test in self.tests.items():
            if status and test.status != status:
                continue
            
            test_info = {
                "test_id": test_id,
                "test_type": test.test_type.value,
                "status": test.status,
                "start_time": test.start_time.isoformat(),
                "variations": len(test.variations) + 1,
                "total_impressions": sum(v.stats["impressions"] for v in [test.baseline] + test.variations),
                "winner": test.get_winner().name if test.get_winner() else None
            }
            tests_list.append(test_info)
        
        return tests_list
    
    def save_test_config(self, test: ABTest):
        """保存测试配置"""
        test_dir = self.output_dir / test.test_id
        test_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存测试配置
        config_file = test_dir / "test_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(test.to_dict(), f, ensure_ascii=False, indent=2)
        
        # 保存原始变体数据
        variations_file = test_dir / "variations.json"
        variations_data = {
            "baseline": {
                "name": test.baseline.name,
                "content": test.baseline.content,
                "metadata": test.baseline.metadata
            },
            "variations": [
                {
                    "name": v.name,
                    "content": v.content,
                    "metadata": v.metadata
                } for v in test.variations
            ]
        }
        with open(variations_file, 'w', encoding='utf-8') as f:
            json.dump(variations_data, f, ensure_ascii=False, indent=2)
    
    def generate_test_report(self, test: ABTest):
        """生成测试报告"""
        test_dir = self.output_dir / test.test_id
        
        # 生成详细报告
        report = self.generate_detailed_report(test)
        
        # 保存报告
        report_file = test_dir / "test_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        # 生成可视化图表
        self.generate_visualization(test, test_dir)
        
        print(f"✅ 测试报告已生成: {report_file}")
    
    def generate_detailed_report(self, test: ABTest) -> str:
        """生成详细测试报告"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# A/B测试报告

**测试ID**: {test.test_id}  
**测试类型**: {test.test_type.value}  
**状态**: {test.status}  
**开始时间**: {test.start_time.strftime('%Y-%m-%d %H:%M:%S')}  
**结束时间**: {test.end_time.strftime('%Y-%m-%d %H:%M:%S') if test.end_time else '进行中'}  
**报告生成时间**: {now}

## 📊 测试概览

| 指标 | 数值 |
|------|------|
| 变体数量 | {len(test.variations) + 1} 个 |
| 总曝光量 | {sum(v.stats['impressions'] for v in [test.baseline] + test.variations):,} 次 |
| 测试时长 | {(test.end_time - test.start_time).days if test.end_time else 0} 天 |
| 流量分配 | 基线 {test.traffic_allocation.get('baseline', 0)*100:.1f}% |

## 🎯 测试结果

"""
        
        # 所有变体的表现
        all_variations = [test.baseline] + test.variations
        
        report += "### 各变体表现对比\n\n"
        report += "| 变体 | 曝光量 | 转化量 | 转化率 | 置信区间 |\n"
        report += "|------|--------|--------|--------|----------|\n"
        
        for variation in all_variations:
            impressions = variation.stats["impressions"]
            conversions = variation.stats["conversions"]
            rate = variation.get_conversion_rate()
            ci_low, ci_high = variation.get_confidence_interval()
            
            report += f"| {variation.name} | {impressions:,} | {conversions:,} | {rate:.2f}% | ({ci_low:.2f}%, {ci_high:.2f}%) |\n"
        
        report += "\n"
        
        # 获胜者分析
        winner = test.get_winner()
        baseline = test.baseline
        
        if winner and winner.name != baseline.name:
            baseline_rate = baseline.get_conversion_rate()
            winner_rate = winner.get_conversion_rate()
            improvement = ((winner_rate - baseline_rate) / baseline_rate * 100) if baseline_rate > 0 else 0
            
            report += f"## 🏆 获胜变体: {winner.name}\n\n"
            report += f"**内容**: {winner.content[:100]}...\n\n"
            report += f"**表现提升**: {improvement:.1f}% (从 {baseline_rate:.2f}% 提升到 {winner_rate:.2f}%)\n\n"
            
            # 统计显著性
            if test.is_statistically_significant(winner, baseline):
                report += "✅ **统计显著性**: 获胜变体显著优于基线 (p < 0.05)\n\n"
            else:
                report += "⚠️ **统计显著性**: 虽然转化率更高，但差异不显著\n\n"
            
            report += "### 建议\n"
            report += f"1. 将 {winner.name} 设置为新的基线\n"
            report += "2. 分析获胜原因，应用到未来内容\n"
            report += "3. 考虑进行更多优化测试\n"
        
        else:
            report += "## 🔄 无明确获胜者\n\n"
            report += "所有变体表现相近，没有显著差异。\n\n"
            report += "### 建议\n"
            report += "1. 保持当前基线不变\n"
            report += "2. 尝试新的变体或测试不同元素\n"
            report += "3. 增加样本量或延长测试时间\n"
        
        # 详细分析
        report += "\n## 🔍 详细分析\n\n"
        
        # 时间趋势（如果有足够数据点）
        if test.baseline.results:
            report += "### 时间趋势\n"
            report += "- 转化率随时间的变化情况\n"
            report += "- 识别表现波动或稳定期\n"
        
        # 变体对比
        report += "\n### 变体对比分析\n"
        for i, variation in enumerate(test.variations, 1):
            variation_rate = variation.get_conversion_rate()
            baseline_rate = baseline.get_conversion_rate()
            diff = variation_rate - baseline_rate
            
            significance = test.is_statistically_significant(variation, baseline)
            sig_symbol = "✅" if significance and diff > 0 else "⚠️"
            
            report += f"\n**{variation.name}**:\n"
            report += f"- 内容: {variation.content[:80]}...\n"
            report += f"- 对比基线: {diff:+.2f}% ({sig_symbol})\n"
            report += f"- 置信区间: ({variation.get_confidence_interval()[0]:.2f}%, {variation.get_confidence_interval()[1]:.2f}%)\n"
        
        report += "\n---\n"
        report += "*报告由 article-workflow A/B Testing System 生成*\n"
        
        return report
    
    def generate_visualization(self, test: ABTest, output_dir: Path):
        """生成可视化图表"""
        try:
            all_variations = [test.baseline] + test.variations
            
            # 创建图表
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle(f'A/B Test Results: {test.test_id}', fontsize=16)
            
            # 1. 转化率对比
            names = [v.name for v in all_variations]
            rates = [v.get_conversion_rate() for v in all_variations]
            
            axes[0, 0].bar(names, rates, color=['blue'] + ['green'] * len(test.variations))
            axes[0, 0].set_title('Conversion Rate Comparison')
            axes[0, 0].set_ylabel('Conversion Rate (%)')
            axes[0, 0].tick_params(axis='x', rotation=45)
            
            # 添加数值标签
            for i, rate in enumerate(rates):
                axes[0, 0].text(i, rate + 0.1, f'{rate:.2f}%', 
                              ha='center', va='bottom')
            
            # 2. 曝光量分布
            impressions = [v.stats["impressions"] for v in all_variations]
            
            axes[0, 1].pie(impressions, labels=names, autopct='%1.1f%%')
            axes[0, 1].set_title('Traffic Allocation')
            
            # 3. 置信区间
            ci_lows = [v.get_confidence_interval()[0] for v in all_variations]
            ci_highs = [v.get_confidence_interval()[1] for v in all_variations]
            
            # 误差棒
            y_pos = range(len(names))
            axes[1, 0].errorbar(y_pos, rates, yerr=[rates[i] - ci_lows[i] for i in range(len(rates))], 
                               fmt='o', capsize=5)
            axes[1, 0].set_title('Conversion Rate with Confidence Intervals')
            axes[1, 0].set_xticks(y_pos)
            axes[1, 0].set_xticklabels(names)
            axes[1, 0].set_ylabel('Conversion Rate (%)')
            
            # 4. 提升百分比
            baseline_rate = test.baseline.get_conversion_rate()
            improvements = [(v.get_conversion_rate() - baseline_rate) / baseline_rate * 100 
                          if baseline_rate > 0 else 0 for v in all_variations]
            
            colors = ['gray' if imp <= 0 else 'green' for imp in improvements]
            axes[1, 1].bar(names, improvements, color=colors)
            axes[1, 1].set_title('Improvement vs Baseline (%)')
            axes[1, 1].axhline(y=0, color='r', linestyle='-', alpha=0.3)
            axes[1, 1].tick_params(axis='x', rotation=45)
            
            # 调整布局
            plt.tight_layout()
            
            # 保存图表
            chart_file = output_dir / "test_results_chart.png"
            plt.savefig(chart_file, dpi=300, bbox_inches='tight')
            plt.close(fig)
            
            print(f"📊 图表已生成: {chart_file}")
            
        except Exception as e:
            print(f"⚠️  图表生成失败: {e}")


def main():
    """主函数"""
    print("🎯 A/B Testing System - 内容优化测试系统")
    print("=" * 50)
    
    # 加载配置
    config_loader = ConfigLoader()
    
    try:
        config_loader.load_config()
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        print("请先运行配置向导: python scripts/config_wizard.py")
        sys.exit(1)
    
    # 创建测试管理器
    test_manager = ABTestManager(config_loader)
    test_manager.load_config()
    
    # 解析命令行参数
    import argparse
    parser = argparse.ArgumentParser(description="A/B Testing System")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # 创建测试
    create_parser = subparsers.add_parser("create", help="创建新测试")
    create_parser.add_argument("type", choices=["title", "summary", "cover"], help="测试类型")
    create_parser.add_argument("--baseline", required=True, help="基线内容")
    create_parser.add_argument("--variations", nargs="+", required=True, help="变体内容列表")
    create_parser.add_argument("--test-id", help="自定义测试ID")
    
    # 添加结果
    result_parser = subparsers.add_parser("result", help="添加测试结果")
    result_parser.add_argument("test_id", help="测试ID")
    result_parser.add_argument("variation", help="变体名称")
    result_parser.add_argument("--success", action="store_true", help="是否成功")
    result_parser.add_argument("--metric", type=float, help="指标数值")
    
    # 获取变体
    next_parser = subparsers.add_parser("next", help="获取下一个测试变体")
    next_parser.add_argument("test_id", help="测试ID")
    
    # 获取结果
    get_parser = subparsers.add_parser("get", help="获取测试结果")
    get_parser.add_argument("test_id", help="测试ID")
    
    # 列出测试
    list_parser = subparsers.add_parser("list", help="列出所有测试")
    list_parser.add_argument("--status", choices=["running", "completed", "paused"], help="按状态过滤")
    
    args = parser.parse_args()
    
    if args.command == "create":
        if args.type == "title":
            test_id = test_manager.create_title_test(
                args.baseline, args.variations, args.test_id
            )
            print(f"✅ 标题A/B测试已创建: {test_id}")
            
        elif args.type == "summary":
            test_id = test_manager.create_summary_test(
                args.baseline, args.variations, args.test_id
            )
            print(f"✅ 摘要A/B测试已创建: {test_id}")
            
        elif args.type == "cover":
            # 封面测试需要更复杂的数据结构
            print("❌ 封面测试需要JSON格式的封面数据")
            print("请使用 --variations 参数传入JSON字符串")
    
    elif args.command == "result":
        test_manager.add_test_result(
            args.test_id, args.variation, args.success, args.metric
        )
        print(f"✅ 结果已添加: 测试 {args.test_id}, 变体 {args.variation}")
        
        # 显示当前状态
        test_info = test_manager.get_test_results(args.test_id)
        print(f"📊 当前状态: {test_info['status']}")
        
        if test_info['status'] == "completed":
            print(f"🏆 获胜者: {test_info['winner']}")
    
    elif args.command == "next":
        variation = test_manager.get_next_variation(args.test_id)
        print(f"🎯 下一个测试变体: {variation.name}")
        print(f"📝 内容: {variation.content}")
    
    elif args.command == "get":
        results = test_manager.get_test_results(args.test_id)
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.command == "list":
        tests = test_manager.list_tests(args.status)
        print(f"📋 测试列表 ({len(tests)} 个):")
        
        for test in tests:
            status_icon = "🟢" if test['status'] == 'running' else "🟡" if test['status'] == 'paused' else "🔴"
            print(f"{status_icon} {test['test_id']} ({test['test_type']})")
            print(f"  状态: {test['status']}, 开始时间: {test['start_time']}")
            print(f"  变体: {test['variations']} 个, 曝光: {test['total_impressions']:,} 次")
            if test['winner']:
                print(f"  获胜者: {test['winner']}")
            print()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()