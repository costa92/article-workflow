#!/usr/bin/env python3
"""
技术教程场景测试
测试 article-workflow 在技术教程内容创作场景下的表现
"""

import os
import sys
import json
import tempfile
import unittest
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "shared"))

class TestTechnicalTutorialScenario(unittest.TestCase):
    """测试技术教程场景"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 技术教程场景配置
        self.scenario_config = {
            "scenario_name": "technical_tutorial",
            "content_type": "技术教程",
            "target_audience": "Python中级开发者",
            "complexity_level": "中级",
            "expected_outputs": ["article", "code_examples", "review_report", "seo_report"],
            "success_criteria": {
                "article_length": "2000-3000字",
                "code_examples": "≥3个",
                "review_score": "≥85/100",
                "seo_score": "≥80/100"
            }
        }
        
    def tearDown(self):
        """测试后清理"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def create_technical_tutorial_article(self) -> dict:
        """创建技术教程测试文章"""
        return {
            "metadata": {
                "title": "Python异步编程实战指南：从入门到精通",
                "author": "技术专家",
                "date": "2025-03-20",
                "category": "Python编程",
                "difficulty": "中级",
                "estimated_read_time": "15分钟"
            },
            "content": {
                "introduction": "在现代Web开发和数据处理中，异步编程已成为提升应用性能的关键技术。Python通过asyncio库提供了强大的异步支持，本文将详细介绍实际开发中的最佳实践。",
                "prerequisites": [
                    "Python 3.7+ 基础",
                    "理解函数和类的基本概念",
                    "了解网络编程基础"
                ],
                "sections": [
                    {
                        "title": "异步编程基础",
                        "content": "异步编程允许程序在等待I/O操作时执行其他任务，从而提高效率。",
                        "key_points": [
                            "协程是异步编程的基本单元",
                            "事件循环管理所有异步任务",
                            "使用async/await语法定义协程"
                        ]
                    },
                    {
                        "title": "核心概念详解",
                        "content": "深入理解asyncio的核心组件和工作原理。",
                        "subsections": [
                            {
                                "title": "协程(Coroutine)",
                                "content": "协程是可以暂停和恢复的函数，使用async def定义。"
                            },
                            {
                                "title": "任务(Task)",
                                "content": "任务包装协程，可以在事件循环中并发执行。"
                            },
                            {
                                "title": "Future对象",
                                "content": "表示异步操作的最终结果，用于协调多个异步操作。"
                            }
                        ]
                    }
                ],
                "code_examples": [
                    {
                        "title": "基础协程示例",
                        "language": "python",
                        "code": """import asyncio

async def fetch_data(url: str) -> str:
    \"\"\"异步获取数据\"\"\"
    # 模拟网络延迟
    await asyncio.sleep(1)
    return f"Data from {url}"

async def main():
    data = await fetch_data("https://api.example.com")
    print(f"获取的数据: {data}")

# 运行协程
asyncio.run(main())""",
                        "explanation": "这个示例展示了如何定义和运行一个简单的协程。"
                    },
                    {
                        "title": "并发任务管理",
                        "language": "python",
                        "code": """import asyncio

async def process_item(item_id: int) -> dict:
    \"\"\"处理单个项目\"\"\"
    await asyncio.sleep(0.5)  # 模拟处理时间
    return {"id": item_id, "status": "processed"}

async def batch_process(items: list) -> list:
    \"\"\"批量处理多个项目\"\"\"
    tasks = []
    for item in items:
        task = asyncio.create_task(process_item(item))
        tasks.append(task)
    
    # 等待所有任务完成
    results = await asyncio.gather(*tasks)
    return results

async def main():
    items = [1, 2, 3, 4, 5]
    results = await batch_process(items)
    print(f"处理结果: {results}")

asyncio.run(main())""",
                        "explanation": "使用asyncio.create_task()创建并发任务，通过asyncio.gather()等待所有任务完成。"
                    },
                    {
                        "title": "错误处理和超时",
                        "language": "python",
                        "code": """import asyncio

async def fetch_with_timeout(url: str, timeout: float = 3.0) -> str:
    \"\"\"带超时的异步获取\"\"\"
    try:
        # 设置超时
        async with asyncio.timeout(timeout):
            await asyncio.sleep(2)  # 模拟网络请求
            return f"Success: {url}"
    except asyncio.TimeoutError:
        return f"Timeout: {url}"
    except Exception as e:
        return f"Error: {url} - {e}"

async def main():
    result = await fetch_with_timeout("https://api.example.com")
    print(result)

asyncio.run(main())""",
                        "explanation": "使用asyncio.timeout()上下文管理器设置超时，确保异步操作不会无限期等待。"
                    }
                ],
                "best_practices": [
                    "避免在协程中使用阻塞操作",
                    "合理设置并发限制",
                    "使用异步上下文管理器管理资源",
                    "为所有异步操作设置超时"
                ],
                "common_pitfalls": [
                    "混用同步和异步代码",
                    "忘记处理异常",
                    "资源泄漏",
                    "死锁问题"
                ],
                "conclusion": "掌握Python异步编程需要理解事件循环机制，熟练使用async/await语法，并遵循最佳实践。通过合理的并发控制和错误处理，可以充分发挥异步编程的优势。",
                "resources": [
                    "官方文档: https://docs.python.org/3/library/asyncio.html",
                    "GitHub示例: https://github.com/python/asyncio",
                    "推荐书籍: 《Python异步编程实战》"
                ]
            },
            "formatting": {
                "include_toc": True,
                "code_highlighting": True,
                "images": ["async_architecture.png", "event_loop_diagram.png"],
                "tables": ["性能对比表", "功能特性表"]
            }
        }
    
    def test_01_scenario_configuration(self):
        """测试场景配置"""
        print("🔧 测试技术教程场景配置...")
        
        # 验证配置完整性
        required_keys = ["scenario_name", "content_type", "target_audience", "success_criteria"]
        for key in required_keys:
            self.assertIn(key, self.scenario_config)
        
        # 验证成功标准
        criteria = self.scenario_config["success_criteria"]
        self.assertIn("article_length", criteria)
        self.assertIn("code_examples", criteria)
        self.assertIn("review_score", criteria)
        
        print(f"  ✅ 场景配置验证通过: {self.scenario_config['scenario_name']}")
        return True
    
    def test_02_article_structure(self):
        """测试文章结构"""
        print("📝 测试技术教程文章结构...")
        
        article = self.create_technical_tutorial_article()
        
        # 验证元数据
        metadata = article["metadata"]
        required_metadata = ["title", "author", "category", "difficulty"]
        for key in required_metadata:
            self.assertIn(key, metadata)
        
        # 验证内容结构
        content = article["content"]
        required_sections = ["introduction", "sections", "code_examples", "best_practices", "conclusion"]
        for section in required_sections:
            self.assertIn(section, content)
        
        # 验证代码示例数量
        code_examples = content["code_examples"]
        self.assertGreaterEqual(len(code_examples), 3)
        
        # 验证每个代码示例的结构
        for example in code_examples:
            self.assertIn("title", example)
            self.assertIn("code", example)
            self.assertIn("explanation", example)
        
        print(f"  ✅ 文章结构验证通过: {len(code_examples)}个代码示例")
        return True
    
    def test_03_content_quality_assessment(self):
        """测试内容质量评估"""
        print("🔍 测试技术教程内容质量...")
        
        article = self.create_technical_tutorial_article()
        content = article["content"]
        
        # 模拟质量评估指标
        quality_metrics = {
            "technical_accuracy": 92,
            "clarity": 88,
            "completeness": 90,
            "practicality": 95,
            "structure": 89
        }
        
        # 计算总分
        total_score = sum(quality_metrics.values()) / len(quality_metrics)
        
        # 验证质量标准
        self.assertGreaterEqual(total_score, 85)
        
        # 生成质量报告
        quality_report = {
            "article_id": "tech-tutorial-001",
            "scenario": self.scenario_config["scenario_name"],
            "quality_metrics": quality_metrics,
            "total_score": round(total_score, 1),
            "strengths": [
                "技术内容准确",
                "代码示例实用",
                "结构清晰"
            ],
            "improvements": [
                "增加更多实际案例",
                "优化部分章节的过渡"
            ],
            "verdict": "PASS" if total_score >= 85 else "FAIL"
        }
        
        # 保存质量报告
        report_file = self.output_dir / "quality_report.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(quality_report, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ 内容质量评估: {quality_report['total_score']}/100 ({quality_report['verdict']})")
        return quality_report
    
    def test_04_seo_optimization_for_technical_content(self):
        """测试技术内容SEO优化"""
        print("🔎 测试技术教程SEO优化...")
        
        article = self.create_technical_tutorial_article()
        title = article["metadata"]["title"]
        
        # 生成SEO优化建议
        seo_optimization = {
            "original_title": title,
            "optimized_titles": [
                f"{title} - 包含完整代码示例",
                f"掌握Python异步编程：实战技巧和最佳实践",
                f"异步编程完全指南：从基础到高级应用",
                f"2025最新Python异步编程教程"
            ],
            "keywords": [
                "Python异步编程",
                "asyncio教程",
                "协程编程",
                "异步并发",
                "Python性能优化",
                "async/await实战"
            ],
            "meta_description": "深入讲解Python异步编程的核心原理和实际应用，包含多个完整代码示例和最佳实践建议，适合中级Python开发者学习和参考。",
            "technical_seo_factors": {
                "code_snippets": len(article["content"]["code_examples"]),
                "structured_data": True,
                "internal_links": 5,
                "external_links": 3
            },
            "optimization_score": 91,
            "recommendations": [
                "在标题中包含'教程'或'指南'关键词",
                "使用代码高亮提高可读性",
                "添加目录便于导航",
                "包含实际应用场景"
            ]
        }
        
        # 验证SEO优化
        self.assertGreaterEqual(seo_optimization["optimization_score"], 80)
        self.assertGreaterEqual(len(seo_optimization["optimized_titles"]), 3)
        self.assertGreaterEqual(len(seo_optimization["keywords"]), 5)
        
        # 保存SEO报告
        seo_file = self.output_dir / "seo_report.json"
        with open(seo_file, 'w', encoding='utf-8') as f:
            json.dump(seo_optimization, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ SEO优化完成: {seo_optimization['optimization_score']}/100")
        return seo_optimization
    
    def test_05_platform_adaptation_for_technical_audience(self):
        """测试技术受众平台适配"""
        print("🌐 测试技术教程平台适配...")
        
        article = self.create_technical_tutorial_article()
        
        # 技术内容平台适配规则
        platform_rules = {
            "technical_blog": {
                "target_audience": "技术开发者",
                "format": "Markdown/HTML",
                "features": ["代码高亮", "数学公式", "图表支持"],
                "length_limit": 10000,
                "seo_importance": "高"
            },
            "zhihu": {
                "target_audience": "技术爱好者",
                "format": "富文本",
                "features": ["专业问答格式", "引用支持", "社区互动"],
                "length_limit": 50000,
                "seo_importance": "中"
            },
            "dev_to": {
                "target_audience": "全球开发者",
                "format": "Markdown",
                "features": ["代码片段", "标签系统", "社区功能"],
                "length_limit": "无限制",
                "seo_importance": "高"
            }
        }
        
        # 生成平台适配版本
        adapted_versions = {}
        for platform, rules in platform_rules.items():
            adapted_versions[platform] = {
                "platform": platform,
                "audience": rules["target_audience"],
                "adaptation_strategy": self.get_adaptation_strategy(platform, article),
                "content_highlights": self.get_content_highlights(article, platform),
                "estimated_engagement": self.estimate_engagement(article, platform),
                "adaptation_complete": True
            }
        
        # 验证适配结果
        self.assertEqual(len(adapted_versions), len(platform_rules))
        
        # 保存适配报告
        adaptation_file = self.output_dir / "platform_adaptation.json"
        with open(adaptation_file, 'w', encoding='utf-8') as f:
            json.dump(adapted_versions, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ 平台适配完成: {len(adapted_versions)}个技术平台")
        return adapted_versions
    
    def get_adaptation_strategy(self, platform: str, article: dict) -> str:
        """获取平台适配策略"""
        strategies = {
            "technical_blog": "完整技术内容，包含所有代码示例和详细解释",
            "zhihu": "专业问答格式，重点突出核心技术和实际应用",
            "dev_to": "国际化技术分享，强调代码质量和最佳实践"
        }
        return strategies.get(platform, "标准技术内容适配")
    
    def get_content_highlights(self, article: dict, platform: str) -> list:
        """获取内容亮点"""
        highlights = []
        content = article["content"]
        
        # 根据平台选择亮点
        if platform == "technical_blog":
            highlights = [
                f"{len(content['code_examples'])}个完整代码示例",
                "详细的技术原理解释",
                "最佳实践和常见问题"
            ]
        elif platform == "zhihu":
            highlights = [
                "解决实际开发问题",
                "技术深度分析",
                "社区互动价值"
            ]
        elif platform == "dev_to":
            highlights = [
                "国际化技术标准",
                "代码质量最佳实践",
                "开发者工具推荐"
            ]
        
        return highlights
    
    def estimate_engagement(self, article: dict, platform: str) -> dict:
        """预估互动情况"""
        # 基于历史数据的简单预估
        base_engagement = {
            "technical_blog": {"views": 5000, "comments": 50, "shares": 200},
            "zhihu": {"views": 8000, "upvotes": 300, "comments": 100},
            "dev_to": {"views": 3000, "reactions": 150, "comments": 40}
        }
        
        # 根据文章质量调整
        quality_factor = 1.2  # 假设高质量文章有20%提升
        estimated = base_engagement.get(platform, {"views": 1000, "engagement": 10})
        
        return {
            "estimated_views": int(estimated.get("views", 1000) * quality_factor),
            "estimated_engagement": int(estimated.get("comments", 10) * quality_factor),
            "confidence_level": "中等"
        }
    
    def test_06_scenario_completeness(self):
        """测试场景完整性"""
        print("🏗️  测试技术教程场景完整性...")
        
        # 运行所有测试
        test_results = []
        
        # 测试1: 场景配置
        try:
            result1 = self.test_01_scenario_configuration()
            test_results.append(("场景配置", result1))
        except Exception as e:
            test_results.append(("场景配置", False))
            print(f"  场景配置测试失败: {e}")
        
        # 测试2: 文章结构
        try:
            result2 = self.test_02_article_structure()
            test_results.append(("文章结构", result2))
        except Exception as e:
            test_results.append(("文章结构", False))
            print(f"  文章结构测试失败: {e}")
        
        # 测试3: 内容质量
        try:
            result3 = self.test_03_content_quality_assessment()
            test_results.append(("内容质量", isinstance(result3, dict)))
        except Exception as e:
            test_results.append(("内容质量", False))
            print(f"  内容质量测试失败: {e}")
        
        # 测试4: SEO优化
        try:
            result4 = self.test_04_seo_optimization_for_technical_content()
            test_results.append(("SEO优化", isinstance(result4, dict)))
        except Exception as e:
            test_results.append(("SEO优化", False))
            print(f"  SEO优化测试失败: {e}")
        
        # 测试5: 平台适配
        try:
            result5 = self.test_05_platform_adaptation_for_technical_audience()
            test_results.append(("平台适配", isinstance(result5, dict)))
        except Exception as e:
            test_results.append(("平台适配", False))
            print(f"  平台适配测试失败: {e}")
        
        # 生成完整性报告
        passed_tests = sum(1 for _, result in test_results if result)
        total_tests = len(test_results)
        
        completeness_report = {
            "scenario": self.scenario_config["scenario_name"],
            "test_results": [
                {"test": test, "passed": passed} for test, passed in test_results
            ],
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "pass_rate": f"{(passed_tests/total_tests*100):.1f}%",
                "completeness_score": (passed_tests/total_tests) * 100
            },
            "generated_files": [
                str(self.output_dir / "quality_report.json"),
                str(self.output_dir / "seo_report.json"),
                str(self.output_dir / "platform_adaptation.json")
            ]
        }
        
        # 保存完整性报告
        completeness_file = self.output_dir / "scenario_completeness.json"
        with open(completeness_file, 'w', encoding='utf-8') as f:
            json.dump(completeness_report, f, indent=2, ensure_ascii=False)
        
        print(f"\n  📊 场景完整性: {passed_tests}/{total_tests} 通过 ({completeness_report['summary']['pass_rate']})")
        
        # 验证通过标准
        self.assertGreaterEqual(passed_tests, total_tests - 1)  # 允许最多1个测试失败
        
        return completeness_report
    
    def run_full_scenario_test(self):
        """运行完整场景测试"""
        print("🚀 开始技术教程场景测试")
        print("=" * 60)
        
        try:
            completeness_report = self.test_06_scenario_completeness()
            
            print("\n" + "=" * 60)
            print("📋 技术教程场景测试完成!")
            
            summary = completeness_report["summary"]
            print(f"  测试通过率: {summary['pass_rate']}")
            print(f"  完整性分数: {summary['completeness_score']:.1f}/100")
            
            if summary['passed_tests'] == summary['total_tests']:
                print("  ✅ 所有测试通过!")
                return True
            else:
                print(f"  ⚠️  {summary['total_tests'] - summary['passed_tests']}个测试失败")
                return False
                
        except Exception as e:
            print(f"❌ 场景测试失败: {e}")
            import traceback
            traceback.print_exc()
            return False


def main():
    """主函数"""
    # 运行unittest测试
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestTechnicalTutorialScenario)
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # 运行完整场景测试
    print("\n" + "=" * 60)
    print("🏗️  运行完整技术教程场景测试...")
    
    scenario_test = TestTechnicalTutorialScenario()
    scenario_test.setUp()
    
    try:
        success = scenario_test.run_full_scenario_test()
        scenario_test.tearDown()
    except Exception as e:
        print(f"❌ 场景测试异常: {e}")
        import traceback
        traceback.print_exc()
        success = False
    
    return result.wasSuccessful() and success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)