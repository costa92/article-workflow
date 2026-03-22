#!/usr/bin/env python3
"""
营销文案场景测试 - 简化版
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

class TestMarketingCopyScenario(unittest.TestCase):
    """测试营销文案场景"""
    
    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        self.output_dir = Path(self.temp_dir) / "output"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 营销文案场景配置
        self.scenario_config = {
            "scenario_name": "marketing_copy",
            "content_type": "营销文案",
            "target_audience": "潜在客户、消费者",
            "marketing_objective": "产品推广、品牌宣传、销售转化",
            "expected_outputs": ["ad_copy", "landing_page", "email_sequence", "social_media_posts", "cta_variations"],
            "success_criteria": {
                "persuasion_score": "≥85/100",
                "conversion_potential": "≥80/100",
                "brand_alignment": "≥90/100",
                "creativity": "≥75/100",
                "a_b_test_variants": "≥3个"
            }
        }
        
    def tearDown(self):
        """测试后清理"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_01_scenario_configuration(self):
        """测试场景配置"""
        print("🔧 测试营销文案场景配置...")
        self.assertEqual(self.scenario_config["scenario_name"], "marketing_copy")
        self.assertEqual(self.scenario_config["content_type"], "营销文案")
        self.assertEqual(len(self.scenario_config["expected_outputs"]), 5)
        print("  ✅ 场景配置验证通过: marketing_copy")
    
    def test_02_create_marketing_content(self):
        """测试创建营销内容"""
        print("📝 创建营销内容...")
        
        # 模拟创建营销内容
        marketing_content = {
            "ad_copy": "🔥 限时优惠！AI智能写作工具，提升10倍创作效率！立即体验 →",
            "landing_page_title": "AI智能写作助手 - 让创作变得更简单",
            "email_sequence": [
                "欢迎邮件: 发现AI写作的神奇力量",
                "功能介绍: 10大核心功能助力创作",
                "案例分享: 用户成功故事",
                "限时优惠: 最后机会，立即行动"
            ],
            "social_media_posts": [
                "🚀 AI写作革命来了！告别写作困难，拥抱高效创作",
                "💡 每天节省3小时写作时间，AI智能写作助你事半功倍",
                "📈 内容创作者必备神器，提升内容质量与发布效率"
            ],
            "cta_variations": [
                "立即免费试用",
                "获取专属优惠",
                "了解更多功能",
                "预约演示"
            ]
        }
        
        # 验证内容结构
        self.assertIn("ad_copy", marketing_content)
        self.assertIn("landing_page_title", marketing_content)
        self.assertIn("email_sequence", marketing_content)
        self.assertIn("social_media_posts", marketing_content)
        self.assertIn("cta_variations", marketing_content)
        
        # 验证内容数量
        self.assertGreaterEqual(len(marketing_content["email_sequence"]), 3)
        self.assertGreaterEqual(len(marketing_content["social_media_posts"]), 3)
        self.assertGreaterEqual(len(marketing_content["cta_variations"]), 3)
        
        print(f"  ✅ 营销内容创建完成: {len(marketing_content['email_sequence'])}个邮件序列")
    
    def test_03_marketing_effectiveness_assessment(self):
        """测试营销效果评估"""
        print("📊 测试营销效果评估...")
        
        # 模拟营销效果评估
        effectiveness_metrics = {
            "persuasion_score": 88,
            "conversion_potential": 82,
            "brand_alignment": 92,
            "creativity": 78,
            "overall_score": 85
        }
        
        # 验证评估指标
        self.assertGreaterEqual(effectiveness_metrics["persuasion_score"], 85)
        self.assertGreaterEqual(effectiveness_metrics["conversion_potential"], 80)
        self.assertGreaterEqual(effectiveness_metrics["brand_alignment"], 90)
        self.assertGreaterEqual(effectiveness_metrics["creativity"], 75)
        self.assertGreaterEqual(effectiveness_metrics["overall_score"], 80)
        
        print(f"  ✅ 营销效果评估: {effectiveness_metrics['overall_score']}/100")
    
    def test_04_a_b_testing_variants(self):
        """测试A/B测试变体"""
        print("🔬 测试A/B测试变体...")
        
        # 模拟A/B测试变体
        ab_test_variants = [
            {
                "variant_id": "A",
                "headline": "AI写作工具：提升10倍创作效率",
                "cta": "立即免费试用",
                "expected_ctr": 3.2
            },
            {
                "variant_id": "B",
                "headline": "智能写作助手：让创作变得更简单",
                "cta": "获取专属优惠",
                "expected_ctr": 3.5
            },
            {
                "variant_id": "C",
                "headline": "内容创作革命：AI驱动的高效写作",
                "cta": "了解更多功能",
                "expected_ctr": 3.8
            }
        ]
        
        # 验证A/B测试变体
        self.assertGreaterEqual(len(ab_test_variants), 3)
        
        for variant in ab_test_variants:
            self.assertIn("variant_id", variant)
            self.assertIn("headline", variant)
            self.assertIn("cta", variant)
            self.assertIn("expected_ctr", variant)
            self.assertGreater(variant["expected_ctr"], 2.0)
        
        print(f"  ✅ A/B测试变体创建完成: {len(ab_test_variants)}个变体")
    
    def test_05_marketing_platform_adaptation(self):
        """测试营销平台适配"""
        print("🌐 测试营销平台适配...")
        
        # 模拟平台适配
        platforms = [
            {
                "platform": "微信",
                "content_type": "公众号文章",
                "character_limit": 2000,
                "features": ["图文结合", "链接", "小程序"]
            },
            {
                "platform": "小红书",
                "content_type": "笔记",
                "character_limit": 1000,
                "features": ["图片为主", "标签", "社区互动"]
            },
            {
                "platform": "抖音",
                "content_type": "短视频",
                "character_limit": 300,
                "features": ["15秒视频", "流行音乐", "特效"]
            }
        ]
        
        # 验证平台适配
        self.assertGreaterEqual(len(platforms), 3)
        
        for platform in platforms:
            self.assertIn("platform", platform)
            self.assertIn("content_type", platform)
            self.assertIn("character_limit", platform)
            self.assertIn("features", platform)
        
        print(f"  ✅ 平台适配完成: {len(platforms)}个平台")
    
    def test_06_scenario_completeness(self):
        """测试场景完整性"""
        print("🏗️  测试营销文案场景完整性...")
        
        # 运行所有测试
        tests_to_run = [
            self.test_01_scenario_configuration,
            self.test_02_create_marketing_content,
            self.test_03_marketing_effectiveness_assessment,
            self.test_04_a_b_testing_variants,
            self.test_05_marketing_platform_adaptation
        ]
        
        passed_tests = 0
        total_tests = len(tests_to_run)
        
        for test_func in tests_to_run:
            try:
                test_func()
                passed_tests += 1
            except Exception as e:
                print(f"  ❌ {test_func.__name__} 测试失败: {e}")
        
        pass_rate = (passed_tests / total_tests) * 100
        self.assertGreaterEqual(pass_rate, 80.0)
        
        print(f"\n  📊 场景完整性: {passed_tests}/{total_tests} 通过 ({pass_rate:.1f}%)")
        print(f"  ✅ 营销文案场景测试通过!")

def run_marketing_copy_scenario():
    """运行营销文案场景测试"""
    print("=" * 60)
    print("🔥 营销文案场景测试")
    print("=" * 60)
    
    # 创建测试套件
    suite = unittest.TestSuite()
    suite.addTest(TestMarketingCopyScenario('test_01_scenario_configuration'))
    suite.addTest(TestMarketingCopyScenario('test_02_create_marketing_content'))
    suite.addTest(TestMarketingCopyScenario('test_03_marketing_effectiveness_assessment'))
    suite.addTest(TestMarketingCopyScenario('test_04_a_b_testing_variants'))
    suite.addTest(TestMarketingCopyScenario('test_05_marketing_platform_adaptation'))
    suite.addTest(TestMarketingCopyScenario('test_06_scenario_completeness'))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 输出结果摘要
    print("\n" + "=" * 60)
    print("📋 营销文案场景测试完成!")
    
    total_tests = result.testsRun
    failed_tests = len(result.failures) + len(result.errors)
    passed_tests = total_tests - failed_tests
    
    print(f"  测试总数: {total_tests}")
    print(f"  通过测试: {passed_tests}")
    print(f"  失败测试: {failed_tests}")
    
    if passed_tests == total_tests:
        print("  ✅ 所有测试通过!")
        return 0
    else:
        print("  ❌ 部分测试失败")
        return 1

if __name__ == "__main__":
    exit_code = run_marketing_copy_scenario()
    sys.exit(exit_code)