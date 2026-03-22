#!/usr/bin/env python3
"""
运行所有场景测试并生成综合报告
"""

import os
import sys
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "shared"))

class ScenarioTestRunner:
    """场景测试运行器"""
    
    def __init__(self):
        self.output_dir = Path(PROJECT_ROOT) / "test_results"
        self.output_dir.mkdir(exist_ok=True)
        self.start_time = datetime.now()
        
    def run_test(self, test_file: str, test_name: str) -> dict:
        """运行单个测试"""
        print(f"🧪 运行 {test_name}...")
        
        try:
            # 使用 subprocess 运行测试
            result = subprocess.run(
                [sys.executable, test_file],
                capture_output=True,
                text=True,
                encoding='utf-8'
            )
            
            test_result = {
                "test_name": test_name,
                "status": "passed" if result.returncode == 0 else "failed",
                "execution_time": 0,
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode,
                "success": result.returncode == 0
            }
            
            return test_result
            
        except Exception as e:
            return {
                "test_name": test_name,
                "status": "error",
                "execution_time": 0,
                "output": "",
                "error": str(e),
                "return_code": 1,
                "success": False
            }
    
    def run_all_scenarios(self) -> dict:
        """运行所有场景测试"""
        print("🚀 开始运行所有场景测试")
        print("=" * 60)
        
        scenario_tests = {
            "技术教程": "test_scenario_technical_tutorial.py",
            "行业分析": "test_scenario_industry_analysis.py",
            "营销文案": "test_scenario_marketing_copy.py",
            "多平台分发": "test_scenario_platform_distribution.py",
            "数据驱动优化": "test_scenario_data_driven_optimization.py",
            "批量处理": "test_scenario_batch_processing.py"
        }
        
        all_results = {}
        total_passed = 0
        total_tests = len(scenario_tests)
        
        for scenario_name, test_file in scenario_tests.items():
            test_path = Path(PROJECT_ROOT) / test_file
            
            if test_path.exists():
                start_time = time.time()
                result = self.run_test(str(test_path), scenario_name)
                end_time = time.time()
                result["execution_time"] = round(end_time - start_time, 2)
                
                all_results[scenario_name] = result
                
                if result["success"]:
                    total_passed += 1
                    print(f"  ✅ {scenario_name} 测试通过")
                else:
                    print(f"  ❌ {scenario_name} 测试失败")
            else:
                print(f"  ⚠️  {test_file} 不存在")
        
        # 计算总体统计
        passed_rate = (total_passed / total_tests) * 100
        
        overall_result = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": total_tests,
            "total_passed": total_passed,
            "passed_rate": f"{passed_rate:.1f}%",
            "execution_summary": {
                "total_time": round(time.time() - self.start_time.timestamp(), 2),
                "average_time_per_test": round(sum(r["execution_time"] for r in all_results.values()) / total_tests, 2),
                "success_rate": passed_rate
            },
            "scenario_results": all_results,
            "summary": {
                "overall_status": "PASSED" if total_passed == total_tests else "FAILED",
                "recommendations": self.generate_recommendations(all_results)
            }
        }
        
        return overall_result
    
    def generate_recommendations(self, results: dict) -> list:
        """生成改进建议"""
        recommendations = []
        
        for scenario_name, result in results.items():
            if not result["success"]:
                recommendations.append({
                    "scenario": scenario_name,
                    "issue": "测试失败",
                    "suggestion": f"检查 {scenario_name} 测试脚本和依赖"
                })
        
        if len(recommendations) == 0:
            recommendations.append({
                "scenario": "所有场景",
                "issue": "无",
                "suggestion": "所有场景测试通过，继续保持"
            })
        
        return recommendations
    
    def generate_comprehensive_report(self) -> dict:
        """生成综合报告"""
        print("\n📊 生成综合测试报告...")
        
        results = self.run_all_scenarios()
        
        # 计算总体评分
        total_passed = sum(1 for r in results["scenario_results"].values() if r["success"])
        total_tests = len(results["scenario_results"])
        
        # 评估每个场景的强度
        scenario_strengths = {}
        for scenario_name, result in results["scenario_results"].items():
            strength = 0
            if result["success"]:
                strength += 5  # 基础分
                if result["execution_time"] < 5:  # 快速执行
                    strength += 2
                if "error" not in result or not result["error"]:  # 无错误
                    strength += 1
                if result["output"] and len(result["output"]) > 100:  # 有详细输出
                    strength += 2
            scenario_strengths[scenario_name] = strength
        
        # 生成综合报告
        comprehensive_report = {
            "test_summary": results,
            "scenario_analysis": {
                "total_scenarios": total_tests,
                "passed_scenarios": total_passed,
                "pass_rate": f"{(total_passed / total_tests * 100):.1f}%",
                "scenario_strengths": scenario_strengths,
                "strongest_scenario": max(scenario_strengths, key=scenario_strengths.get) if scenario_strengths else None,
                "weakest_scenario": min(scenario_strengths, key=scenario_strengths.get) if scenario_strengths else None
            },
            "performance_metrics": {
                "total_execution_time": results["execution_summary"]["total_time"],
                "average_execution_time": results["execution_summary"]["average_time_per_test"],
                "fastest_scenario": min(results["scenario_results"].items(), key=lambda x: x[1]["execution_time"])[0] if results["scenario_results"] else None,
                "slowest_scenario": max(results["scenario_results"].items(), key=lambda x: x[1]["execution_time"])[0] if results["scenario_results"] else None
            },
            "recommendations": results["summary"]["recommendations"],
            "overall_assessment": {
                "status": results["summary"]["overall_status"],
                "confidence_level": "高" if total_passed == total_tests else "中" if total_passed >= total_tests * 0.7 else "低",
                "readiness_for_production": total_passed == total_tests
            }
        }
        
        return comprehensive_report
    
    def save_report(self, report: dict):
        """保存报告到文件"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.output_dir / f"test_report_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n📄 测试报告已保存到: {report_file}")
        
        # 同时生成 Markdown 格式的摘要
        summary_file = self.output_dir / f"test_summary_{timestamp}.md"
        self.generate_markdown_summary(report, summary_file)
        
        return str(report_file), str(summary_file)
    
    def generate_markdown_summary(self, report: dict, output_path: Path):
        """生成 Markdown 格式的摘要"""
        summary = f"""# 🧪 多场景测试报告

## 📊 测试概览

- **测试时间**: {report['test_summary']['timestamp']}
- **测试场景数**: {report['scenario_analysis']['total_scenarios']}
- **通过场景数**: {report['scenario_analysis']['passed_scenarios']}
- **通过率**: {report['scenario_analysis']['pass_rate']}
- **总体状态**: {report['overall_assessment']['status']}

## 📈 性能指标

- **总执行时间**: {report['performance_metrics']['total_execution_time']} 秒
- **平均执行时间**: {report['performance_metrics']['average_execution_time']} 秒
- **最快场景**: {report['performance_metrics']['fastest_scenario']}
- **最慢场景**: {report['performance_metrics']['slowest_scenario']}

## 🏆 场景分析

| 场景 | 状态 | 强度评分 | 执行时间(s) |
|------|------|----------|-------------|
"""

        for scenario_name, result in report['test_summary']['scenario_results'].items():
            status_emoji = "✅" if result["success"] else "❌"
            strength = report['scenario_analysis']['scenario_strengths'].get(scenario_name, 0)
            exec_time = result.get("execution_time", 0)
            summary += f"| {scenario_name} | {status_emoji} | {strength}/10 | {exec_time} |\n"

        summary += f"""
## 💪 最强场景
**{report['scenario_analysis']['strongest_scenario']}**

## 🔧 最弱场景  
**{report['scenario_analysis']['weakest_scenario']}**

## 📋 建议

"""

        for rec in report['recommendations']:
            summary += f"- **{rec['scenario']}**: {rec['suggestion']}\n"

        summary += f"""
## 🚀 生产就绪评估

- **置信水平**: {report['overall_assessment']['confidence_level']}
- **生产就绪**: {'✅ 是' if report['overall_assessment']['readiness_for_production'] else '❌ 否'}

---

*报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary)

def main():
    """主函数"""
    print("=" * 60)
    print("🔬 ARTICLE-WORKFLOW 多场景测试系统")
    print("=" * 60)
    
    # 创建测试运行器
    runner = ScenarioTestRunner()
    
    try:
        # 生成综合报告
        report = runner.generate_comprehensive_report()
        
        # 保存报告
        json_file, md_file = runner.save_report(report)
        
        print("\n" + "=" * 60)
        print("🎉 多场景测试完成!")
        print("=" * 60)
        
        # 显示关键结果
        overall_status = report['overall_assessment']['status']
        pass_rate = report['scenario_analysis']['pass_rate']
        confidence = report['overall_assessment']['confidence_level']
        
        print(f"📊 总体状态: {overall_status}")
        print(f"📈 通过率: {pass_rate}")
        print(f"💪 置信水平: {confidence}")
        print(f"🏭 生产就绪: {'✅ 是' if report['overall_assessment']['readiness_for_production'] else '❌ 否'}")
        print(f"📄 详细报告: {json_file}")
        print(f"📝 摘要报告: {md_file}")
        
        # 返回退出码
        if overall_status == "PASSED":
            return 0
        else:
            return 1
            
    except Exception as e:
        print(f"❌ 测试运行失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)